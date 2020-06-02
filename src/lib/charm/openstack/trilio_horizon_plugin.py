# Copyright 2020 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import charmhelpers.contrib.openstack.utils as os_utils

import charms_openstack.charm
import charms_openstack.plugins

# select the default release function
charms_openstack.charm.use_defaults('charm.default-select-release')

HORIZON_PATH = "/usr/share/openstack-dashboard"
MANAGE_PY = os.path.join(HORIZON_PATH, "manage.py")


class TrilioHorizonPluginQueensCharm(
    charms_openstack.plugins.TrilioVaultSubordinateCharm
):

    service_name = name = "trilio-horizon-plugin"

    release = "queens"

    required_relations = []

    packages = ["python-workloadmgrclient", "tvault-horizon-plugin"]

    # Setting an empty source_config_key activates special handling of release
    # selection suitable for subordinate charms
    source_config_key = ''

    # Use openstack-dashboard package to drive OpenStack Release versioning.
    release_pkg = "openstack-dashboard"
    package_codenames = os_utils.PACKAGE_CODENAMES

    @property
    def version_package(self):
        return self.packages[-1]


class TrilioHorizonPluginCharm(TrilioHorizonPluginQueensCharm):

    release = "rocky"

    packages = ["python3-workloadmgrclient", "python3-tvault-horizon-plugin"]
