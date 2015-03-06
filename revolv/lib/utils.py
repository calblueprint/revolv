import importlib


class ImportProxy(object):
    """
    An ImportProxy is a class which acts as a delegation proxy fo an import.
    It is sometimes the case that we have to import something from a module
    that would create a circular dependency, but that it shouldn't matter,
    because we do not actually use the dependency immediately.

    ImportProxy solves this by essentially performing laxy evaluation of an
    import - for example, we could declare a = ImportProxy("b.c.d", "e"): this
    would in general be equivalent to calling `from b.c.d import e; a = e`. If
    there was a circular dependency in which b.c.d imported something from the
    same module in which a was declared.

    Another example:

    # in revolv/base/factories.py
    from revolv.base.profile import Profile
    class ProfileFactory:
        profile = Profile

    # in revolv/base/profile.py
    # from revolv.base.factories import ProfileFactory # would create circular dependency, but now we don't need it
    class Profile(models.model):
        factories = ImportProxy("revolv.base.factories", "ProfileFactory")
    """

    def __init__(self, module_name, object_class_name):
        self.module_name = module_name
        self.object_class_name = object_class_name
        self.object_class = None
        self.has_imported = False

    def import_module(self):
        """Actually import the object if it has not been imported yet."""
        if self.object_class is not None:
            return
        module = importlib.import_module(self.module_name)
        self.object_class = getattr(module, self.object_class_name)

    def __getattr__(self, key):
        """Proxy the attribute request to the loaded object."""
        self.import_module()
        return getattr(self.object_class, key)
