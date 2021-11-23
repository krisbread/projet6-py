#!/usr/bin/python3

import os, platform, socket, datetime, shutil, pipes, subprocess
from os import getcwd
from os import chdir
from os import mkdir


# 1 # informations sur la machine.
hostname = socket.gethostname()

print("\n\n\t\t########################################################\n")
print("Informations sur votre sytème :\n")
print("Le nom de votre machine est :", hostname, "\nVous êtes sur le systéme d'exploitation", platform.system(), "en version", platform.version(), "avec processeur", platform.machine(),"\n")
if platform.system() == "linux" :
    print("Informations sur votre système :\n")
else :
    print("Désolé, programme en cours de développement pour le sytème d'exploitation", platform.system())
    print("L'application va se fermer.\n\n")
    quit()


# 2 # Dossiers de sauvegarde
sauv = ('/tmp/sauvegarde')
  # dossier contenant les sauvegardes compréssées pour envoi
sauv_zip = ('/tmp/sauvegarde/sauv_zip')

  # dossier de sauvegarde pour la base de données
sauv_bdd = ('/tmp/sauvegarde/sauv_bdd')

  # dossier de sauvegarde wordpress
sauv_wp = ('/tmp/sauvegarde/sauv_wp')

# Création des dossiers de sauvegarde
  # dossier sauvegarde
try:
    os.mkdir(sauv)
    print('création du dossier principal de sauvegarde ')
except: 
    print('le dossier : sauvegarde est deja present')

  # dossier sauv_zip
try:
    os.mkdir(sauv_zip)
    print('création du dossier de sauvegarde : sauv_zip')
except: 
    print('le dossier : sauv_zip est deja present')

  # dossier sauv_bdd
try:
    os.mkdir(sauv_bdd)
    print('création du dossier de sauvegarde : sauv_bdd')
except: 
    print('le dossier : sauv_bdd est deja present')

  # dossier sauv_wp
try:
    os.mkdir(sauv_wp)
    print('création du dossier de sauvegarde : sauv_wp')
except: 
    print('le dossier : sauve_wp est deja present')

# 3 # sauvegarde de la base de données wordpress dans 'sauv_bdd'
dbpassword = '*****' ### indiquer votre mot de passe (attention mdp en clair !!!)
dbhost = 'localhost'
dbwp = 'wp_opcr'
dbwp_sauv = "wp_opcr.sql"
dump_cmd = 'mysqldump'+ ' -u '+ 'root' + ' -p[dbpassword] ' +  dbwp + ' > ' + pipes.quote(sauv_bdd) + '/' + dbwp + '.sql'

# Execution et vérification de l'execution de la commande 'dump_cmd'
if os.system(dump_cmd) == 0:
       print("La sauvegarde de la base de données c'est correctement effectuée")
else:
       print('une erreur c\'est produite lors de la sauvegarde de la base de données')


# 4 # sauvegarde de wordpress 'dossier html' dans sauv_wp
path_wordpress = '/var/www'
datetime = datetime.datetime.now().strftime("%y-%m-%d_%Hh-%M")
try:
    shutil.copytree(path_wordpress , sauv_wp +'/'+ datetime)
    print('sauvegarde du dossier html effectuée dans le dossier : ' + datetime)
    print('chemin complet de la sauvegarde : '+  sauv_wp +'/'+ datetime)
except IOError:
    print('un dossier de sauvegarde datetime a ete cree il y a moins d/une minute')

# Compression des sauvegardes vers sauv_zip
  # zip de la base de données vers sauv_zip
try:
    shutil.make_archive('/tmp/sauvegarde/sauv_zip/bdd', 'zip' , sauv_bdd)
    print('la sauvegarde de la base de données au format zip c\'est correctement effectuée')

except IOError: 
    print('une erreur c\'est produite lors de la sauvegarde au format zip de la base de données')
 
  # zip wp vers sauv_zip
try:
    shutil.make_archive('/tmp/sauvegarde/sauv_zip/wp', 'zip' , sauv_wp)
    print('la sauvegarde wordpress au format zip c\'est correctement effectuée')
except IOError:
    print('une erreur c\'est produite lors de la sauvegarde au format zip du dossier wordpress')

## Upload des sauvegardes vers DropBox
import dropbox
TOKEN = "inserer ici le jeton obtenu " # jeton obtenu sur dropbox votre compte
LOCAL_PATH = "/tmp/sauvegarde/sauv_zip/bdd.zip"    # replace by your local data
REMOTE_PATH = "/bdd.zip"                # replace by the full name of the remote file 
LOCAL_PATH1 = "/tmp/sauvegarde/sauv_zip/wp.zip"
REMOTE_PATH1 = "/wp.zip"

def main(args):

    # try connect with dropbox
    try:
        dbx = dropbox.Dropbox(TOKEN)
        print("Connection OK")

    except Exception as e:
        print(str(e))
        return 1

    try:
        dbx.users_get_current_account()
        print ("TOKEN OK")

    except AuthError:
        print("ERROR: Invalid access token")
        return 1

    try:
        f=open(LOCAL_PATH,"rb")
        dbx.files_upload(f.read(), REMOTE_PATH, mute=True)
        f.close()

    except Exception as err:
        print("Upload err: ", err)

    try:
        ff=open(LOCAL_PATH1,"rb")
        dbx.files_upload(ff.read(), REMOTE_PATH1, mute=True)
        ff.close()

    except Exception as err:
        print("Upload err: ", err)

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))


