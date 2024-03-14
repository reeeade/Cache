from datetime import datetime
from pymemcache.client.base import Client

client = Client('localhost')


def cached_function(expire=None):
    if expire is None:
        expire = 0

    def decorator(func):
        def wrapper(*args, **kwargs):
            n = args[0]
            in_cache = client.get(str(n), default=None)
            if in_cache is not None:
                print(f"{n} in cache")
                return int(in_cache)
            result = func(*args, **kwargs)
            client.set(str(n), result, expire=expire)
            return result

        return wrapper

    return decorator


@cached_function(15)
def fibonacci(n):
    if n < 0:
        raise ValueError("n must be >= 0")
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


a1 = datetime.now()
print(fibonacci(80))
a2 = datetime.now()
print(a2 - a1)
