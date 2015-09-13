from __future__ import (absolute_import, print_function)
import ConfigParser


class Config(object):
    def __init__(self):
        self.access_key_id = None
        self.secret_access_key = None
        self.region = None

    def load_config(self, arguments):
        aws_config = Config()
        cli_aws_region = arguments.get('--region')
        cli_access_key_id = arguments.get('--access_key_id')
        cli_secret_access_key = arguments.get('--secret_access_key')
        if cli_aws_region:
            self.region = cli_aws_region
        if cli_access_key_id:
            self.access_key_id = cli_access_key_id
        if cli_secret_access_key:
            self.secret_access_key = cli_secret_access_key
        return aws_config

    def from_file(self):
        config_parser = ConfigParser.RawConfigParser()
        config_parser.read('acli.cfg')
        file_aws_access_key_id = config_parser.get('main', 'aws_access_key_id')
        file_aws_secret_access_key_id = config_parser.get('main', 'aws_secret_access_key')
        if file_aws_access_key_id:
            self.access_key_id = file_aws_access_key_id
        if file_aws_secret_access_key_id:
            self.secret_access_key = file_aws_secret_access_key_id



