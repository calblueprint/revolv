import factory
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from revolv.base.models import RevolvUserProfile


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: "user_%d" % n)
    email = factory.Sequence(lambda n: "user_%d@revolv.org" % n)
    first_name = "John"
    last_name = "Factory"

    @classmethod
    def _generate(cls, create, attrs):
        """
        Override the default _generate() to disable the post-save signal.
        See http://factoryboy.readthedocs.org/en/latest/recipes.html
        """
        from revolv.base.signals import create_profile_of_user

        # Note: If the signal was defined with a dispatch_uid, include that in both calls.
        post_save.disconnect(create_profile_of_user, sender=User)
        user = super(UserFactory, cls)._generate(create, attrs)
        post_save.connect(create_profile_of_user, sender=User)
        return user


class RevolvUserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RevolvUserProfile
    user = factory.SubFactory(UserFactory)


class RevolvUserProfileAdminFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RevolvUserProfile
    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        """See http://factoryboy.readthedocs.org/en/latest/recipes.html"""
        if not create:
            # Simple build, do nothing.
            return
        self.make_administrator()


class RevolvUserProfileFactories(object):
    base = RevolvUserProfileFactory
    admin = RevolvUserProfileAdminFactory
