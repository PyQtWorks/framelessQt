#!/usr/bin/env python
# -*- coding: utf-8 -*-
# setup.py

from setuptools import setup
from setuptools import find_packages

setup(name='framelessQt',
      version='0.1',
      description='A collection of PySide2 widgets facilitating frameless UI design',
      url='http://github.com/michal-rutkowski/framelessQt',
      author='Michal Adam Rutkowski',
      author_email='rutkowski.michal.jp@gmail.com',
      license='MIT',
      include_package_data=True,
      packages=find_packages(),
      zip_safe=False)
