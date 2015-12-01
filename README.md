acli
========

[![Build Status](https://travis-ci.org/jonhadfield/acli.svg?branch=master)](https://travis-ci.org/jonhadfield/acli)

acli is a simple CLI for querying and managing AWS services, written in Python using the [boto3](http://aws.amazon.com/sdk-for-python/ "boto3") SDK and [terminaltables](https://github.com/Robpol86/terminaltables "terminal tables") libraries.

Please submit any issues encountered.

Latest changes ([changelog](https://github.com/jonhadfield/acli/blob/master/CHANGELOG.md "Changelog"))
------------
0.1.21 (1st December 2015)

- Show instance counts in output for 'acli ec2 summary'

- Add filtering/searching on AMI lists

    `example: acli ami ls --filter=webserver`


0.1.20 (29th November 2015)

- Added ability to delete keys from S3

    `example: acli s3 rm mybucket/myfolder/mykey.txt`

- Added filtering/searching on ec2 instance lists

    `example: acli ec2 ls --filter=nginx`

- Added functions for cleaning up orphaned snapshots and unnamed and unattached volumes. (first run with --noop to check what will be removed.)

    `example: acli clean delete_orphaned_snapshots --noop`

- Added bash completion script to allow tab completion of commands
- Other minor fixes

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
