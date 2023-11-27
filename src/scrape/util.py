
class CannotFind(Exception):
    def __init__(self, args, dargs):
        msg = f'Nothing found by {args} and {dargs}'
        super().__init__(msg)


def find(soup, *args, **dargs):
    result = soup.find(*args, **dargs)
    if not result:
        raise CannotFind(args, dargs)
    else:
        return result


def find_all(soup, *args, **dargs):
    result = soup.find_all(*args, **dargs)
    if not result:
        raise CannotFind(args, dargs)
    else:
        return result
