# Supervision_Nagios

Le but de ce projet est d’automatiser la  supervision  par le service Nagios (déjà en place sur un serveur) d’une nouvelle machine dans un parc informatique.
On utilise pour cela Ansibles pour les taches de déploiement / installation, et des modules Ansible en python pour la configuration.

Ce que fait le playbook Ansible :
- Sur la machine a superviser définit par son ip ou son hostname : 
  - Le serveur NRPE et les plugins nagios sont installer
  - Un utilisateur spécifique à la supervision (nagios:nagcmd) est créé
  - Le fichier de configuration nrpe.cfg est modifié par un module en python pour tenir compte du serveur nagios, et on ajoute les indicateur suivant : 
      - Charge Système : Les valeurs typique : 0.5 0.2 0.1 ; Warning : 1 0.4 0.2 ; Critique : 2 1 0.5
      - Memoire libre : Valeurs typique : 30 % ; Warning : 75 % ; Critique : 90 %
      - Nb de Processus actif : Valeurs typique : 150 ; Warning : 200 ; Critique : 250
      - Nb utilisateur connecte : Valeurs typique : 0 ; Warning : 2 ; Critique : 5
      - Espace disque libre sur Partition Root : Valeurs typique : selon serveur ; Warning : 20 % ; Critique : 10 %
      - Utilisation Swap : Valeurs typique : 0 ; Warning : 50 ; Critique : 20
   - Si le fichier a été modifier, le service nrpe est redémaré.

- Sur le superviseur :
  - un fichier de configuration pour la machine a superviser est ajouté à Nagios dans /usr/local/nagios/etc/servers/ (ou autre selon l'instalation)
  - le service nagios est redémaré.

Mode opératoire :
- Recuperer le répértoire du projet sur le serveur Ansible :  git clone https://github.com/BertrandPro/Supervision_Nagios.git
- Aller dans le dossier Supervision_Nagios (cd  Supervision_Nagios)
- copier le clé ssh du serveur Ansible vers le ou les serveurs a supervisé : (ssh-copy-id -i ../.ssh/id_ecdsa.pub superuser@ip_serveur)
- Eventuellement mettre un agent ssh ( eval $(ssh-agent) && ssh-add -t 2h)
- Crée un fichier vault-passwd.txt comportant le mot de passe vault 'Ansible' ( echo 'Ansible' > vault-passwd.txt)
- Dans 00_inventory.yml, indiqué l'ip ou le hostname (si dns) du serveur nagios, et ceux de la ou des serveur a supervisé.
- Dans host_vars/ créé un fichier du nom du serveur nagios avec l'utilisateur et son mot de passe. utiliser le fichier oc-nagios.yml comme exemple. Le fichier etant crypté, faire un : "ansible-vault edit host_var/oc-nagios.yml --vault-password-file vault-passwd.txt"
- Dans group_vars/supervises/supervises.yml, indiquer l'utilisateur et le mot de passe de l'utilisateur sudo. Le fichier etant crypté, faire un : "ansible-vault edit group_var/supervises/supervises.yml --vault-password-file vault-passwd.txt"
- Dans roles/supervise/task/main.yml, modifier l'ip_nagios:.
- Dans roles/nagios/task/main.yml, modifier l'ip, le nom du serveur et le chemin du dossier contenant les configuration Nagios.
- lancer le playybook : ansible-playbook -i 00_inventory.yml --vault-password-file vault-passwd.txt  playbook.yml
