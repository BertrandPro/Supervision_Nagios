#!/usr/bin/python

# Copyright: (c) 2020, Your Name <YourName@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: auto_nagios_add

short_description: Add serveur_xxx.cfg in nagios

version_added: "0.0.1"

description:  Module qui ajoute un fichier serveur_xxx.cfg avec les indicateurs a suivre dans nagios. 

options:
    ip_supervise:
        description: address ip (ou host si DNS) du serveur a supervise.
        required: true
        type: str
    name_supervise:
        description: nom du host a supervise sous la forme serveur_xxx.
        required: true
        type: str
    path_supervision:
        description: chemin pour le fichier serveur_xxx.cfg
        required: true
        type: str

author:
    - BertrandBZH (bertrand.pro@gmail.com)
'''

EXAMPLES = r'''
- name: Config auto add.cfg
  auto_nagios_add:
    ip_supervise: "192.168.1.30"
    name_supervise: "serveur_alpha"
    path_supervision: "/usr/local/nagios/messerveurs/"
'''

RETURN = r'''
    result:
       description : return ?
'''

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(
            ip_supervise=dict(required=True, type='str'),
            name_supervise=dict(required=True, type='str'),
            path_supervision=dict(required=True, type='str'),
        )
    )

    ip_supervise_local = module.params.get('ip_supervise')
    name_supervise_local = module.params.get('name_supervise')
    path_supervision_local = module.params.get('path_supervision')

    config = """
###############################################################################
#
# HOST DEFINITION
#
###############################################################################

define host {
    use                 linux-server
    host_name           __host_name__
    address             __host_ip__
    check_command       check_ping!40,40%!60,60%
    contacts            nagiosadmin
    parents             Passerelle
}


###############################################################################
#
# SERVICE DEFINITIONS
#
###############################################################################

# Define a service to "ping" the local machine

define service {
    use                 local-service           ; Name of service template to use
    host_name           __host_name__
    service_description 01 - Ping du serveur
    check_command       check_ping!1,20%!2,40%
    contacts            nagiosinfra
}

# Define a service to check the load on the distant machine using NRPE.

define service {
    use                 local-service
    host_name           __host_name__
    service_description 02 - Charge Systeme
    check_command       check_nrpe!check_load
    contacts            nagiosinfra
}

# Define a service to check the memory on the distant machine using NRPE.

define service {
    use                     local-service           ; Name of service template to use
    host_name               __host_name__
    service_description     03 - Memoire libre
    check_command           check_nrpe!check_mem
    contacts                nagiosinfra
}

# Define a service to check the number of currently running procs
# on the distant machine using NRPE.

define service {
    use                     local-service
    host_name               __host_name__
    service_description     04 - Nb de Processus actif
    check_command           check_nrpe!check_procs
    contacts                nagiosinfra
}

# Define a service to check the number of currently logged in
# on the distant machine using NRPE.

define service {
    use                     local-service           ; Name of service template to use
    host_name               __host_name__
    service_description     05 - Nb utilisateur connecte
    check_command           check_nrpe!check_users
    contacts                nagiosinfra
}

# Define a service to check the disk space of the root partition
# on the distant machine using NRPE.

define service {
    use                     local-service           ; Name of service template to use
    host_name               __host_name__
    service_description     06 - Espace disque libre sur Partition Root
    check_command           check_nrpe!check_disk
    contacts                nagiosinfra
}

# Define a service to check the swap usage the local machine.
# on the distant machine using NRPE.

define service {
    use                     local-service           ; Name of service template to use
    host_name               __host_name__
    service_description     07 - Utilisation Swap
    check_command           check_nrpe!check_swap
    contacts                nagiosinfra
}
\n"""

    # resultat dict object
    resultat = dict(
        changed=False,
        original_message='',
        message='',
    )

    # lecture du fichier de configuration s'il existe
    try:
        f = open(path_supervision_local + name_supervise_local + '.cfg', 'r')
    except IOError:
        # le fichier n'existe pas donc il faut le créé
        resultat['changed'] = True
    #        Warning("le fichier n'existe pas")
    else:
        resultat['changed'] = False
        #        Warning("le fichier existe")
        message = f.read()
        f.close()

    # Recherche de l'adresse du serveur et remplacement
    index_balise = config.find('__host_ip__')
    index_debut = config.find('__host_ip__', index_balise)
    index_fin = config.find('\n', index_debut)
    config = config[:index_debut] + ip_supervise_local + config[index_fin:]

    # Recherche et remplacement de tout les nom de host
    index_balise = config.find('__host_name__')
    while index_balise != -1:
        index_debut = config.find('__host_name__', index_balise)
        index_fin = config.find('\n', index_debut)
        config = config[:index_debut] + name_supervise_local + config[index_fin:]
        index_balise = config.find('__host_name__')

    # Ecriture de la configuration
    f = open(path_supervision_local + name_supervise_local + '.cfg', 'w')
    f.write(config)
    f.close()

    resultat['original_message'] = 'original_message'
    resultat['message'] = 'goodbye'

    module.exit_json(**resultat)

if __name__ == "__main__":
    main()

