import time
import logging
from functools import wraps


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """
    Повторное выполнение функции с экспоненциальной задержкой при возникновении исключения.

    Формула задержки:
        t = start_sleep_time * (factor ** n), пока t < border_sleep_time
        t = border_sleep_time, если t >= border_sleep_time
    """
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            sleep_time = start_sleep_time
            attempt = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    logging.warning(
                        f"Function '{func.__name__}' failed with exception: {e}. "
                        f"Retrying in {sleep_time:.2f} seconds (attempt {attempt})..."
                    )
                    time.sleep(sleep_time)
                    sleep_time = min(sleep_time * factor, border_sleep_time)

        return inner

    return func_wrapper
