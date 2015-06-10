#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_tg_react
------------

Tests for `tg_react` webpack module.
"""
from django.test import TestCase

from tg_react.webpack import WebPackConfig


class TestTgWebpack(TestCase):
    def get_exports_part(self, result):
        start_tag = 'module.exports = {'
        end_tag = '};'

        self.assertTrue(start_tag in result)
        self.assertTrue(end_tag in result)

        base_idx = result.index(start_tag) + len(start_tag)
        return result[base_idx:result.index(end_tag, base_idx)].strip().strip(',')

    def test_all_off(self):
        with self.settings(WEBPACK_CONFIG={}):
            result = WebPackConfig.get_config()[0]
            exports = self.get_exports_part(result)

            self.assertTrue('target: "web"' in exports)
            self.assertTrue('LimitChunkCountPlugin' not in exports)
            self.assertTrue('DedupePlugin' not in exports)
            self.assertTrue('UglifyJsPlugin' not in exports)
            self.assertTrue('NODE_ENV: JSON.stringify("production")' not in exports)
            self.assertTrue('loader: "jshint-loader"' not in exports)
            self.assertTrue('jshint: {' not in exports)

    def test_pre_render(self):
        with self.settings(WEBPACK_CONFIG=dict(pre_render=True)):
            result = WebPackConfig.get_config()[0]
            exports = self.get_exports_part(result)

            self.assertTrue('target: "node"' in exports)
            self.assertTrue('LimitChunkCountPlugin' in exports)

    def test_use_react_addons(self):
        with self.settings(WEBPACK_CONFIG=dict(use_react_addons=True)):
            result = WebPackConfig.get_config()[0]
            exports = self.get_exports_part(result)

            self.assertTrue("react$: 'react/addons.js'" in exports)

    def test_minify(self):
        with self.settings(WEBPACK_CONFIG=dict(minify=True)):
            result = WebPackConfig.get_config()[0]
            exports = self.get_exports_part(result)

            self.assertTrue('DedupePlugin' in exports)
            self.assertTrue('UglifyJsPlugin' in exports)
            self.assertTrue('NODE_ENV: JSON.stringify("production")' in exports)

    def test_have_constant(self):
        with self.settings(WEBPACK_CONSTANT_PROCESSORS=['tests.test_webpack.constants']):
            result = WebPackConfig.get_config()[0]
            exports = self.get_exports_part(result)

            self.assertTrue('TG_REACT' in exports)

    def test_jshint(self):
        with self.settings(WEBPACK_CONFIG=dict(jshint=True)):
            result = WebPackConfig.get_config()[0]
            exports = self.get_exports_part(result)

            self.assertTrue('loader: "jshint-loader"' in exports)
            self.assertTrue("process.stdout.write('\\x07')" in exports)
            self.assertTrue('jshint: {' in exports)

        with self.settings(WEBPACK_CONFIG=dict(no_beep=True, jshint=True)):
            result = WebPackConfig.get_config()[0]
            exports = self.get_exports_part(result)

            self.assertTrue('loader: "jshint-loader"' in exports)
            self.assertTrue("process.stdout.write('\\x07')" not in exports)
            self.assertTrue('jshint: {' in exports)


def constants(context):
    return {
        'TG_REACT': 'yesiam',
    }
