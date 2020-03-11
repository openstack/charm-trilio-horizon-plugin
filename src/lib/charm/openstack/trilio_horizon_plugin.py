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
import glob
import os
import shutil
import subprocess

import charmhelpers.core.hookenv as hookenv
import charmhelpers.fetch as fetch

import charms_openstack.charm


HORIZON_PATH = "/usr/share/openstack-dashboard"
MANAGE_PY = os.path.join(HORIZON_PATH, "manage.py")


class TrilioHorizonPluginCharm(charms_openstack.charm.OpenStackCharm):

    service_name = name = "trilio-horizon-plugin"

    # First release supported
    release = "stein"

    required_relations = []

    package_codenames = {
        "tvault-horizon-plugin": collections.OrderedDict([("3", "stein")]),
        "python3-horizon-plugin": collections.OrderedDict([("3", "stein")]),
    }

    def configure_source(self):
        with open(
            "/etc/apt/sources.list.d/" "trilio-gemfury-sources.list", "w"
        ) as tsources:
            tsources.write(hookenv.config("triliovault-pkg-source"))
        fetch.apt_update(fatal=True)

    @property
    def packages(self):
        if hookenv.config("python-version") == 2:
            return ["python-workloadmgrclient", "tvault-horizon-plugin"]
        return ["python3-workloadmgrclient", "python3-tvault-horizon-plugin"]

    # TODO: drop once packaging is updated
    def install(self):
        self.configure_source()
        super().install()
        self.copy_files()
        self.collectstatic_and_compress()

    # TODO: drop once packaging is updated
    def upgrade_charm(self):
        super().upgrade_charm()
        self.copy_files()
        self.collectstatic_and_compress()

    # TODO: drop when package does this
    def copy_files(self):
        for panel in glob.glob("files/trilio/panels/*"):
            shutil.copy(
                panel,
                os.path.join(
                    HORIZON_PATH, "openstack_dashboard/local/enabled"
                ),
            )
        for templatetag in glob.glob("files/trilio/templatetags/*"):
            shutil.copy(
                templatetag,
                os.path.join(HORIZON_PATH, "openstack_dashboard/templatetags"),
            )
        for index_html in glob.glob(
            "/usr/lib/python*/**/workloads_admin/index.html", recursive=True
        ):
            shutil.copy(
                "files/trilio/templates/workload_admin/index.html",
                index_html,
            )

    # TODO: drop when package does this
    def collectstatic_and_compress(self):
        python = "/usr/bin/python{}".format(hookenv.config("python-version"))
        subprocess.check_call([python, MANAGE_PY, "collectstatic", "--noinput"])
        subprocess.check_call([python, MANAGE_PY, "compress", "--force"])
