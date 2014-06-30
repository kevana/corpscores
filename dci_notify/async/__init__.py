'''
Async decorator for CorpScores
'''

from threading import Thread


def async(f):
    '''Decorator that executes in a new thread.'''
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper
