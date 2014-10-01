# -*- coding: utf-8 -*-
"""Installer for the mons.urban.dataimport package."""

from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = \
    read('README.rst') + \
    read('docs', 'CONTRIBUTORS.rst') + \
    read('docs', 'CHANGES.rst') + \
    read('docs', 'LICENSE.rst')

setup(
    name='mons.urban.dataimport',
    version='0.1dev',
    description="",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone :: 4.x",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='Python Zope Plone',
    author='Franck NGAHA, Simon DELCOURT',
    author_email='franck.ngaha@imio.be, simon.delcourt@imio.be',
    url='http://pypi.python.org/pypi/mons.urban.dataimport',
    license='GPL V2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['mons', 'mons.urban'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'imio.urban.dataimport',
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            'plone.app.robotframework',
        ],
        'develop': [
            'zest.releaser',
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
