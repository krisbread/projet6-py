# projet6-py
script python (linux) : sauvegarde automatique de wordpress et de sa base de données(local) sur dropbox.

1 # Récupération des informations sur la machine pour vérifier la compatibilité (os).

2 # Création des dossiers de sauvegarde en local pour : 
wordpress, base de données et d'un dossier zip (utilisation de : os.mkdir())
racine des dossiers : /tmp/
création des dossiers : /tmp/sauvegarde
                        /tmp/sauvegarde/sauv_wp
                        /tmp/sauvegarde/sauv_bdd
                        /tmp/sauvegarde/sauv_zip 

3 # sauvegarde de la base de données dans le dossier sauv_bdd. (os.system)

4 # sauvegarde du dossier wordpress dans sauv_wp, avec comme nom la date et l'heure de creation.
Utilisation de : (datetime.datetime.now().strftime("%y-%m-%d_%Hh-%M") et (shutil.copytree())

5 # compression individuelle des dossiers sauvegardés vers le dossier sauv_zip (shutil.make_archive())

6 # Test de connexion à internet. (urllib.request)
Si la connexion echoue, on quit le programme.

7 # Upload des sauvegardes sur DropBox.
