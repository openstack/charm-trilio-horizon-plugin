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

import collections
import os

import charmhelpers.core.hookenv as hookenv
import charmhelpers.fetch as fetch

import charms_openstack.charm


HORIZON_PATH = "/usr/share/openstack-dashboard"
MANAGE_PY = os.path.join(HORIZON_PATH, "manage.py")


class TrilioHorizonPluginQueensCharm(charms_openstack.charm.OpenStackCharm):

    service_name = name = "trilio-horizon-plugin"

    release = "queens"

    required_relations = []

    package_codenames = {
        "tvault-horizon-plugin": collections.OrderedDict([
            ("3", "stein"),
            ("4", "train"),
        ]),
        "python3-horizon-plugin": collections.OrderedDict([
            ("3", "stein"),
            ("4", "train"),
        ]),
    }

    packages = ["python-workloadmgrclient", "tvault-horizon-plugin"]

    def configure_source(self):
        with open(
            "/etc/apt/sources.list.d/" "trilio-gemfury-sources.list", "w"
        ) as tsources:
            tsources.write(hookenv.config("triliovault-pkg-source"))
        fetch.apt_update(fatal=True)

    @property
    def version_package(self):
        return self.packages[-1]

    def install(self):
        self.configure_source()
        super().install()

    def upgrade_charm(self):
        super().upgrade_charm()


class TrilioHorizonPluginCharm(TrilioHorizonPluginQueensCharm):

    release = "rocky"

    packages = ["python3-workloadmgrclient", "python3-tvault-horizon-plugin"]
