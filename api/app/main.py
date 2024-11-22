from fastapi import FastAPI
from endpoints.event_loc import router as event_loc_router
from endpoints.row_count import router as row_count_router
from endpoints.top_venues import router as top_venues_router
from endpoints.event_on_hour import router as event_on_hour_router
from endpoints.best_artists import router as best_artists_router
from endpoints.get_events import router as get_events_router

from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="API des Événements à New York",
    description="Une API pour savoir les lieux et horaires des événements à NYC",
    version="1.0.0",
    contact={
        "name": "Group 2"
    })



# Inclure les routes
app.include_router(event_loc_router)
app.include_router(row_count_router)
app.include_router(top_venues_router)
app.include_router(event_on_hour_router)
app.include_router(best_artists_router)
app.include_router(get_events_router)

# Point de départ de l'application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)

