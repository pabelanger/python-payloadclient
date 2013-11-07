# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 OpenStack LLC.
# Copyright (C) 2013 PolyBeacon, Inc.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from keystoneclient.v2_0 import client as ksclient

from payloadclient.openstack.common import importutils


def _get_ksclient(**kwargs):
    """Get an endpoint and auth token from Keystone.

    :param kwargs: keyword args containing credentials:
            * username: name of user
            * password: user's password
            * auth_url: endpoint to authenticate against
            * cacert: path of CA TLS certificate
            * insecure: allow insecure SSL (no cert verification)
            * tenant_{name|id}: name or ID of tenant
    """
    return ksclient.Client(username=kwargs.get('username'),
                           password=kwargs.get('password'),
                           tenant_id=kwargs.get('tenant_id'),
                           tenant_name=kwargs.get('tenant_name'),
                           auth_url=kwargs.get('auth_url'),
                           region_name=kwargs.get('region_name'),
                           cacert=kwargs.get('cacert'),
                           insecure=kwargs.get('insecure'))


def get_client(api_version, **kwargs):
    endpoint = kwargs.get('payload_url')
    if kwargs.get('ksp_auth_token') and kwargs.get('payload_url'):
        token = kwargs.get('ksp_auth_token')
    elif (kwargs.get('ksp_username') and
            kwargs.get('ksp_password') and
            kwargs.get('ksp_auth_url') and
            (kwargs.get('ksp_tenant_id') or
                kwargs.get('ksp_tenant_name'))):

        ks_kwargs = {
            'username': kwargs.get('ksp_username'),
            'password': kwargs.get('ksp_password'),
            'tenant_id': kwargs.get('ksp_tenant_id'),
            'tenant_name': kwargs.get('ksp_tenant_name'),
            'auth_url': kwargs.get('ksp_auth_url'),
        }
        _ksclient = _get_ksclient(**ks_kwargs)
        token = _ksclient.auth_token

    cli_kwargs = {
        'token': token,
    }

    return Client(api_version, endpoint, **cli_kwargs)


def Client(version, *args, **kwargs):
    module = importutils.import_module('payloadclient.v1.client')
    client_class = getattr(module, 'Client')
    return client_class(*args, **kwargs)