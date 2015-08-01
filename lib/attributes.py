import distutils
import importlib
import os
import shutil
import sys
import types
import traceback
from datetime import datetime
from multiprocessing import TimeoutError
from multiprocessing.pool import ThreadPool

import attributes

from lib import utilities


class Attribute(object):
    def __init__(self, attribute, **goptions):
        self.name = attribute.get('name', '')
        self.initial = attribute.get('initial', '').lower()
        self.weight = attribute.get('weight', 0.0)
        self.enabled = attribute.get('enabled', True)
        self.essential = attribute.get('essential', False)
        self.persist = attribute.get('persist', True)
        self.dependencies = attribute.get('dependencies', list())
        self.options = goptions
        self.options.update(attribute.get('options', dict()))
        self.reference = importlib.import_module('{0}.main'.format(self.name))

    def __getstate__(self):
        state = self.__dict__.copy()
        if isinstance(self.reference, types.ModuleType):
            state['reference'] = self.reference.__name__
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        if isinstance(self.reference, str):
            self.reference = importlib.import_module(
                '{0}.main'.format(self.name)
            )


class Attributes(object):
    def __init__(
        self, attributes, database, cleanup=False, keystring=None, **goptions
    ):
        self.attributes = None
        self.database = database
        self.today = goptions.get('today', str(datetime.today().date()))
        self.timeout = goptions.get('timeout', '30M')
        self.cleanup = cleanup

        self._parse_attributes(attributes, **goptions)
        self._parse_keystring(keystring)

    def global_init(self, samples):
        try:
            if not self._validate_dependencies():
                raise Exception(
                    'Missing dependencies must be installed to continue.'
                )

            self.database.connect()
            for attribute in self.attributes:
                if hasattr(attribute.reference, 'global_init'):
                    with self.database.cursor() as cursor:
                        attribute.reference.global_init(cursor, samples)
        finally:
            self.database.disconnect()

    def run(self, project_id, repository_root):
        invalidated = False
        score = 0
        rresults = dict()
        repository_home = os.path.join(repository_root, str(project_id))

        try:
            self.database.connect()

            repository_path = self._init_repository(
                project_id, repository_home
            )
            for attribute in self.attributes:
                bresult = False
                rresult = None

                if not attribute.enabled:
                    continue

                with self.database.cursor() as cursor:
                    if hasattr(attribute.reference, 'init'):
                        attribute.reference.init(cursor)

                with self.database.cursor() as cursor, ThreadPool(1) as pool:
                    async_result = pool.apply_async(
                        func=attribute.reference.run,
                        args=(project_id, repository_path, cursor),
                        kwds=attribute.options
                    )
                    try:
                        timeout = utilities.parse_datetime_delta(
                            attribute.options.get('timeout', self.timeout)
                        )
                        (bresult, rresult) = async_result.get(
                            timeout=timeout.total_seconds()
                        )
                    except TimeoutError:
                        sys.stderr.write(
                            (
                                ' \033[91mWARNING\033[0m [{0:10d}] '
                                '{1} timed out\n'
                            ).format(project_id, attribute.name)
                        )

                rresults[attribute.name] = rresult

                if not bresult and attribute.essential:
                    score = 0
                    invalidated = True

                if not invalidated:
                    score += bresult * attribute.weight
        except:
            sys.stderr.write('Exception\n\n')
            sys.stderr.write('  Project ID   {0}\n'.format(project_id))
            extype, exvalue, extrace = sys.exc_info()
            traceback.print_exception(extype, exvalue, extrace)
        finally:
            self.database.disconnect()
            if self.cleanup:
                self._cleanup(repository_home)
            return (score, rresults)

    def get(self, name):
        for attribute in self.attributes:
            if attribute.name == name:
                return attribute

    @property
    def is_persistence_enabled(self):
        for attribute in self.attributes:
            if attribute.persist:
                return True
        return False

    def _cleanup(self, repository_home):
        shutil.rmtree(repository_home, ignore_errors=True)

    def _init_repository(self, project_id, repository_home):
        repository_path = repository_home  # Default

        if not os.path.exists(repository_path):
            os.mkdir(repository_path)

        items = os.listdir(repository_path)
        if items:
            for item in os.listdir(repository_path):
                itempath = os.path.join(repository_path, item)
                if os.path.isdir(itempath):
                    repository_path = itempath
                    break
        else:
            (repo_owner, repo_name) = self.database.get(
                '''
                    SELECT u.login, p.name
                    FROM projects p
                        JOIN users u ON u.id = p.owner_id
                    WHERE p.id = {0}
                '''.format(project_id)
            )
            if not (repo_owner or repo_name):
                raise ValueError('Invalid project ID {0}.'.format(project_id))

            last_commit_date = self.database.get(
                '''
                    SELECT DATE(c.created_at)
                    FROM project_commits pc
                        JOIN commits c ON c.id = pc.commit_id
                    WHERE pc.project_id = {0}
                    ORDER BY c.created_at DESC
                    LIMIT 1
                '''.format(project_id)
            )

            if last_commit_date is None:
                last_commit_date = self.today

            repository_path = utilities.clone(
                repo_owner, repo_name, repository_path, last_commit_date
            )

        return repository_path

    def _parse_attributes(self, attributes, **goptions):
        if attributes:
            self.attributes = list()
            for attribute in attributes:
                self.attributes.append(Attribute(attribute, **goptions))

    def _disable_attributes(self):
        for attribute in self.attributes:
            attribute.enabled = False

    def _disable_persistence(self):
        for attribute in self.attributes:
            attribute.persist = False

    def _parse_keystring(self, keystring):
        if keystring:
            # Clean the slate
            self._disable_attributes()
            self._disable_persistence()

            for key in keystring:
                attribute = next(
                    attribute
                    for attribute in self.attributes
                    if attribute.initial == key.lower()
                )
                attribute.enabled = True
                attribute.persist = key.isupper()

    def _validate_dependencies(self):
        valid = True
        for attribute in self.attributes:
            if attribute.enabled and attribute.dependencies:
                for dependency in attribute.dependencies:
                    if not distutils.spawn.find_executable(dependency):
                        sys.stderr.write(
                            '[{0}] Dependency {1} missing\n'.format(
                                attribute.name, dependency
                            )
                        )
                        valid = False
        return valid
