import json
import requests
from datetime import datetime, timedelta
import time
import random
import os
import random
import time
import datetime


url = f"https://www.bandsintown.com/choose-dates/fetch-next/upcomingEvents?longitude=-74.006&latitude=40.7128&genre_query=all-genres"
            


def scrap_one_page(url,page,dateone,datebis):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
            
    url = f"{url}&date={dateone}T00%3A00%3A00%2C{datebis}T23%3A00%3A00&page={page}&longitude=-74.006&latitude=40.7128&genre_query=all-genres"
    response = requests.get(url, headers=headers)
    dico = response.json()
    
    return dico 
    

def save_json(response, idx_page, date1,date2, folder="data_events"):
    # Créer le dossier si nécessaire
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    # Définir le nom du fichier (ex: "2024-10-01_page_1.json", etc.)
    file_name = os.path.join(folder, f"{date1}_{date2}_page_1_{idx_page}.json")
    
    try:
        # Écriture des données dans un fichier JSON
        with open(file_name, 'w', encoding='utf-8') as json_file:
            json.dump(response, json_file, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Erreur lors de l'écriture du fichier {file_name}: {e}")


def scrap_multiple_pages(start_date, end_date):
    # Initialisation du tests
    dico_ev = dict()
    page = 0
    egale = False
    data_page = None 
    page = 0

    while(egale != True):
        sleep_time = random.uniform(0.5, 5)
        time.sleep(sleep_time)
        data_page0=data_page
            
        page+=1
            
        dico=scrap_one_page(url,page,start_date,end_date)
                  
        
        if len(dico["events"]) > 0:
            data_page=dico["events"][0]['artistImageSrc']
                

            if data_page0 != data_page:
                dico_ev[f"events"] = dico_ev.get(f"events", []) + dico["events"]
                
            else:
                egale=True
                    # Ajout d'un délai aléatoire pour éviter le blocage de l'API
                sleep_time = random.uniform(0.5, 5)  
                time.sleep(sleep_time)
        else :
            sleep_time = random.uniform(0.5, 5)
            time.sleep(sleep_time)
            egale=True

    return dico_ev,page






def rcp_octobre(j):

    page=None
    dico_ev=None

    for jours in range(j, 32, 3):
        
        if dico_ev: 

            save_json(dico_ev,page,dateone,datebis)
                
        j1 = jours + 2
        if j1 > 31:
            j1 = 31
        dateone = f"2024-10-{jours:02d}"
        datebis = f"2024-10-{j1:02d}"

        dico_ev,page = scrap_multiple_pages(dateone,datebis)

    



rcp_octobre(8)



