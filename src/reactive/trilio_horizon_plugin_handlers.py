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

import charms_openstack.charm as charm

# This charm's library contains all of the handler code associated with
# trilio_horizon_plugin
import charm.openstack.trilio_horizon_plugin as trilio_horizon_plugin  # noqa

charm.use_defaults("charm.installed", "config.changed", "update-status")
