# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Orion Poplawski <orion@nwra.com>
# Copyright: (c) 2019, Frederic Bor <frederic.bor@wanadoo.fr>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
import base64
import re
from ansible_collections.pfsensible.core.plugins.module_utils.module_base import PFSenseModuleBase

ZABBIX_AGENT_ARGUMENT_SPEC = dict(
    hostname=dict(required=True, type='str'),
    server=dict(required=True, type='str'),
    serveractive=dict(required=True, type='str'),
    listenip=dict(type='str', default='0.0.0.0'),
    listenport=dict(type='int', default=10050),
    refreshactchecks=dict(type='int', default=120),
    timeout=dict(type='int', default=3),
    buffersend=dict(type='int', default=5),
    buffersize=dict(type='int', default=100),
    startagents=dict(type='int', default=3),
    tlsconnect=dict(default='unencrypted', choices=['unencrypted', 'psk', 'cert']),
    tlsaccept=dict(type=list, default=['unencrypted'], choices=['unencrypted', 'psk', 'cert']),
    tlscafile=dict(type='str', default='none'),
    tlscaos=dict(type='bool', default=False),
    tlscrlfile=dict(type='str', default='none'),
    tlscertfile=dict(type='str', default='none'),
    tlspskidentity=dict(type='str', default=''),
    tlspskfile=dict(type='str', default=''),
    userparams=dict(type='str', default=''),
    enabled=dict(type='bool', default=False),
)


class PFSenseZabbixAgentModule(PFSenseModuleBase):
    """ module managing pfsense zabbix-agent configuration """

    @staticmethod
    def get_argument_spec():
        """ return argument spec """
        return ZABBIX_AGENT_ARGUMENT_SPEC

    ##############################
    # init
    #
    def __init__(self, module, pfsense=None):
        super(PFSenseZabbixAgentModule, self).__init__(module, pfsense)
        self.name = "pfsense_zabbix_agent"
        self.obj = dict()

        # pkgs_elt = self.pfsense.get_element('installedpackages')
        # if pkgs_elt is None:
        # The zabbixagentlts element is not created on package install
        self.root_elt = self.pfsense.get_element('installedpackages')
        if self.root_elt is None:
            self.module.fail_json(msg='Unable to find installed packages configuration entry. Are you sure zabbix-agent is installed?')
        # zabbixagent_elt = pkgs_elt.find('zabbixagentlts')
        # if zabbixagent_elt is None:
        #     zabbixagent_elt = self.pfsense.new_element('zabbixagentlts')
        #     pkgs_elt.append(zabbixagent_elt)
        # self.root_elt = zabbixagent_elt.find('config')
        # if self.root_elt is None:
        #     self.root_elt = self.pfsense.new_element('config')
        #     zabbixagent_elt.append(self.root_elt)

    ##############################
    # params processing
    #
    def _params_to_obj(self):
        """ return a dict from module params """
        obj = dict()
        for key in self.params.keys():
            if key == 'enabled':
                self._get_ansible_param_bool(obj, key, fname='agentenabled', value='on', force=True)
            elif key == 'tlsaccept':
                obj[key] = ','.join(self.params[key])
            elif key == 'tlscaos':
                self._get_ansible_param_bool(obj, key, value='on', force=True)
            else:
                self._get_ansible_param(obj, key)

        return dict(config=obj)

    def _validate_params(self):
        """ do some extra checks on input parameters """

    ##############################
    # XML processing
    #
    def _copy_and_add_target(self):
        """ create the XML target_elt """
        self.pfsense.copy_dict_to_element(self.obj, self.target_elt)
        self.diff['after'] = self.obj.copy()
        self.root_elt.append(self.target_elt)

    def _copy_and_update_target(self):
        """ update the XML target_elt """
        before = self.pfsense.element_to_dict(self.target_elt)
        self.diff['before'] = before.copy()
        changed = self.pfsense.copy_dict_to_element(self.obj, self.target_elt)
        self.diff['after'] = self.pfsense.element_to_dict(self.target_elt)
        if self._remove_deleted_params():
            changed = True

        return (before, changed)

    def _create_target(self):
        """ create the XML target_elt """
        zabbix_elt = self.pfsense.new_element('zabbixagentlts')
        zabbix_elt.append(self.pfsense.new_element('config'))

        return zabbix_elt

    def _find_target(self):
        """ find the XML target_elt """
        result = self.root_elt.findall("./zabbixagentlts")
        if len(result) == 1:
            return result[0]
        elif len(result) > 1:
            self.module.fail_json(msg='Found multiple zabbix-agent configs.')
        else:
            return None

    ##############################
    # run
    #
    def run(self, params):
        """ process input params to add/update/delete """
        self.params = params
        self.target_elt = None
        self._check_deprecated_params()
        self._check_onward_params()
        self._validate_params()

        self.obj = self._params_to_obj()
        if self.target_elt is None:
            self.target_elt = self._find_target()

        self._add()

    def _update(self):
        """ make the target pfsense reload zabbix-agent """
        return self.pfsense.phpshell('''require_once("zabbix-agent.inc");
sync_package_zabbix_agent();''')

    ##############################
    # Logging
    #
    def _log_fields(self, before=None):
        """ generate pseudo-CLI command fields parameters to create an obj """
        values = ''
        if before is None:
            values += self.format_cli_field(self.params, 'hostname')
        else:
            values += self.format_updated_cli_field(self.obj, before, 'hostname', add_comma=(values))
        return values

    def _get_obj_name(self):
        """ return obj's name """
        return "'zabbixagent'"
