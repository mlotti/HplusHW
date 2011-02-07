def kwargsDefault(kwargs, name, default):
    if name in kwargs:
        return kwargs[name]
    return default
