#!/usr/bin/env python
#
# Copyright (c) 2020, Dr. Nandor Poka
# Distributed under the terms of the 3-clause BSD License.

import os
from setuptools import find_packages, setup
from src.sos_java._version import __version__
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

def get_long_description():
    with open(os.path.join(CURRENT_DIR, "README.md"), "r") as ld_file:
        return ld_file.read()

setup(
    name="sos-collection-java",
    version=__version__,
    description='SoS Notebook extension for Java.',
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author='Dr. Nandor Poka',
    url='https://github.com/nandor-poka/sos-collection-java',
    author_email='np@np-bio.info',
    maintainer = 'Dr. Nandor Poka',
    maintainer_email='np@np-bio.info',
    license='"BSD-3-Clause',
    include_package_data=True,

    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
     package_data={'': ['src/*.json']},
    install_requires=[
        'sos>=0.21.5', 'sos-notebook>=0.19.4', 
    ],
    entry_points='''
[sos_languages]
Java = sos_java.kernel:sos_java
''')