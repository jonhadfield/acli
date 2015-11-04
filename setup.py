#!/usr/bin/env python

import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
sys.path.insert(0, os.path.abspath('lib'))

version = "0.1.6"

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.md').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

long_description = readme + '\n\n' + history

if sys.argv[-1] == 'readme':
    print(long_description)
    sys.exit()


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

setup(
    name='acli',
    version=version,
    author='Jon Hadfield',
    author_email='jon@lessknown.co.uk',
    url='http://github.com/jonhadfield/acli',
    download_url='https://github.com/jonhadfield/acli/tarball/{0}'.format(version),
    install_requires=['docopt==0.6.2',
                      'colorclass==1.2.0',
                      'botocore>=1.2.10',
                      'boto3>=1.1.4',
                      'requests>=2.7.0',
                      'terminaltables>=1.2.1'],
    description='A CLI to manage AWS resources',
    long_description=long_description,
    packages=find_packages('lib'),
    platforms='any',
    license='MIT',
    scripts=['bin/acli'],
    package_dir={'': 'lib'},
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: System :: Networking',
    ],
    keywords=(
        'aws, Python, cli, amazon, ec2'
    ),
    tests_require=['requests>=2.7.0',
                   'pytest-cov>=2.2.0',
                   'pytest>=2.8.2',
                   'moto>=0.4.15',
                   'docopt>=0.6.2',
                   'boto3>=1.1.4',
                   'terminaltables>=1.2.1',
                   'colorclass==1.2.0',
                   'matplotlib>=1.4.3'],
    cmdclass={'test': PyTest},
)
