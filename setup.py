# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '1.0b1'

README = open("README.rst").read()
HISTORY = open(os.path.join("docs", "HISTORY.rst")).read()

setup(name='collective.gridlets',
      version=version,
      description="(Sub)Homepages manager using Gridster.js for Plone.",
      long_description=README + "\n" + HISTORY,
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          "Development Status :: 4 - Beta",
          "Framework :: Plone",
          "Framework :: Plone :: 4.3",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
      ],
      keywords='plone grid portlets homepage cover dynamic',
      author='Víctor Fernández de Alba',
      author_email='sneridagh@gmail.com',
      url='https://github.com/collective/collective.gridlets',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
