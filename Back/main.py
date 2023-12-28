from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from const import (
    OPEN_API_DESCRIPTION,
    OPEN_API_TITLE,
)
from routers import (
    leagues,
    players,
    player_team,
    teams
)


app = FastAPI(
    title=OPEN_API_TITLE,
    description=OPEN_API_DESCRIPTION,
    version='0.3',
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(leagues.router)
app.include_router(players.router)
app.include_router(player_team.router)
app.include_router(teams.router)