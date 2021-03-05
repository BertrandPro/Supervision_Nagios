#! /usr/bin/env python3
# coding: utf-8

import argparse
import logging as lg
import ipaddress
import configparser

import nagios


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--ip",help="""IPv4/CIDR de la machine a superviser""")
    parser.add_argument("-U", "--USER", help="""utilisateur (sudo) de la machine à superviser""")
    parser.add_argument("-P", "--PASSWORD", help="""Mot de passe de la machine a superviser""")
    parser.add_argument("-v", "--verbose", action='store_true', help="""Make the application talk!""")
    return parser.parse_args()

def install_nrpe():
    print("installation de nrpe sur la cible")


def create_user():
    print("Création de l'utilisateur")

def ajout_serveur():
    indicateurs = """# supervision Auto-Nagios : ajout des commandS argument\n
command[check_load]=/usr/lib/nagios/plugins/check_load -r -w .15,.10,.05 -c .30,.25,.20
command[check_procs]=/usr/lib/nagios/plugins/check_procs -w 150 -c 200
command[check_users]=/usr/lib/nagios/plugins/check_users -w 2 -c 5
command[check_disk]=/usr/lib/nagios/plugins/check_disk -u GB -w 20% -c 10% -p /
command[check_swap]=/usr/lib/nagios/plugins/check_swap -w 50 -c 20
command[check_mem]=/usr/lib/nagios/plugins/check_mem.sh -w 50 -c 80\n"""

    # lecture du fichier de configuration d'exemple suite a l instalation
    f = open('nrpe.vierge.cfg','r')
    message = f.read()
    f.close()

    # Recherche de l'adresse du serveur nagios et remplacement
    index_balise = message.find('allowed_hosts')
    index_debut = message.find('127.0.0.1',index_balise)
    index_fin =  message.find('\n',index_debut)
    message = message[:index_debut]+str(nagios.IP.ip)+message[index_fin:]

    # ajout des indicateurs local à envoyer au serveur nagios si non fait
    # Recherche des following examples use hardcoded command arguments et remplacement
    index_balise = message.find('following examples use hardcoded command')
    index_debut = message.find('\ncommand',index_balise)
    index_fin =  message.find('# The following examples allow user-supplied',index_debut)-2
    if message.find('# supervision Auto-Nagios') == -1:
        message = message[:index_debut] + indicateurs + message[index_fin:]

    # Ecriture de la configuration
    f = open('nrpe.cfg','w')
    f.write(message)
    f.close()

def main():
    args = parse_arguments()
    if args.verbose:
        lg.basicConfig(level=lg.DEBUG)
    try:
        if args.ip == None:
            raise Warning("Indiquer la machine a superviser : --ip xxx.xxx.xxx.xxx")
        elif args.USER == None:
            raise Warning("Indiquer un utilisateur sudo pour la machine a superviser : -U login")
        elif args.PASSWORD == None:
            raise Warning("Indiquer le mot de passe de l'utilisateur : -P mot_de_passe")
        else:
            ip_cible = ipaddress.ip_address(args.ip)
            user = args.USER
            mdp = args.PASSWORD

            print("ip nagios : ", nagios.IP)
            print("réseaux :", nagios.IP.network)
            if ip_cible in nagios.IP.network:
                lg.debug("{} est bien dans dans le reseau {}".format(ip_cible,nagios.IP.network))
            else:
                lg.critical("{} n'est pas dans le réseau {}".format(ip_cible,nagios.IP.network))
            lg.debug("user : {} - mot de passe : {}".format(args.USER,args.PASSWORD))


    #         try:
    #                 # if args.extension == 'xml':
    #             #     x_an.launch_analysis(datafile)
    #             # elif args.extension == 'csv':
    #             #     c_an.launch_analysis(datafile)
    #         except FileNotFoundError as e:
    #             print("Ow :( The file was not found. Here is the original message of the exception :", e)
    #         finally:
    #             lg.info('#################### Analysis is over ######################')
    except Warning as e:
        lg.warning(e)

    # install_nrpe(ip_cible)
    # create_user(ip_cible, user, mdp)
    ajout_serveur()

if __name__ == "__main__":
    main()