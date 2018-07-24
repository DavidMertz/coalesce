#!/usr/bin/env python
"""
Access messy nested data structures

GreedyAccess will keep marching down trees even if failure occured earlier:

    >>> from coalesce import GreedyAccess, make_test
    >>> cfg = make_test()
    >>> GreedyAccess(cfg).user.profile.song
    <GreedyAccess proxy for 'Nightclubbing'>
    >>> GreedyAccess(cfg).user.profile.song + ' and spam'
    'Nightclubbing and spam'
    >>> GreedyAccess(cfg).user.profile.food
    <GreedyAccess proxy for None>
    >>> print(GreedyAccess(cfg).user.profile.food.unbox())
    None
    >>> GreedyAccess(cfg).user.profile.food.unbox('spam')
    'spam'
    >>> GreedyAccess(cfg).user.profile.food.unbox('spam') + ' and spam'
    'spam and spam'

NoneCoalesce only descends until a None is encountered.  Accessing attributes
or keys of None will still fail:

    >>> from coalesce import NoneCoalesce
    >>> NoneCoalesce(cfg).user.profile.song
    <NoneCoalesce proxy for 'Nightclubbing'>
    >>> NoneCoalesce(cfg).user.profile.song.unbox()
    'Nightclubbing'
    >>> NoneCoalesce(cfg).user.profile.food
    Traceback (most recent call last):
        ...
    AttributeError: 'types.SimpleNamespace' object has no attribute 'food'
    >>> NoneCoalesce(cfg).user.profile
    <NoneCoalesce proxy for namespace(arms=2, song='Nightclubbing')>

    >>> val = None
    >>> print(NoneCoalesce(val).attr)
    None


We provide for returning values other than None if some other default is more
useful for your use case (a zero-argument lambda function would often be
useful here):

    #doctest: +ELLIPSIS
    >>> def say_spam():
    ...     return "spam"
    ...
    >>> GreedyAccess(cfg).user.profile.food.unbox(say_spam)
    'spam'
    >>> GreedyAccess(cfg).user.profile.food.unbox(say_spam, lazy=False) #doctest: +ELLIPSIS
    <function say_spam ...>

"""

import wrapt


class GreedyAccess(wrapt.ObjectProxy):
    "Nested access casting lookup failures to None proxy"
    def __getattr__(self, attr):
        try:
            return GreedyAccess(getattr(self.__wrapped__, attr))
        except AttributeError:
            return GreedyAccess(None)

    def __getitem__(self, key):
        try:
            return GreedyAccess(self.__wrapped__[key])
        except KeyError:
            return GreedyAccess(None)

    def __str__(self):
        return "<GreedyAccess proxy for %r>" % (self.__wrapped__)

    __repr__ = __str__

    def unbox(self, default=None, lazy=True):
        if self.__wrapped__ is None:
            if lazy and callable(default):
                return default()
            else:
                return default
        else:
            return self.__wrapped__


class NoneCoalesce(wrapt.ObjectProxy):
    "Nested access masking lookup failures on None only"
    def __getattr__(self, attr):
        if self.__wrapped__ is None:
            return None
        else:
            return NoneCoalesce(getattr(self.__wrapped__, attr))

    def __getitem__(self, key):
        if self.__wrapped__ is None:
            return None
        else:
            return NoneCoalesce(self.__wrapped__[key])

    def __str__(self):
        return "<NoneCoalesce proxy for %r>" % (self.__wrapped__)

    __repr__ = __str__

    def unbox(self, default=None, lazy=True):
        if self.__wrapped__ is None:
            if lazy and callable(default):
                return default()
            else:
                return default
        else:
            return self.__wrapped__


def make_test():
    from types import SimpleNamespace
    cfg = SimpleNamespace()
    cfg.user = SimpleNamespace()
    cfg.user.profile = SimpleNamespace()
    cfg.user.profile.arms = 2
    cfg.user.profile.song = "Nightclubbing"
    return cfg


if __name__ == "__main__":
    import doctest
    doctest.testmod()

