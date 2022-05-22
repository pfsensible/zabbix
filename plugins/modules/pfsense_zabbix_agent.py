#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021-2022, Orion Poplawski <orion@nwra.com>
# Copyright: (c) 2019, Frederic Bor <frederic.bor@wanadoo.fr>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: pfsense_zabbix_agent
short_description: Manage pfSense zabbix-agent configuration
description:
  - Manage pfSense zabbix-agent configuration.
version_added: "0.1.0"
author: "Orion Poplawski (@opoplawski)"
options:
  hostname:
    description: The hostname of the agent.
    required: true
    type: str
  server:
    description: The hostname or IP address of the zabbix server.
    required: true
    type: str
  serveractive:
    description: The hostname or IP address of the zabbix server for active checks.
    required: false
    type: str
  listenip:
    description: The IP address for the agent to listen on.
    required: false
    default: 0.0.0.0
    type: str
  listenport:
    description: The port for the agent to listen on.
    required: false
    default: 10050
    type: int
  refreshactchecks:
    description: The agent will refresh list of active checks once per this number of seconds.
    required: false
    default: 120
    type: int
  timeout:
    description: Do not spend more than this many seconds on getting requested value.
    required: false
    default: 3
    type: int
  buffersend:
    description: Do not keep data longer than this many seconds in buffer.
    required: false
    default: 5
    type: int
  buffersize:
    description: Maximum number of values in the memory buffer. The agent will send all collected data to Zabbix server or proxy if the buffer is full.
    required: false
    default: 100
    type: int
  startagents:
    description: Number of pre-forked instances of zabbix_agentd that process passive checks.
    required: false
    default: 3
    type: int
  tlsconnect:
    description: How the agent should connect to server or proxy. Used for active checks.
    required: false
    choices: ['unencrypted', 'psk', 'cert']
    default: unencrypted
    type: str
  tlsaccept:
    description: What incoming connections to accept.
    required: false
    choices: ['unencrypted', 'psk', 'cert']
    default: [unencrypted]
    type: list
  tlscafile:
    description: Top-level CA certificate for peer certificate verification.
    required: false
    default: none
    type: str
  tlscaos:
    description: Use the CA certificate list from the operating system.
    required: false
    default: false
    type: bool
  tlscrlfile:
    description: Certificate revocation list.
    required: false
    default: none
    type: str
  tlscertfile:
    description: Agent certificate.
    required: false
    default: none
    type: str
  tlspskidentity:
    description: Unique, case sensitive string used to identify the pre-shared key.
    required: false
    default: ''
    type: str
  tlspskfile:
    description: Pre-shared key.
    required: false
    default: ''
    type: str
  userparams:
    description: User parameters
    required: false
    default: ''
    type: str
  enabled:
    description: Enable or disable zabbix-agent.
    default: false
    type: bool
notes:
requirements:
  - pfsensible.core >= 0.4.0
'''

EXAMPLES = r'''
- name: Configure Zabbix agent
  pfsense_zabbix_agent:
    enabled: yes
    hostname: "{{ ansible_nodename }}"
    server: "{{ zabbix_server }}"
    serveractive: "{{ zabbix_server }}"
    listenip: "{{ ansible_igb0.ipv4[0].address if ansible_igb0 is defined else ansible_ix0.ipv4[0].address }}"
  become: yes
'''

RETURN = r'''
commands:
    description: the set of commands that would be pushed to the remote device (if pfSense had a CLI)
    returned: always
    type: list
    sample: ["create zabbix_agent 'hostname=myfirewall'"]
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.pfsensible.zabbix.plugins.module_utils.zabbix_agent import PFSenseZabbixAgentModule, ZABBIX_AGENT_ARGUMENT_SPEC


def main():
    module = AnsibleModule(
        argument_spec=ZABBIX_AGENT_ARGUMENT_SPEC,
        supports_check_mode=True)

    pfmodule = PFSenseZabbixAgentModule(module)
    pfmodule.run(module.params)
    pfmodule.commit_changes()


if __name__ == '__main__':
    main()
