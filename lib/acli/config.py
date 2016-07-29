# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
try:
    import configparser
except ImportError:
    from external.six.moves import configparser
import os


class Config(object):
    def __init__(self, cli_args):
        self.access_key_id = None
        self.secret_access_key = None
        self.region = None
        self.config_loader(cli_args)

    def is_config_loaded(self):
        if self.access_key_id and self.secret_access_key and self.region:
            return True

    def config_loader(self, cli_args):
        """ Load configuration from sources in order of precedence:
        CLI, ENV, BOTO
        """
        self.from_cli(cli_args)
        self.load_acli_config()

    def from_cli(self, cli_args):
        cli_aws_region = cli_args.get('--region')
        cli_access_key_id = cli_args.get('--access_key_id')
        cli_secret_access_key = cli_args.get('--secret_access_key')
        if cli_aws_region:
            self.region = cli_aws_region
        if cli_access_key_id:
            self.access_key_id = cli_access_key_id
        if cli_secret_access_key:
            self.secret_access_key = cli_secret_access_key

    @staticmethod
    def load_acli_config():
        if os.path.isfile('acli.cfg'):
            configparser.read('acli.cfg')
