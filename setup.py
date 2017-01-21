# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='cat-cannon',
    version='0.1.0',
    description='Scripts for my Raspberry Pi movement detection based water disincentive for Cats',
    long_description=readme,
    author='Phillip Whittlesea',
    author_email='pw.github@thega.me.uk',
    url='https://github.com/pwhittlesea/cat-cannon',
    license=license,
    packages=find_packages()
)

