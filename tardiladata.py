# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 13:49:07 2016

@author: aeidelman

Telécharge, ouvre et sauvegarde tous les fichiers dila
Il faut installer à la main le fichier Freemium.

"""


import os
import urllib
import re
import tarfile
import shutil
from os.path import join

from itertools import chain

from config_dila import dila_data_path

bases_dila = ['INCA', 'CASS', 'CAPP', 'JADE']


def TarDilaData(base):
    ''' télécharge toute les données de la base nécessite
        de faire le travail uniquement sur le gros fichier Freemium_xxx
        qui est lourd
    '''
    assert base in bases_dila
    small_base = base.lower()
    dila_path = join(dila_data_path, base)
    path_extract = join(dila_data_path, 'extract')
    if not os.path.exists(path_extract):
        os.mkdir(path_extract)

    url = "ftp://echanges.dila.gouv.fr/" + base + '/'

    path_dest_zip = os.path.join(dila_path, 'zip')
    if not os.path.exists(path_dest_zip):
        os.mkdir(path_dest_zip)

    html = urllib.request.urlopen(url)
    html_page = html.read()
    all_zip = re.findall(r'\w*-\w*.tar.gz', html_page.decode())
    print(len(all_zip))
    print(len(os.listdir(path_dest_zip)))

    import time

    for k in range(10):
        for zip_name in all_zip:
            if 'reemium' in zip_name:
                continue
            path_dest_zipfile = os.path.join(path_dest_zip, zip_name)
            if not os.path.exists(path_dest_zipfile):
                url = urllib.parse.urljoin(url, zip_name)
                print(zip_name)
                try:
                    data = urllib.request.urlopen(url, timeout=1)
                    with open(path_dest_zipfile, 'wb') as f:
                        f.write(data.read())
                except:
                    time.sleep(2)


    print('\n\n')

    for file in os.listdir(path_dest_zip):
        if 'reemium' in file:
            continue
        if not os.path.exists(join(path_extract, file[5:-7])):
            print(file[5:-7])
            tar = tarfile.open(join(path_dest_zip, file))
            tar.extractall(path_extract)
            tar.close()
    print('\n\n')


    # dans certains cas, il y a eu un problème de téléchargement et les données
    # d'un zip ne sont pas le dossier correspondant au nom
    set(os.listdir(path_extract))
    set(os.listdir(path_extract)) - set([file[5:-7] for file in os.listdir(path_dest_zip)])
    charges_mais_pas_extrait = set([file[5:-7] for file in os.listdir(path_dest_zip)]) - \
         set(os.listdir(path_extract))

    for file in charges_mais_pas_extrait:
        if os.path.exists(join(path_dest_zip, small_base + '_' + file + '.tar.gz')):
            print('on supprime : ', join(path_dest_zip, file + '.tar.gz'))
            os.remove(join(path_dest_zip, small_base + '_' + file + '.tar.gz'))





#### Fonctions pour déplacer les fichiers
def moveTree(sourceRoot, destRoot):
    for path, dirs, files in os.walk(sourceRoot):
        relPath = os.path.relpath(path, sourceRoot)
        destPath = os.path.join(destRoot, relPath)
        if not os.path.exists(destPath):
            os.makedirs(destPath)
        for file in files:
            destFile = os.path.join(destPath, file)
            if os.path.isfile(destFile):
                continue
            srcFile = os.path.join(path, file)
            #print "rename", srcFile, destFile
            os.rename(srcFile, destFile)



def gommme_le_dossier_correspondant_au_telechargement(base):
    assert base in bases_dila
    small_base = base.lower()
    dila_path = join(dila_data_path, base)
    path_extract = join(dila_path, 'extract')

    for folder in os.listdir(path_extract):
        print('******************************', folder)
        if base == 'JADE':
            src_folder = join(path_extract, folder, small_base, 'global')
        else:
            src_folder = join(path_extract, folder, 'juri', small_base, 'global')

        moveTree(src_folder, join(dila_path, 'files'))


def gomme_la_base_origine():
    path_for_all = join(dila_data_path, 'ALL')

    for base in bases_dila:
#        small_base = base.lower()
        dila_path = join(dila_data_path, base)
        path_files = join(dila_path, 'files')
        for path, dirs, files in os.walk(path_files):
            if files:
                for file in files:
                    shutil.copy(join(path, file), join(path_for_all, file))


def get_all_path_base(base, filename_only=False):
    ''' plus simple que de déplacer les fichiers (voir fonction ci-dessous) '''
    assert base in bases_dila
    dila_path = join(dila_data_path, base)
    path_extract = join(dila_path, 'extract')

    all_files = list()
    for path, dirs, files in os.walk(path_extract):
        if files:
            if filename_only:
                all_files += files
            else:
                files_of_path = [join(path, file) for file in files]
                all_files += files_of_path
    return all_files


def get_all_path(filename_only=False):
    ''' plus simple que de déplacer les fichiers (voir fonction ci-dessous) '''
    all_files = list()
    for base in bases_dila:
        all_files += get_all_path_base(base, filename_only)
    return all_files




def doublons(liste):
    # il y a des doublons dans les extractions (bizarre ou pas ?)
    seen = set()
    not_uniq = []
    for x in liste:
        if x in seen:
            not_uniq.append(x)
        if x not in seen:
            seen.add(x)
    return seen, not_uniq


#    all_files = []
#    for base in bases_dila:
#        all_files += get_all_path_base(join(dila_data_path, base, 'files'),
#                                      filename_only=True)
#
#    s, n = doublons(all_files)
# => Il n'y a que dix doublons !!

# les doublons c'est bien le même texte.
# on a un des fichiers un peu plus propre dans CASS que dans INCA
# il faut donc mieux mettre CASS après INCA pour écrase
