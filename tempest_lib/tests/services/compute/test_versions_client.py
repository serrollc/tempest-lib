# Copyright 2015 NEC Corporation.  All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import copy
from oslotest import mockpatch

from tempest_lib.services.compute import versions_client
from tempest_lib.tests import fake_auth_provider
from tempest_lib.tests.services.compute import base


class TestVersionsClient(base.BaseComputeServiceTest):

    FAKE_INIT_VERSION = {
        "version": {
            "id": "v2.1",
            "links": [
                {
                    "href": "http://openstack.example.com/v2.1/",
                    "rel": "self"
                },
                {
                    "href": "http://docs.openstack.org/",
                    "rel": "describedby",
                    "type": "text/html"
                }
            ],
            "status": "CURRENT",
            "updated": "2013-07-23T11:33:21Z",
            "version": "2.1",
            "min_version": "2.1"
            }
        }

    FAKE_VERSIONS_INFO = {
        "versions": [FAKE_INIT_VERSION["version"]]
        }

    FAKE_VERSION_INFO = copy.deepcopy(FAKE_INIT_VERSION)

    FAKE_VERSION_INFO["version"]["media-types"] = [
        {
            "base": "application/json",
            "type": "application/vnd.openstack.compute+json;version=2.1"
        }
        ]

    def setUp(self):
        super(TestVersionsClient, self).setUp()
        fake_auth = fake_auth_provider.FakeAuthProvider()
        self.versions_client = (
            versions_client.VersionsClient
            (fake_auth, 'compute', 'regionOne'))

    def _test_versions_client(self, bytes_body=False):
        self.check_service_client_function(
            self.versions_client.list_versions,
            'tempest_lib.common.rest_client.RestClient.raw_request',
            self.FAKE_VERSIONS_INFO,
            bytes_body,
            200)

    def _test_get_version_by_url(self, bytes_body=False):
        self.useFixture(mockpatch.Patch(
            "tempest_lib.common.rest_client.RestClient.token",
            return_value="Dummy Token"))
        params = {"version_url": self.versions_client._get_base_version_url()}
        self.check_service_client_function(
            self.versions_client.get_version_by_url,
            'tempest_lib.common.rest_client.RestClient.raw_request',
            self.FAKE_VERSION_INFO,
            bytes_body,
            200, **params)

    def test_list_versions_client_with_str_body(self):
        self._test_versions_client()

    def test_list_versions_client_with_bytes_body(self):
        self._test_versions_client(bytes_body=True)

    def test_get_version_by_url_with_str_body(self):
        self._test_get_version_by_url()

    def test_get_version_by_url_with_bytes_body(self):
        self._test_get_version_by_url(bytes_body=True)
