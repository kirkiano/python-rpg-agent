from functools import partial, update_wrapper


def named_partial(func, *args, **kwargs):
    """
    Partially apply the given func to the given args and kwargs,
    but also preserve the function's __name__ etc in the resulting
    partial application.
    """
    partially_applied = partial(func, *args, **kwargs)
    update_wrapper(partially_applied, func)
    return partially_applied
