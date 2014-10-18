# -*- coding: utf-8 -*

"""Docean - command-line client for the DigitalOcean API v2

Usage:
    docean [options] ssh_keys add <path>
    docean [options] ssh_keys delete <id>

Options:
    -h --help  Shows these lines.
    --access-token <access_token>
"""

from docopt import docopt


def main():
    args = _parse_args()

    if args['ssh_keys']:
        if args['add']:
            print 'Adding ssh key', args['<path>']

        if args['delete']:
            print 'Deleting ssh key', args['<id>']


def _parse_args():
    return docopt(__doc__)
