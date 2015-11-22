# -*- coding: utf-8 -*-
"""Usage:
    acli lc (ls | list) [options]
    acli lc info <lc_name> [options]

    -h, --help
"""
from __future__ import (absolute_import, print_function, unicode_literals)
from docopt import docopt

if __name__ == '__main__':
    print(docopt(__doc__))
