# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)

from botocore.exceptions import ClientError

from acli.connections import get_client
from acli.errors import handle_boto_errors
from acli.output.es import (output_domain_list, output_domain_info)


@handle_boto_errors
def es_list(aws_config=None):
    """
    @type aws_config: Config
    """
    es_client = get_client(client_type='es', config=aws_config)
    domains = es_client.list_domain_names()
    domain_names = domains.get('DomainNames')
    if domain_names:
        output_domain_list(domains=domain_names)
    else:
        exit("No domains found.")


@handle_boto_errors
def es_info(aws_config=None, domain_name=None):
    """
    @type aws_config: Config
    @type domain_name: unicode
    """
    es_client = get_client(client_type='es', config=aws_config)
    try:
        domain = es_client.describe_elasticsearch_domains(DomainNames=[domain_name])
        output_domain_info(domain=domain)
    except (ClientError, IndexError):
        exit("Cannot find domain: {0}".format(domain_name))
