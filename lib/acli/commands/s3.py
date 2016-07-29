# -*- coding: utf-8 -*-
"""Usage:
    acli s3 (ls | list) [<item>]
    acli s3 info [<item>]
    acli s3 cp <source> <dest>
    acli s3 (del | rm) <item>

    -o, --output=<output_type>      table, json, yaml or graph [default: table].
    -h, --help
"""
from __future__ import (absolute_import, print_function, unicode_literals)
from docopt import docopt

if __name__ == '__main__':
    print(docopt(__doc__))
