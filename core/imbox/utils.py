def merge_two_dicts(x, y):
    """Copied from https://stackoverflow.com/a/26853961/4386191"""
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z


def str_encode(value='', encoding=None, errors='strict'):
    return str(value, encoding, errors)


def str_decode(value='', encoding=None, errors='strict'):
    if isinstance(value, str):
        return bytes(value, encoding, errors).decode('utf-8')
    elif isinstance(value, bytes):
        return value.decode(encoding or 'utf-8', errors=errors)
    else:
        raise TypeError("Cannot decode '{}' object".format(value.__class__))