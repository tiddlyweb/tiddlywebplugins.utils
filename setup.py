"""
Setup.py for tiddlywebplugins
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION = 0.7

setup(name = 'tiddlywebplugins',
        version = VERSION,
        description = 'Tools and methods for managing TiddlyWeb plugins',
        author = 'Chris Dent',
        author_email = 'cdent@peermore.com',
        url = 'http://github.com/tiddlyweb/tiddlywebplugins',
        packages = ['tiddlywebplugins'],
        platforms = 'Posix; MacOS X; Windows',
        install_requires = ['tiddlyweb'],
        )




