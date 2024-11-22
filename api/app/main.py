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
from endpoints.event_search_date_start_end import router as event_search_date_start_end_router
from endpoints.event_search import router as event_search_router
import os

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
                "description": "Documentation sur les événements"
            }
        }
    ],
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,  # Réduit la profondeur des modèles affichés
        "defaultModelExpandDepth": 2  # Pour montrer plus de détails sur les objets
    },
    docs_url="/docs",
    redoc_url="/redoc"
)


# Inclure les routes
app.include_router(event_loc_router)
app.include_router(row_count_router)
app.include_router(top_venues_router)
app.include_router(event_on_hour_router)
app.include_router(best_artists_router)
app.include_router(get_events_router)
app.include_router(events_by_day_of_week_router)
app.include_router(event_search_date_start_end_router)
app.include_router(event_search_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)