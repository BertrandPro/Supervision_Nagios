# Supervision_Nagios
Automatisation de la  supervision par le service Nagios d’une nouvelle machine dans un parc informatique.

Le but de ce projet est d’automatiser la  supervision par le service Nagios (déjà en place sur un serveur) d’une nouvelle machine dans un parc informatique.

Sur la machine a superviser, le script
- Installe le serveur NRPE et les plugins
VARIANTE : selon l’OS (Debian/Ubuntu, CentOS / RHEL, autre...)
- Cré un utilisateur spécifique à la supervision
- Configure la liaison supervisé/superviseur
- Configure un certain nombre d’indicateur local
variante : Qui dépende du type de machine (poste de travail, serveur HTTP, MySQL…)
- Si SGBD : configuration d’un acces par Nagios et création utilisateur

Sur le superviseur :
- Ajoute le Host à Nagios
- Ajoute les indicateur Locaux (RRPE) et distant (acc »s HTTP, ping…)


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
VARIANTE : hote si VM…
