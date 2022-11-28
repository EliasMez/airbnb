from bs4 import BeautifulSoup
import pandas as pd
import requests
import gzip
import shutil
import os
import urllib.request
from django.core.management.base import BaseCommand

def scraper() :
    url = 'http://insideairbnb.com/get-the-data/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text)

    h3_all = data = soup.find_all('h3')

    chemins=[]
    def encodage_replace(chemin) :
        return chemin.replace(' ','_').replace('Ã¼','ü').replace('Å','a').replace('Ã¤','ä').replace('Ã©','é').replace('-','_').replace("Ã³","ó").replace("Ã­a","ía").replace("Ã","î")#.replace("",'')

    for h3 in h3_all :
        h3 = h3.getText()
        sp_list = h3.split(",")
        sp_list.reverse()
        sp_list = [sp.lstrip() for sp in sp_list]
        
        chemin = encodage_replace("/".join(sp_list)) + "/"  
        if 'Tokyo' not in chemin :
            if 'Toronto' not in chemin :
                chemins.append(chemin)

    links = [link.get('href') for link in soup.find_all('a')]
    links = filter(None,links)
    links = [href for href in links if ('csv.gz' in href and 'calendar' not in href)]

    pre_gz_path="gz_input/"
    pre_csv_path="csv_input/"
    nb_csv_per_city=2

    for i in range(len(chemins)):
        chemin = chemins[i]
        print()
        print(str(i+1) + ' sur ' + str(len(chemins)))
        print(chemin)
        gz_path = pre_gz_path + chemin
        csv_path = pre_csv_path + chemin
        for y in range(nb_csv_per_city) :
            link = links[nb_csv_per_city*i+y]
            print(link)
            if not os.path.exists(gz_path):
                os.makedirs(gz_path)
            gz_link = gz_path + link.split('/')[-1]
            csv_link = csv_path + link.split('/')[-1][:-3]

            try :
                urllib.request.urlretrieve(link,gz_link)
                if not os.path.exists(csv_path) :
                    os.makedirs(csv_path)
                
                with gzip.open(gz_link, 'rb') as f_in:
                    with open(csv_link, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
            except UnicodeEncodeError:
                print('UnicodeEncodeError au dessus')
                continue
        


    shutil.rmtree(pre_gz_path)

    # dossiers erreur unicode :
    # input_path_list = [x[0] for x in os.walk(pre_csv_path) if x[1]==[]]
    # for path in input_path_list:
    #     if len(os.listdir(path)) == 0:
            # shutil.rmtree(path) #supprimer dossiers vides a répeter
    #         print(path)

class Command(BaseCommand):
    help = 'Does some magical work'

    def handle(self, *args, **options):
        """ Do your work here """
        scraper()
        self.stdout.write('There are nothings!')