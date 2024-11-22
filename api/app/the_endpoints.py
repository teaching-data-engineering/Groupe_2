from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from google.cloud import bigquery 
from google.oauth2 import service_account

app = FastAPI()


from pydantic import BaseModel
class Objet(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/mon_endpoint/{objet_id}")
async def read_objet(objet_id: int, q: Union[str, None] = None):
    return {"objet_id": objet_id, "q": q}

@app.put("/mon_endpoint/{objet_id}")
def update_objet(objet_id: int, objet: Objet):
    return {"objet_name": objet.name, "objet_id": objet_id}

def connection_bigquery(query):

    credentials = service_account.Credentials.from_service_account_file(
    "api/app/sa-key-group-2.json")
    client = bigquery.Client(credentials=credentials)
    

    query_job = client.query(query)
    results = query_job.result()  # ExÃ©cute la requÃªte et rÃ©cupÃ¨re les rÃ©sultats
    return [dict(row) for row in results]  # Retourne une liste de dictionnaires
  

@app.get("/row_count/{limit}")
def get_row_count(limit: int):
    # DÃ©finir une requÃªte SQL avec la limite
    lien= "ai-technologies-ur2.dataset_groupe_2.test"
    query = f'SELECT * FROM {lien} LIMIT {limit}'
    #f'SELECT * FROM {lien} LIMIT {limit}'
    return response_req(query)

###-----------------------------------------------

def response_req(query):
    try:
        # Appeler la fonction de connexion Ã  BigQuery
        results = connection_bigquery(query)
        return {"success": True, "data": results}
    except Exception as e:
        return {"success": False, "error": str(e)}

  
@app.get("/events")
def get_events():
    lien= "ai-technologies-ur2.dataset_groupe_2.test"
    query= f'SELECT title FROM {lien} WHERE ENDS_WITH(locationText,"NY")'
    return response_req(query)


@app.get("/events/by-day-of-week/{week}")
def get_events_by_day(week: Union[int, None] = None):
    lien= "ai-technologies-ur2.dataset_groupe_2.test"
    filter_req= f"WHERE num_semaine= {week}" if isinstance(week,int) else ""
    query= f'SELECT DATE(startsAt),  COUNT(title) AS Total_events FROM {lien} {filter_req} GROUP BY DATE(startsAt)'
    return response_req(query)s

@app.get("/events/search/{artistName}+{venueName}+{date_start}+{date_end}")
def get_events_search(artistName: str | None, venueName: str| None , date_start: str | None, date_end: str | None):
    lien= "ai-technologies-ur2.dataset_groupe_2.test"

    nom_artist_req= f"WHERE artistName LIKE {artistName}" if isinstance(artistName, str) and artistName else ""
    venue_name_req= f" AND venueName LIKE {venueName}" if isinstance(venueName, str) else ""
    date_req= f' AND startsAt BETWEEN DATE({date_start}) AND DATE({date_end})' if isinstance(date_start, str) and isinstance(date_end, str) else ""

    query= f'SELECT title FROM {lien} {nom_artist_req}{venue_name_req}{date_req}'
    return response_req(query)
    

#6

@app.get("/events/search/rsvp_day_venue")
def get_rsvp_day_venue():
    lien= "ai-technologies-ur2.dataset_groupe_2.test"
    query= f"SELECT DATE(startsAt),venueName, COUNT(rsvpCount) as rsvp FROM {lien} GROUP BY venueName, DATE(startsAt)"
    return response_req(query)