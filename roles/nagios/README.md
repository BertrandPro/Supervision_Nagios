Role Name
=========

Crée un fichier serveur_xxx.cfg dans le répertoire donné avec les indicateurs a suivre sur une machine distante.

Requirements
------------

Un Nagios instalaler avec un repertoire evaluer (ex : /usr/local/nagios/etc/servers/)

Role Variables
--------------

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

Dependencies
------------

No.

Example Playbook
----------------

- name: ajout du fichier 'name_supervise'.cfg à nagios
  auto-nagios-add:
    ip_supervise: '192.168.1.25'
    name_supervise: 'serveur_test25'
    path_supervision: '/usr/local/nagios/etc/servers/'
  
License
-------

GNU General Public License v3.0+

Author Information
------------------

Bertrand PRODAULT.
