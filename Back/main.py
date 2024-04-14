from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pathlib
import uvicorn
templates = Jinja2Templates(directory="templates")


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

app.mount("/assets", StaticFiles(directory=pathlib.Path(__file__).parent / 'static'), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
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

@app.get("/{full_path:path}")
async def catch_all(request: Request, full_path: str):
    print("full_path: "+full_path)
    return templates.TemplateResponse("index.html", {"request": request})

if __name__=="__main__":
    uvicorn.run("main:app",host='0.0.0.0', port=80, reload=True, workers=1)