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

charms_openstack.plugins.trilio.make_trilio_handlers()

HORIZON_PATH = "/usr/share/openstack-dashboard"
MANAGE_PY = os.path.join(HORIZON_PATH, "manage.py")


class TrilioHorizonPluginBase(
    charms_openstack.plugins.TrilioVaultSubordinateCharm
):

    abstract_class = True

    service_name = name = "trilio-horizon-plugin"
    required_relations = []

    # Setting an empty source_config_key activates special handling of release
    # selection suitable for subordinate charms
    source_config_key = ''

    # Use openstack-dashboard package to drive OpenStack Release versioning.
    os_release_pkg = "openstack-dashboard"
    package_codenames = os_utils.PACKAGE_CODENAMES

    @classmethod
    def trilio_version_package(cls):
        return 'python3-tvault-horizon-plugin'

    def trilio_encryption_supported(self):
        return False

    def local_settings(self):
        settings = (
            "TRILIO_ENCRYPTION_SUPPORT = {}\n"
            "OPENSTACK_ENCRYPTION_SUPPORT = {}").format(
                self.trilio_encryption_supported(),
                self.config['openstack-encryption-support'])
        return settings


class TrilioHorizonPluginCharmQueens41(TrilioHorizonPluginBase):

    release = "queens"
    trilio_release = "4.1"
    packages = ["python-workloadmgrclient", "tvault-horizon-plugin"]


class TrilioHorizonPluginCharmQueens42(TrilioHorizonPluginBase):

    release = "queens"
    trilio_release = "4.2"
    packages = ["python-workloadmgrclient", "tvault-horizon-plugin"]

    def trilio_encryption_supported(self):
        return True


class TrilioHorizonPluginCharmRocky41(TrilioHorizonPluginCharmQueens41):

    release = "rocky"
    trilio_release = "4.1"
    packages = ["python3-workloadmgrclient", "python3-tvault-horizon-plugin"]


class TrilioHorizonPluginCharmRocky42(TrilioHorizonPluginCharmQueens42):

    release = "rocky"
    trilio_release = "4.2"
    packages = ["python3-workloadmgrclient", "python3-tvault-horizon-plugin"]
