from typing import List, Optional

from sqlalchemy import select
from unidecode import unidecode

from models.player_team import PlayerTeamModel
from models.players import PlayerModel
from models.teams import TeamModel
from schemas.players import PlayerSchema, PlayersSlimSchema
from services.base import (
    BaseDataManager,
    BaseService,
)


class PlayerService(BaseService):
    async def get_player(self, player_id: int) -> PlayersSlimSchema:
        """Get player by ID."""

        return await PlayerDataManager(self.session).get_player(player_id)

    async def get_players(self) -> List[PlayersSlimSchema]:
        """Select all players"""

        return await PlayerDataManager(self.session).get_players()

    async def search_players(self, name: str, search_from_middle: bool) -> List[PlayersSlimSchema]:
        """Search players by name"""
        return await PlayerDataManager(self.session).search_players(name=name, search_from_middle=search_from_middle)

    async def get_nationalities(self) -> List[str]:
        return await PlayerDataManager(self.session).get_nationalities()

    async def get_players_by_league(self, league_id: str, year: int) -> List[PlayersSlimSchema]:
        return await PlayerDataManager(self.session).get_players_by_league(league_id, year)

    async def get_players_by_team(self, team_id: str, year: int) -> List[PlayersSlimSchema]:
        return await PlayerDataManager(self.session).get_players_by_team(team_id, year)


class PlayerDataManager(BaseDataManager):
    async def get_player(self, player_id: int) -> PlayersSlimSchema:
        stmt = select(PlayerModel).where(PlayerModel.player_id == player_id)
        model = await self.get_one(stmt)

        return PlayersSlimSchema(**model.to_dict())

    async def get_players(self) -> List[PlayersSlimSchema]:
        schemas: List[PlayersSlimSchema] = list()

        stmt = select(PlayerModel).order_by(PlayerModel.birth_date.desc())

        for model in await self.get_all(stmt):
            schemas += [PlayersSlimSchema(**model.to_dict())]

        return schemas

    async def search_players(self, name: str, search_from_middle: bool) -> List[PlayersSlimSchema]:
        schemas: List[PlayersSlimSchema] = list()
        stmt = select(PlayerModel).where(
            PlayerModel.name_unaccented.like(('%' if search_from_middle else '') + unidecode(name) + '%')).limit(1000)
        for model in await self.get_all(stmt):
            schemas += [PlayersSlimSchema(**model.to_dict())]
        return schemas

    async def get_nationalities(self) -> list[str]:
        stmt = select(PlayerModel.nationality).group_by(
            PlayerModel.nationality)
        result = await self.get_all(stmt)
        result.remove(None)
        return result

    async def get_players_by_league(self, league_id: str, year: int) -> List[PlayersSlimSchema]:
        schemas: List[PlayersSlimSchema] = list()
        stmt = (select(PlayerModel)
                .join(PlayerTeamModel, onclause=PlayerModel.player_id == PlayerTeamModel.player_id)
                .join(TeamModel, onclause=PlayerTeamModel.team_id == TeamModel.team_id)
                .where(TeamModel.league_id == league_id, PlayerTeamModel.year == year)).distinct()
        for model in await self.get_all(stmt):
            schemas += [PlayersSlimSchema(**model.to_dict())]
        return schemas

    async def get_players_by_team(self, team_id: str, year: int) -> List[PlayersSlimSchema]:
        schemas: List[PlayersSlimSchema] = list()
        stmt = (select(PlayerModel)
                .join(PlayerTeamModel, onclause=PlayerModel.player_id == PlayerTeamModel.player_id)
                .where(PlayerTeamModel.team_id == team_id, PlayerTeamModel.year == year)).distinct()
        for model in await self.get_all(stmt):
            schemas += [PlayersSlimSchema(**model.to_dict())]
        return schemas
