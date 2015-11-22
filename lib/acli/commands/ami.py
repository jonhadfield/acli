# -*- coding: utf-8 -*-
"""Usage:
    acli ami (ls | list)
    acli ami info <ami_id>

    -h, --help
"""
from __future__ import (absolute_import, print_function, unicode_literals)
from docopt import docopt

if __name__ == '__main__':
    print(docopt(__doc__))
