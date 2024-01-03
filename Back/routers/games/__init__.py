from fastapi import APIRouter
from routers.games import grid
router = APIRouter(prefix="/games")

router.include_router(grid.router)

@router.get("/", response_model=str)
async def get_leagues():
    return "games"