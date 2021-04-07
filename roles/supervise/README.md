Role Name
=========

Modifie le fichier /etc/nagios/nrpe.cfg pour modifier le serveur nagios et ajouter des indicateurs a suivre par le nagios distant.

Requirements
------------

Une instalation de nagios-nrpe.

Role Variables
--------------

    ip_nagios:
        description: addresse ip (ou host si DNS) du serveur nagios.
        required: true
        type: str

Dependencies
------------

No.

Example Playbook
----------------

- name: Config auto nrpe
  auto_nagios_nrpe:
    ip_nagios: "192.168.1.49"


License
-------

GNU General Public License v3.0+

Author Information
------------------

Bertrand PRODAULT.