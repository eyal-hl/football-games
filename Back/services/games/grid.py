from typing import List

from sqlalchemy import select, func, desc
from sqlalchemy.orm import aliased

from models.player_team import PlayerTeamModel
from models.players import PlayerModel
from models.teams import TeamModel
from schemas.players import PlayersSlimSchema
from services.base import (
    BaseDataManager,
    BaseService,
)


class GridService(BaseService):
    async def all_answers(self, team1: str, team2: str, nationality: str, league1: str, league2: str) -> (
            List)[PlayersSlimSchema]:
        return await GridDataManager(self.session).all_answers(team1=team1, team2=team2, nationality=nationality,
                                                               league1=league1, league2=league2)


class GridDataManager(BaseDataManager):
    async def all_answers(self, team1: str, team2: str, nationality: str, league1: str, league2) -> (
            List)[PlayersSlimSchema]:
        schemas: List[PlayersSlimSchema] = []

        if team1 and team2:
            stmt = (
                select(PlayerModel).join(PlayerTeamModel,
                                         onclause=PlayerTeamModel.player_id == PlayerModel.player_id)
                .where(
                    PlayerTeamModel.team_id.in_([team1, team2])
                )
                .order_by(desc(PlayerTeamModel.year))
                .group_by(PlayerModel.player_id)
                .having(func.count(func.distinct(PlayerTeamModel.team_id)) == 2)
            )
        elif team1 and nationality:
            stmt = (
                select(PlayerModel).join(PlayerTeamModel,
                                         onclause=PlayerTeamModel.player_id == PlayerModel.player_id)
                .where(
                    PlayerTeamModel.team_id == team1
                ).where(PlayerModel.nationality == nationality)
                .distinct()
                .order_by(desc(PlayerTeamModel.year))
            )
        elif team1 and league1:
            pt2 = aliased(PlayerTeamModel)
            stmt = (
                select(PlayerModel)
                .join(PlayerTeamModel, PlayerModel.player_id == PlayerTeamModel.player_id)
                .join(pt2, PlayerModel.player_id == pt2.player_id)
                .join(TeamModel, pt2.team_id == TeamModel.team_id)
                .where(PlayerTeamModel.team_id == team1)
                .where(TeamModel.league_id == league1)
                .distinct()
                .order_by(desc(PlayerTeamModel.year))
            )
        elif nationality and league1:
            stmt = (
                select(PlayerModel).join(PlayerTeamModel,
                                         onclause=PlayerTeamModel.player_id == PlayerModel.player_id)
                .join(TeamModel, onclause=PlayerTeamModel.team_id == TeamModel.team_id)
                .where(
                    TeamModel.league_id == league1
                ).where(PlayerModel.nationality == nationality)
                .distinct()
                .order_by(desc(PlayerTeamModel.year))
            )
        elif league1 and league2:
            stmt = (
                select(PlayerModel).join(PlayerTeamModel,
                                         onclause=PlayerTeamModel.player_id == PlayerModel.player_id)
                .join(TeamModel, onclause=PlayerTeamModel.team_id == TeamModel.team_id)
                .where(
                    TeamModel.league_id.in_([league1, league2])
                )
                .group_by(PlayerModel.player_id)
                .having(func.count(func.distinct(TeamModel.league_id)) == 2)
                .order_by(desc(PlayerTeamModel.year))
            )
        else:
            raise 'error'

        for model in await self.get_all(stmt):
            schemas.append(PlayersSlimSchema(**model.to_dict()))

        return schemas
