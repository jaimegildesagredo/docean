# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_description = open('README.rst').read()

setup(
    name='docean',
    version='0.1.0',
    description='Docean is a command-line client for the DigitalOcean API v2',
    long_description=long_description,
    url='https://github.com/jaimegildesagredo/docean',
    author='Jaime Gil de Sagredo Luna',
    author_email='jaimegildesagredo@gmail.com',
    license='Apache 2.0',
    packages=find_packages(exclude=['specs', 'specs.*']),
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: Apache Software License'
    ]
)
