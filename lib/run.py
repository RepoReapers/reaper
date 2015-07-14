import multiprocessing
import warnings
import sys
import traceback

QUERY_SAVE = (
    'INSERT INTO reaper_results('
    'run_id, project_id, architecture, forks, subscribers, stargazers, '
    'continuous_integration, documentation, history, license, management, '
    'unit_test, score'
    ') VALUES ('
    '%(run_id)d, %(project_id)d, %(architecture)5.2f, %(forks)d, '
    '%(subscribers)d, %(stargazers)d, %(continuous_integration)d, '
    '%(documentation)5.2f, %(history)5.2f, %(license)d, '
    '%(management)5.2f, %(unit_test)5.2f, %(score)5.2f'
    ')'
)


class Run(object):
    def __init__(self, repo_root, attributes, database, threshold, processes):
        self.run_id = None
        self.repo_root = repo_root
        self.attributes = attributes
        self.database = database
        self.threshold = threshold
        self.processes = processes

        # Generating identifier for this run in the reaper_runs table
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
            print('{0}'.format(str.center('Run {0}'.format(self.run_id), 25)))
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
            if rresults:
                self._save(project_id, score, rresults)

    def _save(self, project_id, score, rresults):
        if self.run_id is not None:
            data = {
                'run_id': self.run_id, 'project_id': project_id, 'score': score
            }

            for key in rresults:
                # Starting off with default values
                if 'community' in key:
                    data['subscribers'] = None
                    data['stargazers'] = None
                    data['forks'] = None
                else:
                    data[key] = None

                if self.attributes.get(key).persist:
                    if 'community' in key:
                        data['subscribers'] = rresults[key]['sub']
                        data['stargazers'] = rresults[key]['star']
                        data['forks'] = rresults[key]['forks']
                    else:
                        data[key] = rresults[key]
            try:
                self.database.connect()
                self.database.post(QUERY_SAVE % data)
            finally:
                self.database.disconnect()
