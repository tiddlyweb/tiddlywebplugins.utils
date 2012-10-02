"""
Setup.py for tiddlywebplugins.utils
"""

import os
from setuptools import setup, find_packages

VERSION = '1.3'

setup(
        namespace_packages = ['tiddlywebplugins'],
        name = 'tiddlywebplugins.utils',
        long_description=open(os.path.join(os.path.dirname(__file__), 'README')).read(),
        version = VERSION,
        description = 'Tools and methods for managing TiddlyWeb plugins',
        author = 'Chris Dent',
        author_email = 'cdent@peermore.com',
        url = 'http://pypi.python.org/pypi/tiddlywebplugins.utils',
        packages = find_packages(exclude='test'),
        platforms = 'Posix; MacOS X; Windows',
        install_requires = ['tiddlyweb>=1.2.0'],
        zip_safe = False,
        )
