# -*- coding: utf-8 -*-
from __future__ import (absolute_import, print_function, unicode_literals)
import sys
import os
import platform
import base64
from contextlib import contextmanager
from botocore.exceptions import NoCredentialsError


@contextmanager
def cred_checked_iam_client(iam_client):
    try:
        assert iam_client.list_users()
        yield iam_client
    except NoCredentialsError:
        exit('No credentials found.')
    except Exception as e:
        exit('Unhanded exception: {0}'.format(e))


@contextmanager
def cred_checked_ec2_client(ec2_client):
    try:
        assert ec2_client.describe_account_attributes()
        yield ec2_client
    except NoCredentialsError:
        exit('No credentials found.')
    except Exception as e:
        exit('Unhanded exception: {0}'.format(e))


@contextmanager
def cred_checked_elb_client(elb_client):
    try:
        assert elb_client.describe_load_balancers()
        yield elb_client
    except NoCredentialsError:
        exit('No credentials found.')
    except Exception as e:
        exit('Unhanded exception: {0}'.format(e))

BASH_COMPLETION_SCRIPT = "Cl9hY2xpKCkKewogICAgbG9jYWwgY3VyCiAgICBjdXI9IiR7Q09NUF9XT1JEU1tDT01QX0NXT1JEXX0iCgogICAgaWYgWyAkQ09NUF9DV09SRCAtZXEgMSBdOyB0aGVuCiAgICAgICAgQ09NUFJFUExZPSggJCggY29tcGdlbiAtVyAnLS12ZXJzaW9uIC0taW5zdGFsbC1jb21wbGV0aW9uIGVsYiBhbWkgYWNjb3VudCBlYzInIC0tICRjdXIpICkKICAgIGVsc2UKICAgICAgICBjYXNlICR7Q09NUF9XT1JEU1sxXX0gaW4KICAgICAgICAgICAgZWxiKQogICAgICAgICAgICBfYWNsaV9lbGIKICAgICAgICA7OwogICAgICAgICAgICBhbWkpCiAgICAgICAgICAgIF9hY2xpX2FtaQogICAgICAgIDs7CiAgICAgICAgICAgIGFjY291bnQpCiAgICAgICAgICAgIF9hY2xpX2FjY291bnQKICAgICAgICA7OwogICAgICAgICAgICBlYzIpCiAgICAgICAgICAgIF9hY2xpX2VjMgogICAgICAgIDs7CiAgICAgICAgZXNhYwoKICAgIGZpCn0KCl9hY2xpX2VsYigpCnsKICAgIGxvY2FsIGN1cgogICAgY3VyPSIke0NPTVBfV09SRFNbQ09NUF9DV09SRF19IgoKICAgIGlmIFsgJENPTVBfQ1dPUkQgLWVxIDIgXTsgdGhlbgogICAgICAgIENPTVBSRVBMWT0oICQoIGNvbXBnZW4gLVcgJyBpbmZvIGxpc3QnIC0tICRjdXIpICkKICAgIGVsc2UKICAgICAgICBjYXNlICR7Q09NUF9XT1JEU1syXX0gaW4KICAgICAgICAgICAgaW5mbykKICAgICAgICAgICAgX2FjbGlfZWxiX2luZm8KICAgICAgICA7OwogICAgICAgICAgICBsaXN0KQogICAgICAgICAgICBfYWNsaV9lbGJfbGlzdAogICAgICAgIDs7CiAgICAgICAgZXNhYwoKICAgIGZpCn0KCl9hY2xpX2VsYl9pbmZvKCkKewogICAgbG9jYWwgY3VyCiAgICBjdXI9IiR7Q09NUF9XT1JEU1tDT01QX0NXT1JEXX0iCgogICAgaWYgWyAkQ09NUF9DV09SRCAtZ2UgMyBdOyB0aGVuCiAgICAgICAgQ09NUFJFUExZPSggJCggY29tcGdlbiAtZlcgJyAnIC0tICRjdXIpICkKICAgIGZpCn0KCl9hY2xpX2VsYl9saXN0KCkKewogICAgbG9jYWwgY3VyCiAgICBjdXI9IiR7Q09NUF9XT1JEU1tDT01QX0NXT1JEXX0iCgogICAgaWYgWyAkQ09NUF9DV09SRCAtZ2UgMyBdOyB0aGVuCiAgICAgICAgQ09NUFJFUExZPSggJCggY29tcGdlbiAtVyAnICcgLS0gJGN1cikgKQogICAgZmkKfQoKX2FjbGlfYW1pKCkKewogICAgbG9jYWwgY3VyCiAgICBjdXI9IiR7Q09NUF9XT1JEU1tDT01QX0NXT1JEXX0iCgogICAgaWYgWyAkQ09NUF9DV09SRCAtZXEgMiBdOyB0aGVuCiAgICAgICAgQ09NUFJFUExZPSggJCggY29tcGdlbiAtVyAnIGluZm8gbGlzdCcgLS0gJGN1cikgKQogICAgZWxzZQogICAgICAgIGNhc2UgJHtDT01QX1dPUkRTWzJdfSBpbgogICAgICAgICAgICBpbmZvKQogICAgICAgICAgICBfYWNsaV9hbWlfaW5mbwogICAgICAgIDs7CiAgICAgICAgICAgIGxpc3QpCiAgICAgICAgICAgIF9hY2xpX2FtaV9saXN0CiAgICAgICAgOzsKICAgICAgICBlc2FjCgogICAgZmkKfQoKX2FjbGlfYW1pX2luZm8oKQp7CiAgICBsb2NhbCBjdXIKICAgIGN1cj0iJHtDT01QX1dPUkRTW0NPTVBfQ1dPUkRdfSIKCiAgICBpZiBbICRDT01QX0NXT1JEIC1nZSAzIF07IHRoZW4KICAgICAgICBDT01QUkVQTFk9KCAkKCBjb21wZ2VuIC1mVyAnICcgLS0gJGN1cikgKQogICAgZmkKfQoKX2FjbGlfYW1pX2xpc3QoKQp7CiAgICBsb2NhbCBjdXIKICAgIGN1cj0iJHtDT01QX1dPUkRTW0NPTVBfQ1dPUkRdfSIKCiAgICBpZiBbICRDT01QX0NXT1JEIC1nZSAzIF07IHRoZW4KICAgICAgICBDT01QUkVQTFk9KCAkKCBjb21wZ2VuIC1XICcgJyAtLSAkY3VyKSApCiAgICBmaQp9CgpfYWNsaV9hY2NvdW50KCkKewogICAgbG9jYWwgY3VyCiAgICBjdXI9IiR7Q09NUF9XT1JEU1tDT01QX0NXT1JEXX0iCgogICAgaWYgWyAkQ09NUF9DV09SRCAtZ2UgMiBdOyB0aGVuCiAgICAgICAgQ09NUFJFUExZPSggJCggY29tcGdlbiAtVyAnICcgLS0gJGN1cikgKQogICAgZmkKfQoKX2FjbGlfZWMyKCkKewogICAgbG9jYWwgY3VyCiAgICBjdXI9IiR7Q09NUF9XT1JEU1tDT01QX0NXT1JEXX0iCgogICAgaWYgWyAkQ09NUF9DV09SRCAtZXEgMiBdOyB0aGVuCiAgICAgICAgQ09NUFJFUExZPSggJCggY29tcGdlbiAtVyAnIGluZm8gc3RhdHMgbGlzdCcgLS0gJGN1cikgKQogICAgZWxzZQogICAgICAgIGNhc2UgJHtDT01QX1dPUkRTWzJdfSBpbgogICAgICAgICAgICBpbmZvKQogICAgICAgICAgICBfYWNsaV9lYzJfaW5mbwogICAgICAgIDs7CiAgICAgICAgICAgIHN0YXRzKQogICAgICAgICAgICBfYWNsaV9lYzJfc3RhdHMKICAgICAgICA7OwogICAgICAgICAgICBsaXN0KQogICAgICAgICAgICBfYWNsaV9lYzJfbGlzdAogICAgICAgIDs7CiAgICAgICAgZXNhYwoKICAgIGZpCn0KCl9hY2xpX2VjMl9pbmZvKCkKewogICAgbG9jYWwgY3VyCiAgICBjdXI9IiR7Q09NUF9XT1JEU1tDT01QX0NXT1JEXX0iCgogICAgaWYgWyAkQ09NUF9DV09SRCAtZ2UgMyBdOyB0aGVuCiAgICAgICAgQ09NUFJFUExZPSggJCggY29tcGdlbiAtZlcgJyAnIC0tICRjdXIpICkKICAgIGZpCn0KCl9hY2xpX2VjMl9zdGF0cygpCnsKICAgIGxvY2FsIGN1cgogICAgY3VyPSIke0NPTVBfV09SRFNbQ09NUF9DV09SRF19IgoKICAgIGlmIFsgJENPTVBfQ1dPUkQgLWdlIDMgXTsgdGhlbgogICAgICAgIENPTVBSRVBMWT0oICQoIGNvbXBnZW4gLWZXICcgJyAtLSAkY3VyKSApCiAgICBmaQp9CgpfYWNsaV9lYzJfbGlzdCgpCnsKICAgIGxvY2FsIGN1cgogICAgY3VyPSIke0NPTVBfV09SRFNbQ09NUF9DV09SRF19IgoKICAgIGlmIFsgJENPTVBfQ1dPUkQgLWdlIDMgXTsgdGhlbgogICAgICAgIENPTVBSRVBMWT0oICQoIGNvbXBnZW4gLVcgJyAnIC0tICRjdXIpICkKICAgIGZpCn0KCmNvbXBsZXRlIC1GIF9hY2xpIGFjbGk="
BASH_COMPLETION_PATH_OSX = "/usr/local/etc/bash_completion.d"
BASH_COMPLETION_PATH_LINUX = "/etc/bash_completion.d"


def install_completion():
    if platform.system() == 'Darwin':
        if os.path.exists(BASH_COMPLETION_PATH_OSX):
            with open("{0}/acli".format(BASH_COMPLETION_PATH_OSX), 'w') as acli_file:
                acli_file.write(base64.b64decode(BASH_COMPLETION_SCRIPT))
            sys.exit("bash completion script written to: {0}/acli\nrestart terminal to use.".format(
                BASH_COMPLETION_PATH_OSX)
            )
        else:
            sys.exit("bash completion not installed. try 'brew install bash-completion'.")
    elif platform.system() == 'Linux':
        if os.path.exists(BASH_COMPLETION_PATH_LINUX):
            with open("{0}/acli".format(BASH_COMPLETION_PATH_LINUX), 'w') as acli_file:
                acli_file.write(base64.b64decode(BASH_COMPLETION_SCRIPT))
            sys.exit("bash completion script written to: {0}/acli\nrestart terminal to use.".format(
                BASH_COMPLETION_PATH_LINUX)
            )
        else:
            sys.exit("bash completion not installed.")

    else:
        sys.exit("Shell completion only available on Linux and OS X.")
