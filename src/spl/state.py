import lockfile
import os
import simplejson

from spl.errors import CannotGetStateLockException


_INITIAL_STATE = {
    'installed_resources': {}
}

_STATE_DIR = '.spl/'
_STATE_FILE = _STATE_DIR + 'spl-state-v1.json'


def acquire_lock_or_die():
    try:
        lf = lockfile.LockFile(_STATE_DIR)
        lf.acquire(timeout=0)
        return lf
    except lockfile.AlreadyLocked:
        raise CannotGetStateLockException()


class StateLock(object):

    def __enter__(self):
        self.lf = acquire_lock_or_die()

    def __exit__(self, ttype, value, traceback):
        if self.lf and self.lf.i_am_locking():
            self.lf.release()


class State(StateLock):
    def __init__(self, state=_INITIAL_STATE):
        self._state = state

    @staticmethod
    def load():
        with StateLock():
            if os.path.exists(_STATE_FILE):
                with open(_STATE_FILE, 'r') as stateFile:
                    state = simplejson.load(stateFile)
                    print(state)
                    return State(state)
            else:
                return State()

    def save(self):
        with StateLock():
            with open(_STATE_FILE, 'w') as stateFile:
                return simplejson.dump(self._state, stateFile)

    def __enter__(self):
        StateLock.__enter__(self)
        return self

    def __exit__(self, ttype, value, traceback):
        self.save()
        StateLock.__exit__(self, ttype, value, traceback)

    @property
    def installed_resources(self):
        return self._state['installed_resources'].copy()
