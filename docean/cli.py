# -*- coding: utf-8 -*

"""Docean - command-line client for the DigitalOcean API v2

Usage:
    docean [options] ssh_keys add <name> <path>
    docean [options] ssh_keys delete <name>

Options:
    -h --help  Shows these lines.
    --access-token <access_token>
"""

import json
from functools import partial

from docopt import docopt
from booby import Model, fields
from finch import Session, Collection
from tornado import httpclient, ioloop


def main():
    args = _parse_args()

    print args

    if args['ssh_keys']:
        session = Session(
            httpclient.AsyncHTTPClient(),
            auth=DigitalOceanAuth(args['--access-token']))

        ssh_keys = SshKeys(session)

        if args['add']:
            name = args['<name>']
            public_key_path = args['<path>']

            print 'Adding ssh key', name, public_key_path

            with open(public_key_path) as public_key_file:
                ssh_key = SshKey(
                    name=name,
                    public_key=public_key_file.read())

            ssh_keys.add(ssh_key, _on_public_key_added)
            ioloop.IOLoop.instance().start()

        if args['delete']:
            name = args['<name>']

            print 'Deleting ssh key', name

            ssh_keys.all(partial(_delete_key, ssh_keys, name))
            ioloop.IOLoop.instance().start()



def _parse_args():
    return docopt(__doc__)


def _delete_key(ssh_keys, name, keys, error):
    if error is not None:
        raise error

    for key in keys:
        if key.name == name:
            ssh_keys.delete(SshKey(id=key.id), _on_deleted)
            print 'Bar'
            break
    else:
        print 'Key not found'
        ioloop.IOLoop.instance().stop()


def _on_deleted(error):
    ioloop.IOLoop.instance().stop()

    if error is not None:
        raise error

    print 'Key deleted'



def _on_public_key_added(ssh_key, error):
    ioloop.IOLoop.instance().stop()

    if error is not None:
        raise error

    print ssh_key


class SshKey(Model):
    id = fields.Field(primary=True)
    name = fields.Field()
    public_key = fields.Field()
    fingerprint = fields.Field()

    def decode(self, response):
        return json.loads(response.body)['ssh_key']


class SshKeys(Collection):
    model = SshKey
    url = 'https://api.digitalocean.com/v2/account/keys'

    def decode(self, response):
        return json.loads(response.body)['ssh_keys']


class DigitalOceanAuth(object):
    def __init__(self, access_token):
        self._access_token = access_token

    def __call__(self, request):
        request.headers['Authorization'] = 'Bearer {}'.format(self._access_token)
