import logging


def info_log(func):
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        # 🪵 log method call to info
        logging.info(f"{func.__name__}: {signature}")
        # 🔨 do the real work
        result = func(*args, **kwargs)
        # 🪵 log result to debug
        logging.critical(result)
        return result
    return wrapper
