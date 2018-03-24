def wrap_method(cls, style, namer):
    method_name = namer(style)

    def wrapper(self, *args, **kwargs):
        return self._in(method_name, style, *args, **kwargs)
    setattr(cls, method_name, wrapper)
    return wrapper


def wrap_methods(cls):
    for style in cls.WRAP_STYLES:
        setattr(cls, style, wrap_method(cls, style, cls.METHOD_NAMER))
    return cls
