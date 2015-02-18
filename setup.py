#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

readme = open('README.md').read()
history = open('HISTORY.md').read().replace('.. :changelog:', '')

requirements = [
    'Django<1.8',
]

test_requirements = [
    'nose>=1.3,<2',
    'factory_boy>=2.4,<3.0',
    'fake-factory>=0.4.0,<1',
    'nosexcover>=1.0.8, <2',
    'ipdb',
    'mock',
]

setup(
    name='django-cache-manager',
    version='0.1.1',
    description='Cache manager for django models',
    long_description=readme + '\n\n' + history,
    author='Vijay Katam',
    url='https://github.com/vijaykatam/django-cache-manager',
    packages=find_packages(exclude=('tests',)),
    package_dir={'django_cache_manager':
                 'django_cache_manager'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='django-cache-manager',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='nose.collector',
    tests_require=test_requirements,
)
