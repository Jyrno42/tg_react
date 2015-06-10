#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import tg_react

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = tg_react.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.md').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='Thorgate React',
    version=version,
    description="""Thorgate React is a set of commonly used helpers we use at Thorgate to develop Django based React powered applications.""",
    long_description=readme + '\n\n' + history,
    author='Thorgate',
    author_email='jyrno@thorgate.eu',
    url='https://github.com/thorgate/tg_react',
    packages=[
        'tg_react',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='tg_react',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
