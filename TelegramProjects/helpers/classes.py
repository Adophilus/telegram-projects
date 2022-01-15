import types

class RecursiveNamespace(types.SimpleNamespace):
    # def __init__(self, /, **kwargs):  # better, but Python 3.8+
    def __init__(self, **kwargs):
        """Create a SimpleNamespace recursively"""
        self.__dict__.update({k: self.__elt(v) for k, v in kwargs.items()})

    def __elt(self, elt):
        """Recurse into elt to create leaf namespace objects"""
        if type(elt) is dict:
            return type(self)(**elt)
        if type(elt) in (list, tuple):
            return [self.__elt(i) for i in elt]
        return elt

    # Optional, allow comparison with dicts:
    #def __eq__(self, other):
    #    return self.__dict__ == (other.__dict__ if hasattr(other, '__dict__') else other)
