# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '0.1'


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('README.rst')
    + '\n' +
    read('CHANGES.rst'))

setup(
    name='z3c.formwidget.multiunit',
    version=version,
    description="A multi unit widget for z3c.form.",
    long_description=long_description,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Zope3",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Zope",
    ],
    keywords='zope zope3 z3c.form',
    author='Thomas Massmann',
    author_email='thomas.massmann@it-spir.it',
    url='https://github.com/tmassman/z3c.formwidget.multiunit',
    download_url='http://pypi.python.org/pypi/z3c.formwidget.multiunit',
    license='GPL',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['z3c', 'z3c.formwidget'],
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'setuptools',
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,
)
