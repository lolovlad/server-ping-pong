from types import MethodType


class Fluent(object):
    def __getattribute__(self, item):
        funct = object.__getattribute__(self, item)
        if funct and type(funct) == MethodType:
            def fluent(*args, **kwargs):
                ans = funct(*args, **kwargs)
                return ans if ans is not None else self
            return fluent
        return funct

