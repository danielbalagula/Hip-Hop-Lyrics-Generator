# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='song-lyrics-generator',
    version='0.0.1',
    description='Sample package for Python-Guide.org',
    long_description=readme,
    author='Daniel Balagula',
    author_email='db2791@nyu.edu',
    url='https://github.com/danielbalagula/song-lyrics-generator',
    license=license,
    packages=find_packages()
)