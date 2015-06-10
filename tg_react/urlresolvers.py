import re

from django.conf import settings
from django.core.urlresolvers import RegexURLResolver


class ReactBackendUrlResolver(RegexURLResolver):
    def __init__(self, urlconf_name, default_kwargs=None, app_name=None, namespace=None):
        regex = re.compile('^%s/' % self.get_backend_prefix(), re.UNICODE)

        super(ReactBackendUrlResolver, self).__init__(regex, urlconf_name, default_kwargs, app_name, namespace)

    @classmethod
    def get_backend_prefix(cls):
        return getattr(settings, 'TG_BACKEND_PREFIX', 'd')


def react_patterns(*args):
    return [ReactBackendUrlResolver(list(args))]
