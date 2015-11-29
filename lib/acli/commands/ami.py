# -*- coding: utf-8 -*-
"""Usage:
    acli ami (ls | list) [options]
    acli ami info <ami_id>

    -f, --filter=<term>             filter results by term
    -h, --help
"""
from __future__ import (absolute_import, print_function, unicode_literals)
from docopt import docopt

if __name__ == '__main__':
    print(docopt(__doc__))
