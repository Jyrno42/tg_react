=============================
Thorgate React
=============================

[![pypi Status](https://badge.fury.io/py/tg_react.png)](https://badge.fury.io/py/tg_react)
[![Build Status](https://travis-ci.org/thorgate/tg_react.svg?branch=master)](https://travis-ci.org/thorgate/tg_react)
[![Coverage Status](https://coveralls.io/repos/thorgate/tg_react/badge.svg)](https://coveralls.io/r/thorgate/tg_react)

Thorgate React is a set of commonly used helpers we use at Thorgate to develop Django based React powered applications.

Documentation
-------------

The full documentation will be available at https://tg_react.readthedocs.org.

Quickstart
----------

Install Thorgate React::

    pip install tg_react

Then use it in a project::

    import tg_react

Features
--------

- [x] Provide constants based on Django settings to the webpack configuration
- [x] Webpack configuration can be setup via Django settings
- [ ] Webpack workflow is integrated inside your Django app (./manage.py [react_build, react_hot])
- [x] Helpers to setup urls when letting React do the frontend Routing
- [ ] Full test coverage
- [ ] Documented
