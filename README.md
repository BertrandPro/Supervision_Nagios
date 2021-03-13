# Supervision_Nagios
EN dev !

Le but de ce projet est d’automatiser la  supervision  par le service Nagios (déjà en place sur un serveur) d’une nouvelle machine dans un parc informatique.
On utilise pour cela Ansibles pour les tache de déploiement / installation, et un module python pour la configuration.

Les indicateurs de base sont les suivants :

Charge Système : Les valeurs typique : 0.5 0.2 0.1 ; Warning : 1 0.4 0.2 ; Critique : 2 1 0.5
Memoire libre : Valeurs typique : 30 % ; Warning : 75 % ; Critique : 90 %
Nb de Processus actif : Valeurs typique : 150 ; Warning : 200 ; Critique : 250
Nb utilisateur connecte : Valeurs typique : 0 ; Warning : 2 ; Critique : 5
Espace disque libre sur Partition Root : Valeurs typique : selon serveur ; Warning : 20 % ; Critique : 10 %
Utilisation Swap : Valeurs typique : 0 ; Warning : 50 ; Critique : 20
Températures de CPUs : Valeurs typique : 0 ; Warning : 50 ; Critique : 20


Sur la machine a superviser, on ajoute :
Ansible	=> Installe le serveur NRPE et les plugins
VARIANTE : selon l’OS (Debian/Ubuntu, CentOS / RHEL, autre...)
Ansible	=> Crée un utilisateur spécifique à la supervision

module python	=> Configure un certain nombre d’indicateur local (fichier nrpe.cfg format .ini)

variante : Qui dépende du type de machine (poste de travail, serveur HTTP, MySQL…)
?????? => Si SGBD : configuration d’un acces par Nagios et création utilisateur

Sur le superviseur :
Python ? Ajoute le Host à Nagios
Python ? Ajoute les indicateur Locaux (RRPE) et distant (acc »s HTTP, ping…)


Pour cela, on a besoins :

FIXE :
Ip de Nagos
Utilisateur et mdp de Nagios
Utilisateur et mdp commun à tout les hosts


VARIABLE :
Ip du host,
compte et mdp sudo (pour l’install)
Type de supervision (http ? SGBD…)
Si SGBD : database, user et mdp
les valeur des W et C… ???
VARIANTE : hote si VM…


Utilisation :
on veux superviser une machine IP avec un utilisateur USER ayant pour mdp MDP

sur le superviseur (déjà configurer avec une paire de clé et un agent-ssh :
$ ssh-copy-id USER@IP
valider l’empreinte et le mdp.
