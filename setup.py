#!/usr/bin/env python

from distutils.core import setup

setup(name='kfp-buildkit',
      version='1.0',
      description='Small docker stub for the kfp client to build images using (rootless) buildkit',
      author='Sebastian Alberternst',
      author_email='alberternst@gmail.com',
      url='https://www.python.org/sigs/distutils-sig/',
      packages=['docker'],
      )
