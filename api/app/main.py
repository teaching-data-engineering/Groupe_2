from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from endpoints.event_loc import router as event_loc_router
from endpoints.row_count import router as row_count_router
from endpoints.top_venues import router as top_venues_router
from endpoints.event_on_hour import router as event_on_hour_router
from endpoints.best_artists import router as best_artists_router
from endpoints.get_events import router as get_events_router
from endpoints.events_by_day_of_week import router as events_by_day_of_week_router
import os

# Obtenir le chemin absolu du répertoire courant
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(
    title="API des Événements à New York",
    description="Une API pour savoir les lieux et horaires des événements à NYC",
    version="1.0.0",
    contact={
        "name": "Group 2"
    },
    openapi_tags=[
        {
            "name": "Evenements",
            "description": "Accédez aux informations sur les événements à New York.",
            "externalDocs": {
                "description": "Documentation sur les événements",
                "url": "https://example.com"
            }
        }
    ],
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "defaultModelExpandDepth": 2
    }
)

# Monter les fichiers statiques avec le chemin absolu
static_dir = os.path.join(BASE_DIR, "static")
templates_dir = os.path.join(BASE_DIR, "templates")

# Vérifier et créer les répertoires s'ils n'existent pas
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
    os.makedirs(os.path.join(static_dir, "css"))
    os.makedirs(os.path.join(static_dir, "js"))

if not os.path.exists(templates_dir):
    os.makedirs(templates_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Configurer les templates avec le chemin absolu
templates = Jinja2Templates(directory=templates_dir)

# Route pour la page d'accueil
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Inclure les routes
app.include_router(event_loc_router)
app.include_router(row_count_router)
app.include_router(top_venues_router)
app.include_router(event_on_hour_router)
app.include_router(best_artists_router)
app.include_router(get_events_router)
app.include_router(events_by_day_of_week_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)