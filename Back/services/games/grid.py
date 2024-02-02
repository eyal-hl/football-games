from typing import List

from sqlalchemy import select, func, desc, and_
from sqlalchemy.orm import aliased

from models.player_team import PlayerTeamModel
from models.players import PlayerModel
from models.teams import TeamModel
from models.special_team import SpecialTeamModel
from models.specials import SpecialsModel
from schemas.players import PlayersSlimSchema
from services.base import (
    BaseDataManager,
    BaseService,
)
from models.base import SQLModel
from const import POSSIBLE_GRID_TYPES


class GridService(BaseService):
    async def all_answers(self, type1: str, value1: str, type2: str, value2: str) -> (
            List)[PlayersSlimSchema]:
        return await GridDataManager(self.session).all_answers(type1=type1, value1=value1, type2=type2, value2=value2)


def get_where_clause(type: str, value: str, playerTeamModel: PlayerTeamModel, teamModel: TeamModel,
                     specialTeamModel: SpecialTeamModel) -> bool:
    match type:
        case 'team':
            return playerTeamModel.team_id == value
        case 'league':
            return teamModel.league_id == value
        case 'title' | 'manager':
            return specialTeamModel.special_id == value


class GridDataManager(BaseDataManager):
    async def all_answers(self, type1: str, value1: str, type2: str, value2: str) -> (
            List)[PlayersSlimSchema]:
        schemas: List[PlayersSlimSchema] = []

        if (POSSIBLE_GRID_TYPES.index(type1) > POSSIBLE_GRID_TYPES.index(type2)):
            type1, value1, type2, value2 = type2, value2, type1, value1

        match (type1, type2):
            case ('nationality', 'team' | 'league' | 'title' | 'manager'):
                stmt = (select(PlayerModel).join(PlayerTeamModel,
                                                 onclause=PlayerTeamModel.player_id == PlayerModel.player_id)
                .join(TeamModel, onclause=PlayerTeamModel.team_id == TeamModel.team_id)
                .outerjoin(SpecialTeamModel, onclause=and_(PlayerTeamModel.team_id == SpecialTeamModel.team_id,
                                                           PlayerTeamModel.year == SpecialTeamModel.year))
                .where(
                    and_(PlayerModel.nationality == value1,
                         get_where_clause(type2, value2, PlayerTeamModel, TeamModel, SpecialTeamModel))))

            case _:
                print('error', type1, type2, value1, value2)
                raise 'error'

                #     if team1 and team2:
                #     stmt = (
                #     select(PlayerModel).join(PlayerTeamModel,
                #                              onclause=PlayerTeamModel.player_id == PlayerModel.player_id)
                # .where(
                #     PlayerTeamModel.team_id.in_([team1, team2])
                # )
                # .order_by(desc(PlayerTeamModel.year))
                # .group_by(PlayerModel.player_id)
                # .having(func.count(func.distinct(PlayerTeamModel.team_id)) == 2)
                # )
                # elif team1 and nationality:
                # stmt = (
                #     select(PlayerModel).join(PlayerTeamModel,
                #                              onclause=PlayerTeamModel.player_id == PlayerModel.player_id)
                #     .where(
                #         PlayerTeamModel.team_id == team1
                #     ).where(PlayerModel.nationality == nationality)
                #     .distinct()
                #     .order_by(desc(PlayerTeamModel.year))
                # )
                # elif team1 and league1:
                # pt2 = aliased(PlayerTeamModel)
                # stmt = (
                #     select(PlayerModel)
                #     .join(PlayerTeamModel, PlayerModel.player_id == PlayerTeamModel.player_id)
                #     .join(pt2, PlayerModel.player_id == pt2.player_id)
                #     .join(TeamModel, pt2.team_id == TeamModel.team_id)
                #     .where(PlayerTeamModel.team_id == team1)
                #     .where(TeamModel.league_id == league1)
                #     .distinct()
                #     .order_by(desc(PlayerTeamModel.year))
                # )
                # elif nationality and league1:
                # stmt = (
                #     select(PlayerModel).join(PlayerTeamModel,
                #                              onclause=PlayerTeamModel.player_id == PlayerModel.player_id)
                #     .join(TeamModel, onclause=PlayerTeamModel.team_id == TeamModel.team_id)
                #     .where(
                #         TeamModel.league_id == league1
                #     ).where(PlayerModel.nationality == nationality)
                #     .distinct()
                #     .order_by(desc(PlayerTeamModel.year))
                # )
                # elif league1 and league2:
                # stmt = (
                #     select(PlayerModel).join(PlayerTeamModel,
                #                              onclause=PlayerTeamModel.player_id == PlayerModel.player_id)
                #     .join(TeamModel, onclause=PlayerTeamModel.team_id == TeamModel.team_id)
                #     .where(
                #         TeamModel.league_id.in_([league1, league2])
                #     )
                #     .group_by(PlayerModel.player_id)
                #     .having(func.count(func.distinct(TeamModel.league_id)) == 2)
                #     .order_by(desc(PlayerTeamModel.year))
                # )
                # else:
                # raise 'error'

        for model in await self.get_all(stmt.distinct().limit(100)):
            schemas.append(PlayersSlimSchema(**model.to_dict()))

        return schemas
