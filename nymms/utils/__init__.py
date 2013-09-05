import logging

logger = logging.getLogger(__name__)


def retry_on_exception(exception_list, retries=3, reset_func=None,
                       final_exception=None, delay=0):
    """ A decorator that executes a function and catches any exceptions in
    'exception_list'.  It then retries 'retries' with 'delay' seconds between
    retries and executing 'reset_func' each time.  If it fails after reaching
    the retry limit it then raises 'final_exception' or the last exception
    raised.
    """
    def decorator(func):
        def wrapped(*args, **kwargs):
            i = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except exception_list as e:
                    if reset_func:
                        reset_func()
                    if delay:
                        if callable(delay):
                            time.sleep(delay(i))
                        else:
                            time.sleep(delay)
                    logger.warn("%s exception caught.  Retrying %d time(s): "
                                "%s", e.__class__.__name, retries - i,
                                e.message)
                i += 1
                if retries and i > retries:
                    break
            if final_exception:
                raise final_exception(e.message)
            else:
                raise e
        return wrapped
    return decorator
