from typing import List

from sqlalchemy import select

from models.leagues import LeagueModel
from schemas.leagues import LeagueSchema
from services.base import (
    BaseDataManager,
    BaseService,
)


class LeagueService(BaseService):
    async def get_league(self, league_id: str) -> LeagueSchema:
        """Get movie by ID."""

        return await LeagueDataManager(self.session).get_league(league_id)

    async def get_leagues(self) -> List[LeagueSchema]:
        """Select movies with filter by ``year`` and ``rating``."""

        return await LeagueDataManager(self.session).get_leagues()


class LeagueDataManager(BaseDataManager):
    async def get_league(self, league_id: str) -> LeagueSchema:
        stmt = select(LeagueModel).where(LeagueModel.league_id == league_id)
        model = await self.get_one(stmt)

        return LeagueSchema(**model.to_dict())

    async def get_leagues(self) -> List[LeagueSchema]:
        schemas: List[LeagueSchema] = list()

        stmt = select(LeagueModel)

        for model in await self.get_all(stmt):
            schemas += [LeagueSchema(**model.to_dict())]

        return schemas
