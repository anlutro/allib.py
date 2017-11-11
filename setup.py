#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages
import os
import os.path

# allow setup.py to be ran from anywhere
os.chdir(os.path.dirname(__file__))

setup(
	name='allib',
	version='0.3.1',
	license='MIT',
	description='Personal library of useful stuff.',
	author='Andreas Lutro',
	author_email='anlutro@gmail.com',
	url='https://github.com/anlutro/allib.py',
	packages=find_packages(include=('allib', 'allib.*')),
)
