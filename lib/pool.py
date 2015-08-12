import multiprocessing
import multiprocessing.pool


class NonDaemonicProcess(multiprocessing.Process):
    def _get_daemon(self):
        return False

    def _set_daemon(self, value):
        pass

    daemon = property(_get_daemon, _set_daemon)


class NonDaemonicProcessPool(multiprocessing.pool.Pool):
    Process = NonDaemonicProcess
