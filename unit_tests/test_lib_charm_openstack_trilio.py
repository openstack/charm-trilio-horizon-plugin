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


import charm.openstack.trilio_horizon_plugin as trilio_horizon
import charms_openstack.test_utils as test_utils


class Helper(test_utils.PatchHelper):
    def setUp(self):
        super().setUp()
        self.patch_release(
            trilio_horizon.TrilioHorizonPluginCharmQueens42.release)
        self.patch_release(
            trilio_horizon.TrilioHorizonPluginCharmRocky42.release)


class TestTrilioHorizonCharm(Helper):

    def test_packages_queens(self):
        dm_charm = trilio_horizon.TrilioHorizonPluginCharmQueens42()
        self.assertEqual(
            dm_charm.packages,
            ["python-workloadmgrclient", "tvault-horizon-plugin"],
        )

    def test_packages_rocky(self):
        dm_charm = trilio_horizon.TrilioHorizonPluginCharmRocky42()
        self.assertEqual(
            dm_charm.packages,
            ["python3-workloadmgrclient", "python3-tvault-horizon-plugin"],
        )
