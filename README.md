acli
========

[![Build Status](https://travis-ci.org/jonhadfield/acli.svg?branch=master)](https://travis-ci.org/jonhadfield/acli)

acli is a simple CLI for querying and managing AWS services, written in Python using the [boto3](http://aws.amazon.com/sdk-for-python/ "boto3") SDK and [terminaltables](https://github.com/Robpol86/terminaltables "terminal tables") library.

Whilst early in development, I'm focussing on reporting on the most common AWS services and then the most requested services.
Any and all feedback appreciated.

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

    acli --help


Examples
--------
List ec2 instances in the account:

    acli ec2 list

View information on an instance:

    acli ec2 info i-12ab3c45

List contents of an S3 bucket:

    acli s3 list my_bucket

License
-------
MIT
