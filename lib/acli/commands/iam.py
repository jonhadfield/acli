# -*- coding: utf-8 -*-
"""Usage:
    acli iam summary
    acli iam user (ls | list) [options]
    acli iam user info <username>

    -o, --output=<output_type>      table, json, yaml or graph [default: table].
    -h, --help
"""
from __future__ import (absolute_import, print_function, unicode_literals)
from docopt import docopt

if __name__ == '__main__':
    print(docopt(__doc__))
