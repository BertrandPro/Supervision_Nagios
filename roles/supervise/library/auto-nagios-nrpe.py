#!/usr/bin/python

# Copyright: (c) 2020, Your Name <YourName@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: auto_nagios_nrpe

short_description: Auto configure nrpe.cfg

version_added: "0.0.2"

description:  Module qui modifie le fichier nrpe.cfg d'un serveur à superviser. 

options:
    ip_nagios:
        description: addresse ip (ou host si DNS) du serveur nagios.
        required: true
        type: str
    request:
        description: This is the message to send to the test module.
        required: true
        type: str
author:
    - BertrandBZH (bertrand.pro@gmail.com)
'''

EXAMPLES = r'''
- name: Config auto nrpe
  auto_nagios_nrpe:
    ip_nagios: "192.168.1.49"
    request: "toto"
'''

RETURN = r'''
    result:
       description : return toto
'''

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(
            ip_nagios=dict(required=False, type='str'),
            request=dict(required=False, type='str'),
        )
    )

    ip_nagios_local = module.params.get('ip_nagios')
    request_local = module.params.get('request')


    indicateurs = """# supervision Auto-Nagios : ajout des commandS argument\n
    command[check_load]=/usr/lib/nagios/plugins/check_load -r -w .15,.10,.05 -c .30,.25,.20
    command[check_procs]=/usr/lib/nagios/plugins/check_procs -w 150 -c 200
    command[check_users]=/usr/lib/nagios/plugins/check_users -w 2 -c 5
    command[check_disk]=/usr/lib/nagios/plugins/check_disk -u GB -w 20% -c 10% -p /
    command[check_swap]=/usr/lib/nagios/plugins/check_swap -w 50 -c 20
    command[check_mem]=/usr/lib/nagios/plugins/check_mem.sh -w 50 -c 80\n"""

    # resultat dict object
    resultat = dict(
        changed = False,
        original_message='',
        message='',
    )

    # lecture du fichier de configuration d'exemple suite a l installation
    f = open('/etc/nagios/nrpe.cfg', 'r')
    message = f.read()
    f.close()

    # Recherche de l'adresse du serveur nagios et remplacement
    index_balise = message.find('allowed_hosts')
    index_debut = message.find('127.0.0.1', index_balise)
    index_fin = message.find('\n', index_debut)
    message = message[:index_debut] + ip_nagios_local + message[index_fin:]

    # ajout des indicateurs local à envoyer au serveur nagios si non fait
    # Recherche des following examples use hardcoded command arguments et remplacement
    index_balise = message.find('following examples use hardcoded command')
    index_debut = message.find('\ncommand', index_balise)
    index_fin = message.find('# The following examples allow user-supplied', index_debut) - 2
    if message.find('# supervision Auto-Nagios') == -1:
        message = message[:index_debut] + indicateurs + message[index_fin:]
        resultat['changed'] = True
    else:
        resultat['changed'] = False
    # Ecriture de la configuration
    f = open('/etc/nagios/nrpe.cfg', 'w')
    f.write(message)
    f.close()


    resultat['original_message'] = request_local
    resultat['message'] = 'goodbye'

    module.exit_json(**resultat)


if __name__ == "__main__":
    main()

