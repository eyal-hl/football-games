from typing import List

from sqlalchemy import select, desc, func, and_
from sqlalchemy.orm import aliased

from models.leagues import LeagueModel
from models.player_team import PlayerTeamModel
from schemas.player_team import PlayerTeamSchema
from schemas.teams import ConnectionSchema
from models.teams import TeamModel
from services.base import (
    BaseDataManager,
    BaseService,
)
from utils import format_team_years


class connectedPlayersService(BaseService):
    def get_connection_details(self, player1: int, player2: int) -> List[ConnectionSchema]:
        """Get movie by ID."""

        return connectedPlayersManager(self.session).getConnection(player1, player2)

    def get_path(self) -> List[PlayerTeamSchema]:
        """Select movies with filter by ``year`` and ``rating``."""

        return connectedPlayersManager(self.session).getPath()


class connectedPlayersManager(BaseDataManager):
    def getConnection(self, player1: int, player2: int) -> List[ConnectionSchema]:
        pt1 = aliased(PlayerTeamModel)
        pt2 = aliased(PlayerTeamModel)

        stmt = select(pt1, TeamModel.name, TeamModel.team_id).join(pt2, onclause=and_(
            pt1.team_id == pt2.team_id, pt1.year == pt2.year)).join(
            TeamModel, onclause=pt1.team_id == TeamModel.team_id).where(
            and_(pt1.player_id == player1, pt2.player_id == player2)).group_by(pt1.team_id, pt1.year)

        results = []
        models = self.session.execute(stmt)
        for model in models.fetchall():
            results.append({'team_id': model[2], 'team_name': model[1], 'year': model[0].to_dict()['year']})
        formatted = format_team_years(results)
        return [ConnectionSchema(**a) for a in formatted]

    def getPath(self, league_id: str) -> PlayerTeamSchema:
        stmt = select(LeagueModel).where(LeagueModel.league_id == league_id)
        model = self.get_one(stmt)

        return PlayerTeamSchema(**model.to_dict())
