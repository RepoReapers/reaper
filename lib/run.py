import multiprocessing
import warnings
import sys
import traceback

QUERY_SAVE = 'INSERT INTO reaper_results({columns}) VALUES ({placeholders})'


class Run(object):
    def __init__(self, repo_root, attributes, database, threshold, processes):
        self.run_id = None
        self.repo_root = repo_root
        self.attributes = attributes
        self.database = database
        self.threshold = threshold
        self.processes = processes

        if self.attributes.is_persistence_enabled:
            # Generating identifier for this run in the reaper_runs table if at
            #   least one attribute has persistence enabled.
            try:
                self.database.connect()
                self.run_id = self.database.post(
                    'INSERT INTO reaper_runs VALUES()'
                )
            finally:
                self.database.disconnect()

            if self.run_id is None:
                warnings.warn('No run_id. Results will not be saved')

    def run(self, samples):
        try:
            print('#' * 25)
            print('{0}'.format(str.center(
                'Run {0}'.format(self.run_id if self.run_id else '-'), 25
            )))
            print('#' * 25)
            self.attributes.global_init(samples)
            with multiprocessing.Pool(self.processes) as pool:
                pool.map(self._process, samples)
            print('#' * 25)
        except Exception as e:
            extype, exvalue, extrace = sys.exc_info()
            traceback.print_exception(extype, exvalue, extrace)

    def _process(self, project_id):
        score = 0.0
        rresults = dict()

        try:
            (score, rresults) = self.attributes.run(project_id, self.repo_root)

            # Generate a green checkmark or red x using terminal escapes
            cresult = '\033[92m✓\033[0m'
            if score < self.threshold:
                cresult = '\033[91m✘\033[0m'

            print(' [{0:>10d}] {1} {2}'.format(project_id, score, cresult))
        except:
            sys.stderr.write('Exception\n\n')
            sys.stderr.write('  Project ID   {0}\n'.format(project_id))
            extype, exvalue, extrace = sys.exc_info()
            traceback.print_exception(extype, exvalue, extrace)
        finally:
            if self.attributes.is_persistence_enabled and rresults is not None:
                self._save(project_id, score, rresults)

    def _save(self, project_id, score, rresults):
        if self.run_id is not None:
            columns = ('run_id', 'project_id', 'score')
            values = (self.run_id, project_id, score)

            for key in rresults:
                if self.attributes.get(key).persist:
                    if rresults[key] is not None:
                        columns += (key,)
                        values += (rresults[key],)
            try:
                query = QUERY_SAVE.format(
                    columns=','.join(columns),
                    placeholders=','.join(['%s' for i in range(len(columns))])
                )
                self.database.connect()
                self.database.post(query, values)
            finally:
                self.database.disconnect()
