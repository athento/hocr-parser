#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='hocr-parser',
    version='0.1',
    description='HOCR Specification Python Parser',
    author='Athento',
    author_email='rh@athento.com',
    url='https://github.com/athento/hocr-parser',
    license='Apache 2.0 License',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: OCR'
    ],
    package_dir={'hocr_parser': 'src/hocr_parser'},
    packages=find_packages('src'),
    dependency_links=[
        'bzr+lp:beautifulsoup#egg=beautifulsoup-4.0',
    ],
    install_requires=[
        'beautifulsoup4'
    ],
    extras_require={
        'test': [
            'pytest'
        ],
    },
)
