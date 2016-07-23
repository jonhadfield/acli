acli
========

[![Build Status](https://travis-ci.org/jonhadfield/acli.svg?branch=master)](https://travis-ci.org/jonhadfield/acli)

acli is a simple CLI for querying and managing AWS services, written in Python using the [boto3](http://aws.amazon.com/sdk-for-python/ "boto3") SDK and [terminaltables](https://github.com/Robpol86/terminaltables "terminal tables") libraries.

Please submit any issues encountered.

Latest changes ([changelog](https://github.com/jonhadfield/acli/blob/master/CHANGELOG.md "Changelog"))
------------

0.1.25 (23rd July 2016)

- Correct ec2 instance counts
- Fix python 3 compatibility
- Fix output issues with s3 and ec2
- Upgrade dependencies  

0.1.24 (5th April 2016)

- Improve permission checks to prevent false negatives
- Minor fixes

0.1.23 (30th March 2016)

- Make it work with Python 2.6
- Properly report a lack of (matching) AMIs
- Let 'ls' option work for ami listing
- Fail nicely if S3 directory transfer attempted (not able to sync dirs yet)
- Check instance has tags before trying to filter on them


0.1.21 (1st December 2015)

- Show instance counts in output for 'acli ec2 summary'
- Add filtering/searching on AMI lists

    `example: acli ami ls --filter=webserver`


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
