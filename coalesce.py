class GreedyAccess(object):
    def __init__(self, thing, sentinel=None):
        self.thing = thing
        self.sentinel = sentinel

    def __getattr__(self, attr):
        try:
            return GreedyAccess(getattr(self.thing, attr),
                                self.sentinel)
        except AttributeError:
            return GreedyAccess(self.sentinel, self.sentinel)

    def unbox(self, new_sentinel=None):
        if self.thing != self.sentinel:
            return self.thing
        elif new_sentinel != self.sentinel:
            return new_sentinel
        else:
            return self.sentinel


class NoneCoalesce(object):
    "Standard operations on object for 'is not None'"
    def __init__(self, obj):
        self.obj = obj

    def __getattr__(self, name):
        try:
            return getattr(self.obj, name)
        except AttributeError:
            return NoneCoalesce(None)

    def __getitem__(self, item):
        try:
            return self.obj[item]
        except (TypeError, KeyError):
            return NoneCoalesce(None)

    def __call__(self, *args, **kwds):
        try:
            return self.obj(*args, **kwds)
        except TypeError:
            return NoneCoalesce(None)

    def __bool__(self):
        return self.obj is not None

    def __repr__(self):
        return "NoneCoalesce[%r]" % self.obj

    def __str__(self):
        return "NoneCoalesce[%r]" % self.obj

    def __len__(self):
        try:
            return len(self.obj)
        except TypeError:
            return 0
