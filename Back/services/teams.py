from typing import List

from sqlalchemy import select

from models.teams import TeamModel
from schemas.teams import TeamSchema
from services.base import BaseDataManager, BaseService


class TeamService(BaseService):
    async def get_team(self, team_id: str) -> TeamSchema:
        """Get team by ID."""
        return await TeamDataManager(self.session).get_team(team_id)

    async def get_teams(self) -> List[TeamSchema]:
        """Select all teams."""
        return await TeamDataManager(self.session).get_teams()

    async def get_teams_by_league(self, league_id: str) -> List[TeamSchema]:
        """Select teams by league."""
        return await TeamDataManager(self.session).get_teams_by_league(league_id)


class TeamDataManager(BaseDataManager):
    async def get_team(self, team_id: str) -> TeamSchema:
        stmt = select(TeamModel).where(TeamModel.team_id == team_id)
        model = await self.get_one(stmt)

        return TeamSchema(**model.to_dict())

    async def get_teams(self) -> List[TeamSchema]:
        schemas: List[TeamSchema] = list()

        stmt = select(TeamModel)

        for model in await self.get_all(stmt):
            schemas += [TeamSchema(**model.to_dict())]

        return schemas

    async def get_teams_by_league(self, league_id: str) -> List[TeamSchema]:
        schemas: List[TeamSchema] = list()

        stmt = select(TeamModel).where(TeamModel.league_id == league_id)

        for model in await self.get_all(stmt):
            schemas += [TeamSchema(**model.to_dict())]

        return schemas
