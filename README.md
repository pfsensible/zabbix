# pfsensible.zabbix

This is a set of modules to allow you to configure Zabbix on pfSense firewalls with ansible.

## Installation using ansible galaxy

To install:

```
ansible-galaxy collection install pfsensible.zabbix
```

Optionally, you can specify the path of the collection installation with the `-p` option.

```
ansible-galaxy collection install pfsensible.zabbix -p ./collections
```

Additionally, you can set the `collections_paths` option in your `ansible.cfg` file to automatically designate install locations.

```ini
# ansible.cfg
[defaults]
collections_paths=collections
```

## Configuration

Current versions of ansible should automatically detect the version of Python on the pfSense system.  If Python discovery fails, you can set
ansible_python_interpreter in your playbook or hosts vars, e.g. for pfSense 2.7.2:

```
ansible_python_interpreter: /usr/local/bin/python3.11
```

Modules must run as root in order to make changes to the system.  By default pfSense does not have sudo capability so `become` will not work.  You can install it with:
```
  - name: "Install packages"
    package:
      name:
        - pfSense-pkg-sudo
      state: present
```
and then configure sudo so that your user has permission to use sudo.

This package assumes that the Zabbix agent package has been installed.  This can be any version of the package, e.g.:
```
  - name: "Install Zabbix agent"
    package:
      name:
        - pfSense-pkg-zabbix-agent7
      state: present
```

## Modules
The following modules are currently available:

* [pfsense_zabbix_agent](https://github.com/pfsensible/zabbix/wiki/pfsense_zabbix_agent) for Zabbix agent

## Operation

Modules in the collection work by editing `/cf/conf/config.xml` using xml.etree.ElementTree, then
calling the appropriate PHP update function via the pfSense PHP developer shell.

Some formatting is lost, and CDATA items are converted to normal entries,
but so far no problems with that have been noted.

## Writing new modules

See [GENERATING_MODULES](https://github.com/pfsensible/core/blob/master/GENERATING_MODULES.md) for instructions on how to use the
pfensible-generate-module script to automate the task writing basic pfsensible modules.

## License

GPLv3.0 or later
