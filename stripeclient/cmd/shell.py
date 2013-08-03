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

import sys

from cliff import app
from cliff import commandmanager

from stripeclient.openstack.common import log as logging
from stripeclient import version

LOG = logging.getLogger(__name__)


class Shell(app.App):

    def __init__(self):
        super(Shell, self).__init__(
            description='Stripe client', version=version.VERSION_INFO,
            command_manager=commandmanager.CommandManager('stripe.shell'),
        )


def main(argv=sys.argv[1:]):
    return Shell().run(argv)
