import json
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.serializers.json import DjangoJSONEncoder
from django.template.loader import render_to_string
from django.utils.module_loading import import_string


class WebpackConstants(object):
    @classmethod
    def get_constant_processors(cls):
        processors = getattr(settings, 'WEBPACK_CONSTANT_PROCESSORS', ['tg_react.webpack.default_constants'])

        if not isinstance(processors, (list, tuple)):
            raise ImproperlyConfigured('WEBPACK_CONSTANT_PROCESSORS must be a list or tuple')

        return processors

    @classmethod
    def collect(cls):
        """ Load all constant generators from settings.WEBPACK_CONSTANT_PROCESSORS
            and concat their values.
        """
        constants = {}

        for method_path in WebpackConstants.get_constant_processors():
            method = import_string(method_path)

            if not callable(method):
                raise ImproperlyConfigured('Constant processor "%s" is not callable' % method_path)

            result = method(constants)

            if isinstance(result, dict):
                constants.update(result)

        return constants


def default_constants(context):
    return {
        'SITE_URL': settings.SITE_URL,
        'STATIC_URL': settings.STATIC_URL,
    }


class WebPackConfig(object):
    @classmethod
    def get_json_encoder(cls):
        encoder = getattr(settings, 'WEBPACK_JSON_ENCODER', 'django.core.serializers.json.DjangoJSONEncoder')

        the_module = import_string(encoder)

        if not issubclass(the_module, json.JSONEncoder):
            raise ImproperlyConfigured('WEBPACK_JSON_ENCODER must be subclass of json.JSONEncoder.')

        return the_module

    @classmethod
    def default_settings(cls):
        return {
            'jshint': False,
            'pre_render': False,
            'use_react_addons': False,
            'minify': False,
            'no_beep': False,
        }

    @classmethod
    def get_configurations(cls):
        custom_config = getattr(settings, 'WEBPACK_CONFIG', {})
        if isinstance(custom_config, dict):
            custom_config = [custom_config, ]

        result = []

        for cfg in custom_config:
            config = cls.default_settings()
            config.update(cfg)
            result.append(config)

        return result

    @classmethod
    def get_config(cls):
        return list(map(cls.render_config, cls.get_configurations()))

    @classmethod
    def render_config(cls, config):
        config.update({
            'constants': json.dumps(WebpackConstants.collect(), cls=cls.get_json_encoder()),
        })

        return render_to_string('tg_react/webpack_config.template', config)
