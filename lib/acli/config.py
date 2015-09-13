from __future__ import (absolute_import, print_function)
import ConfigParser


class Config(object):
    def __init__(self, cli_args):
        self.access_key_id = None
        self.secret_access_key = None
        self.region = None
        self.config_loader(cli_args)

    def config_loader(self, cli_args):
        """ Load configuration from sources in order of precedence:
        CLI, ACLI_CONFIG, BOTO, ENV
        """
        self.from_cli(cli_args)
        self.from_acli_config_file()
        self.from_boto_file()
        self.from_env()

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

    def from_boto_file(self):
        pass

    def from_env(self):
        pass

    def from_acli_config_file(self):
        config_parser = ConfigParser.RawConfigParser()
        config_parser.read('acli.cfg')
        file_aws_access_key_id = config_parser.get('main', 'aws_access_key_id')
        file_aws_secret_access_key_id = config_parser.get('main', 'aws_secret_access_key')
        file_aws_region = config_parser.get('main', 'aws_region')

        if file_aws_access_key_id:
            self.access_key_id = file_aws_access_key_id
        if file_aws_secret_access_key_id:
            self.secret_access_key = file_aws_secret_access_key_id
        if file_aws_region:
            self.region = file_aws_region



