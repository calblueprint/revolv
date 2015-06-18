"""
Custom storage settings used to ensure that static files collected
to Amazon s3 aren't just dropped in the root of the bucket (and instead
are collected to a bucket's subdirectory).

See https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/

One note: we define two different kinds of "storages" here, because we
want to separate the staticfiles that are served on staging with those
served on production (e.g., if we push new staticfiles to staging, we
don't want those to be seen on production yet until we're sure they work).

So, we need to make sure that we run collectstatic twice when deploying
this application: once after pushing new code to staging, which will collect
the static files into the /static_staging/ directory (or whatever we define
the directory name to be in settings.py) and once on production, which will
collect all the static files to the /static_production/ directory in our S3
bucket.

TODO: we should use three different buckets entirely for the production, staging,
and local development environments. See https://github.com/calblueprint/revolv/issues/352
"""

from django.conf import settings
from storages.backends.s3boto import S3BotoStorage


class RevolvProductionStaticStorage(S3BotoStorage):
    """Storage that tells boto to collect files into the staging directory in our S3 bucket."""
    location = settings.STATICFILES_PRODUCTION_LOCATION


class RevolvStagingStaticStorage(S3BotoStorage):
    """Storage that tells boto to collect files into the production directory in our S3 bucket."""
    location = settings.STATICFILES_STAGING_LOCATION
