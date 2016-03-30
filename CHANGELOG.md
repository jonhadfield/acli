CHANGELOG
---------
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

0.1.20 (29th November 2015)

- Added ability to delete keys from S3

    `example: acli s3 rm mybucket/myfolder/mykey.txt`

- Added filtering/searching on ec2 instance lists

    `example: acli ec2 ls --filter=nginx`

- Added functions for cleaning up orphaned snapshots and unnamed and unattached volumes. (first run with --noop to check what will be removed.)

    `example: acli clean delete_orphaned_snapshots --noop`

- Added bash completion script to allow tab completion of commands
- Other minor fixes

0.1.18 (25th November 2015)

- Add initial support for Amazon ElasticSearch
- Minor output improvements and refactoring

0.1.17 (22nd November 2015)

- Allow use of ls instead of list for the various services
- Only transfer between local and S3 if files differ
