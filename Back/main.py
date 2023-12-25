from fastapi import FastAPI

from const import (
    OPEN_API_DESCRIPTION,
    OPEN_API_TITLE,
)
from routers import (
    leagues,
    players
)


app = FastAPI(
    title=OPEN_API_TITLE,
    description=OPEN_API_DESCRIPTION,
    version='0.3',
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.include_router(leagues.router)
app.include_router(players.router)