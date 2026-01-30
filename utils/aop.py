import traceback
from functools import wraps


def log_exceptions(log, context: str = ""):
    """
    AOP decorator that logs uncaught exceptions and lets them bubble up.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                traceback_str = ""
                for line in traceback.format_exc().splitlines():
                    traceback_str += f"\n{line}"

                log(f"ERROR in {context or func.__name__}\n{type(e).__name__}: {e}\n{traceback_str}\n")
                raise e
                
        return wrapper
    return decorator
