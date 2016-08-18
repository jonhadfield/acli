acli
========

[![Build Status](https://travis-ci.org/jonhadfield/acli.svg?branch=master)](https://travis-ci.org/jonhadfield/acli)

acli is a simple CLI for querying and managing AWS services, written in Python using the [boto3](http://aws.amazon.com/sdk-for-python/ "boto3") SDK and [terminaltables](https://github.com/Robpol86/terminaltables "terminal tables") libraries.

Please submit any issues encountered.

Latest changes ([changelog](https://github.com/jonhadfield/acli/blob/master/CHANGELOG.md "Changelog"))
------------

0.1.30 (18th August 2016)

- Embed Six (remove external dependency)
- Python 3 compatibility for S3

0.1.29 (29th July 2016)

- Move s3 owner information to s3 info
- Python 3 compatibility
- Minor fixes

0.1.28 (25th July 2016)

- Add s3 owner information

0.1.27 (25th July 2016)

- Broken

0.1.26 (24th July 2016)

- Add basic support for EFS
- Minor fixes

0.1.25 (23rd July 2016)

- Correct ec2 instance counts
- Fix python 3 compatibility
- Fix output issues with s3 and ec2
- Upgrade dependencies  

0.1.24 (5th April 2016)

- Improve permission checks to prevent false negatives
- Minor fixes


Installation
------------
Simple:

    sudo pip install acli

Latest (from source):

    git clone git@github.com:jonhadfield/acli.git
    sudo python setup.py install

Setup
-----

Using the boto3 library means that credentials will be retrieved from the standard locations: http://boto3.readthedocs.org/en/latest/guide/configuration.html#configuration-files

Alternatively, you can specify them on the command line (see -h option for details).


Usage
-----
To see available services and commands, run:

    acli -h


Examples
--------
List ec2 instances in the account matching:

    acli ec2 list

View information on an instance:

    acli ec2 info i-12ab3c45

List contents of an S3 bucket:

    acli s3 list my_bucket

License
-------
MIT
