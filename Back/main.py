from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware


from const import (
    OPEN_API_DESCRIPTION,
    OPEN_API_TITLE,
)
from routers import (
    leagues,
    players,
    player_team,
    teams,
    games,
    specials
)


app = FastAPI(
    title=OPEN_API_TITLE,
    description=OPEN_API_DESCRIPTION,
    version='0.4',
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/favicon.ico")
async def get_favicon():
    return FileResponse("static/favicon.ico")

app.include_router(leagues.router)
app.include_router(players.router)
app.include_router(player_team.router)
app.include_router(teams.router)
app.include_router(specials.router)
app.include_router(games.router)
