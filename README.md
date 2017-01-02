# TarDilaData
Script qui permet de télécharger les données publiées par la Dila

Data
===
Les données sont diffusées par la dila sur un ftp et recencées sur le site data.gouv.fr.
L'organisation diffusante sur data.gouv.fr est en fait le "Premier Ministre" ([voir sa page de publication](http://www.data.gouv.fr/fr/datasets/?sort=-created&organization=534fffa5a3a7292c64a7809e))


A quoi sert ce repo ?
===
Le programme permet de lever deux difficultés associées au mode de diffustion des données. En effet, celles-ci sont diffusées avec des mises à jour régulière. Cela est pratique pour ne pas avoir à recharger un fichier à chaque nouvelle version mais il peut s'avérere très fastidieux de télécharger une à une les mises à jour pour reconstituer toute la base.

Le fichier permet donc :
  - de télécharger automatiquement toutes les données (que j'appelle zip par abus de langage, ce sont des fichiers compressé en tar.gz (tar donnant en partie le nom du repo)).
  - le téléchargement tient compte de difficulté de téléchargement potentielle et d'accès perturbé au ftp.
  - de les extraires
  - de potentiellement les ranger différemment même si on préférera utiliser les outils de parcours des fichiers (contenu dans le dossier)


  Utilisation - Documentation
  ===
  Le dossier contient un fichier de configuration rudimentaire et une le programme tardiladata.py.
  Le fichier de configuration contient la définition du chemin dila_data_path où vous voulez enregistrer les données sur votre disque.
  Le fichier tardiladata.py contient :
  * une fonction principale : TarDilaData. Cette fonction prend le nom d'une base de téléchargement
    * Elle lit la page dila correspondate
    * Elle télécharge les fichiers dans le dossier : dila_data_path\nom_de_la_base\zip s'ils n'ont pas déjà été téléchargé
    * Elle extrait les zip dans le dossier : dila_data_path\nom_de_la_base\extract s'il n'ont pas déjà été extraits
    * Elle vérifie que tout s'est bien passé au téléchargement et à l'extraction
    * **Attention: le fichier Freemium est très lourd et il faut le traiter à la main**. Le programme ne s'en occupe pas.
  * des fonctions pour reorganiser les fichier
    * gommme_le_dossier_correspondant_au_telechargement retire le nom du fichier associé à l'extraction, avec ce programme on peut donc avoir tous les fichiers et leur arborescence comme si on avait eu un fichier unique. Les fichiers sont rangés dans dila_data_path\nom_de_la_base\files
    * gomme_la_base_origine fait la même chose mais en retirant aussi le nom de la base pour mettre tout dans un dossier dila_data_path\ALL. Assez coûteux en temps (et en espace), cette fonction est moins utile que la suivante
    * get_all_path_base permet de parcourir toute le dossier extract d'un base et de retourner tous les chemins correspondant au fichier et la liste des fichiers avec l'option filename_only
  * une fonction doublon et du code commenté pour regarder quels sont les doublons entre différentes bases

  TODO
  ===
  Le programme a été testé sur les base INCA, CASS, CAPP et JADE dans leur partie xml. On peut vouloir compléter avec d'autres bases.
