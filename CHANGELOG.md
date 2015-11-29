CHANGELOG
---------

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
