# -*- coding: utf-8 -*-
"""Usage:
    acli clean (delete_orphaned_snapshots | delete_unnamed_volumes) [options]

    -n, --noop      Don't run but show what would be changed.
    -h, --help
"""
from __future__ import (absolute_import, print_function, unicode_literals)
from docopt import docopt

if __name__ == '__main__':
    print(docopt(__doc__))
