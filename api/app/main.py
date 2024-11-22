from fastapi import FastAPI
from endpoints.event_loc import router as event_loc_router
from endpoints.row_count import router as row_count_router
from endpoints.top_venues import router as top_venues_router
from endpoints.event_on_hour import router as event_on_hour_router
from endpoints.bests_artists import router as bests_artists_router
from endpoints.get_events import router as get_events_router
from endpoints.events_by_day_of_week import router as events_by_day_of_week_router
from endpoints.event_search import router as event_search_router
from endpoints.event_search_date_start_end import router as event_search_date_start_end_router

app = FastAPI()

# Inclure les routes
app.include_router(event_loc_router)
app.include_router(row_count_router)
app.include_router(top_venues_router)
app.include_router(event_on_hour_router)
app.include_router(bests_artists_router)
app.include_router(get_events_router)
app.include_router(events_by_day_of_week_router)
app.include_router(event_search_router)
app.include_router(event_search_date_start_end_router)

# Point de départ de l'application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)