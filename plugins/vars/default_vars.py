# -*- coding: utf-8 -*-
# (c) 2014, Craig Tracey <craigtracey@gmail.com>
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

import collections
import yaml

from ansible.constants import DEFAULTS, get_config, load_config_file

import ansible.errors as errors
import ansible.inventory as inventory
import ansible.utils as utils


def deep_update_dict(d, u):
    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            r = deep_update_dict(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


class VarsModule(object):

    def __init__(self, inventory):
        self.inventory = inventory
        self.inventory_basedir = inventory.basedir()

    def _get_defaults(self):
        p = load_config_file()
        defaults_file = get_config(p, DEFAULTS, 'var_defaults_file',
                                   'ANSIBLE_VAR_DEFAULTS_FILE', None)
        if defaults_file:
            return yaml.load(open(defaults_file))

    def run(self, host, vault_password=None):
        default_vars = self._get_defaults()
        group_vars = host.get_variables()
        if default_vars:
            return deep_update_dict(default_vars, group_vars)
        return group_vars
