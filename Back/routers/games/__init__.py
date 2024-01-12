from fastapi import APIRouter
from routers.games import grid
from routers.games import connect_players
router = APIRouter(prefix="/games")

router.include_router(grid.router)
router.include_router(connect_players.router)

@router.get("/", response_model=str)
async def get_games():
    return "grid\nconnect players"