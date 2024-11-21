import json
import requests
from datetime import datetime, timedelta
import time
import random
import os
import random
import time
import datetime
import pandas as pd
from bs4 import BeautifulSoup
import re

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

    return dico_ev,page-1






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

    


# Récupération des données
# rcp_octobre(8)

# Transformation des json en df pandas
def jsons_to_dataframe(directory):
    # Liste pour stocker tous les événements
    events = []

    # Parcourir tous les fichiers dans le répertoire
    for filename in os.listdir(directory):
        if filename.endswith('.json'):  # Vérifiez que le fichier est un JSON
            json_file_path = os.path.join(directory, filename)
            # Lire le fichier JSON
            
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Parcourir les données JSON
            for date_range, event_list in data.items():
                for event in event_list:
                    # Ajout de la période à chaque événement
                    event['date_range'] = date_range
                    # Ajouter l'événement à la liste
                    events.append(event)

    # Convertir la liste en DataFrame
    final_df = pd.DataFrame(events)
    
    # On peut aussi réorganiser ou renommer certaines colonnes si nécessaire
    return final_df



# Utilisation de la fonction
directory = 'data_events'  # Remplacez par le chemin correct vers votre dossier
df = jsons_to_dataframe(directory)

#print(df.columns)
# Afficher les premières lignes du DataFrame
#print(df.head())
#print(df.shape)


# Affichage propre du dataframe
def afficher_avec_tabulate(df):
    df = df.drop(columns = ['artistImageSrc', 'properlySizedImageURL', 'callToActionRedirectUrl', 'fallbackImageUrl', 'streamingEvent', 'pinIconSrc', 'eventUrl', 'artistUrl', 'watchLiveText', 'isPlus', 'callToActionText', 'timezone'])
    df[['DateStartEvent', 'HourStartEvent']] = df['startsAt'].str.split('T', expand=True)
    df = df.drop(columns = ['DateStartEvent'])

    return df

# Téléchargement du fichier
df.to_csv("data_NY.csv")

# Import du fichier

data = pd.read_csv("data_NY.csv")

def recup_followers_Shows(url):

    sleep_time = random.uniform(0.13, 0.56)
    time.sleep(sleep_time)

    user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/92.0"
]

    headers = {
    "User-Agent": random.choice(user_agents)
}
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    #print(soup)

    # Extraction du nombre de followers
    followers_div = soup.find('div', class_='eR4wTX9jPTzBy4HTQWjx')
    if followers_div:
        followers_text = followers_div.text
        # Recherche d'un chiffre avec ou sans virgule avant "Followers"
        followers_match = re.search(r'([\d,]+)\s*Followers', followers_text, re.IGNORECASE)
        if followers_match:
            # Nettoyer la valeur pour retirer les virgules
            followers = followers_match.group(1).replace(',', '')
        else:
            followers = None
    else:
        followers = None
        

    # Extraction du nombre de shows
    show_div = soup.find('div', class_='IVmyWKohpQCYW1CkKHYw')
    if show_div:
        show_text = show_div.text
        # Recherche du chiffre avant "Shows"
        show_match = re.search(r'(\d+)', show_text, re.IGNORECASE)
        show = show_match.group(1) if show_match else None
    else:
        show = None
        

    return followers, show  


# l_followers = list()
# l_show = list()

# for artis_url in data['artistUrl']:
#     followers,show = recup_followers_Shows(artis_url)
#     l_followers.append(followers.split()[0])
#     l_show.append(show.split()[0])

# print(l_followers[:3])

def num_week(my_date):
    day = my_date.day  # Récupérer le jour du mois
    num = 0
    if day <= 7:
        num = 1
    elif 8 <= day <= 14:
        num = 2
    elif 15 <= day <= 21:
        num = 3
    elif 22 <= day <= 28:
        num = 4
    elif 29 <= day <= 31:
        num = 5
    return num

def segment_rsvp(df, rsvp_count):
    if rsvp_count <= df['rsvpCountInt'].quantile(0.25):
        return 'Low'
    elif df['rsvpCountInt'].quantile(0.25) < rsvp_count <= df['rsvpCountInt'].quantile(0.50):
        return 'Medium'
    elif df['rsvpCountInt'].quantile(0.50) < rsvp_count <= df['rsvpCountInt'].quantile(0.75):
        return 'High'
    else:
        return 'Very High'

def enrish(data):
    data['startsAt'] = pd.to_datetime(data['startsAt'])
    data['endsAt'] = pd.to_datetime(data['endsAt'])
    data['is_weekend'] = data['startsAt'].apply(lambda date: date.weekday() >= 5)
    data['num_semaine'] = data['startsAt'].apply(num_week)
    data['jour_avant']=  (datetime.datetime.today() - data['startsAt'])
    data['jour_avant']= data['jour_avant'].apply(lambda date: date.days)
    data= data.drop(columns= 'Unnamed: 0')
    return data

# Utilisation de la fonction
#print(afficher_avec_tabulate(data))

data = enrish(data)

# Téléchargement du fichier
data = enrish(data)
data.to_csv("data_NY_enrish.csv")
#print(data.columns)



# print(data.columns)

# print(data.head(10))


# from google.cloud import bigquery


# from google.oauth2 import service_account
# import pandas_gbq



# credentials = service_account.Credentials.from_service_account_file(
#     "sa-key-group-2.json",
# )
# pandas_gbq.to_gbq(data, "dataset_groupe_2.test", project_id="ai-technologies-ur2",credentials=credentials, if_exists="replace")