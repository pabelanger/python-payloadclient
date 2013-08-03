# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (C) 2013 PolyBeacon, Inc.
#
# Author: Paul Belanger <paul.belanger@polybeacon.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from cliff import lister
from cliff import show

from stripeclient.openstack.common import log as logging
from stripeclient.v1 import client

LOG = logging.getLogger(__name__)


class Add(show.ShowOne):

    def get_parser(self, prog_name):
        parser = super(Add, self).get_parser(prog_name)
        parser.add_argument('name', metavar='name', help='Queue name')
        parser.add_argument(
            '--description', type=str, default=None,
            help='(Default: None)'
        )
        parser.add_argument(
            '--disabled', type=bool, default=False,
            help='(Default: False)'
        )
        parser.add_argument(
            '--id', type=int, default=None,
            help='(Default: None)'
        )

        return parser

    def take_action(self, parsed_args):
        endpoint = 'http://localhost:9859'
        kwargs = {}
        self.http_client = client.Client(endpoint, **kwargs)
        json = {
            'id': parsed_args.id,
            'description': parsed_args.description,
            'disabled': parsed_args.disabled,
            'name': parsed_args.name,
        }

        data = self.http_client.queues.create(json)

        return zip(*sorted(data.items()))


class Show(lister.Lister):

    def take_action(self, parsed_args):
        endpoint = 'http://localhost:9859'
        kwargs = {}
        self.http_client = client.Client(endpoint, **kwargs)
        data = self.http_client.queues.get_all()

        columns = (
            'id',
            'name',
            'description',
            'disabled',
            'created_at',
            'updated_at',
        )

        res = ((
            q.id,
            q.name,
            q.description,
            q.disabled,
            q.created_at,
            q.updated_at,
        ) for q in data)

        return (columns, res)
