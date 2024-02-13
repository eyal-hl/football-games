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

        if POSSIBLE_GRID_TYPES.index(type1) > POSSIBLE_GRID_TYPES.index(type2):
            type1, value1, type2, value2 = type2, value2, type1, value1

        pl = aliased(PlayerModel)
        pt1 = aliased(PlayerTeamModel)
        pt2 = aliased(PlayerTeamModel)
        pt3 = aliased(PlayerTeamModel)
        pt4 = aliased(PlayerTeamModel)
        tm1 = aliased(TeamModel)
        tm2 = aliased(TeamModel)
        st1 = aliased(SpecialTeamModel)
        st2 = aliased(SpecialTeamModel)

        match (type1, type2):
            case ('nationality', 'team' | 'league' | 'title' | 'manager'):
                stmt = (select(pl).join(pt1,
                                        onclause=pt1.player_id == pl.player_id)
                .join(tm1, onclause=pt1.team_id == tm1.team_id)
                .outerjoin(st1, onclause=and_(pt1.team_id == st1.team_id,
                                              pt1.year == st1.year))
                .where(
                    and_(pl.nationality == value1,
                         get_where_clause(type2, value2, pt1, tm1, st1))))
            case ('team' | 'league' | 'title' | 'manager', 'team' | 'league' | 'title' | 'manager'):
                stmt = (select(pl).join(pt1, onclause=pt1.player_id == pl.player_id)
                        .join(pt2, onclause=pt1.player_id == pt2.player_id)
                        .join(tm1, onclause=pt1.team_id == tm1.team_id)
                        .join(tm2, onclause=pt2.team_id == tm2.team_id)
                        .outerjoin(st1, onclause=and_(pt1.team_id == st1.team_id, pt1.year == st1.year))
                        .outerjoin(st2, onclause=and_(pt2.team_id == st2.team_id, pt2.year == st2.year))
                        .where(and_(get_where_clause(type1, value1, pt1, tm1, st1),
                                    get_where_clause(type2, value2, pt2, tm2, st2))))
            case ('nationality', 'player'):
                stmt = (select(pl).join(pt1, onclause=pt1.player_id == pl.player_id)
                        .join(pt2, onclause=and_(pt1.team_id == pt2.team_id, pt1.year == pt2.year))
                        .where(and_(pl.nationality == value1, pt2.player_id == value2)))
            case ('team' | 'league' | 'title' | 'manager', 'player'):
                stmt = (select(pl).where(pl.player_id != value2).join(pt1, onclause=pt1.player_id == pl.player_id)
                        .join(pt2, onclause=pt1.player_id == pt2.player_id)
                        .join(pt3,
                              onclause=and_(pt2.team_id == pt3.team_id, pt2.year == pt3.year,
                                            pt3.player_id == value2))
                        .join(tm1, onclause=pt1.team_id == tm1.team_id)
                        .outerjoin(st1, onclause=and_(pt1.team_id == st1.team_id, pt1.year == st1.year))
                        .where(get_where_clause(type1, value1, pt1, tm1, st1))
                        )
            case ('player', 'player'):
                stmt = (select(pl).where(and_(pl.player_id != value1, pl.player_id != value2)).join(pt1,
                                                                                                    onclause=pt1.player_id == pl.player_id)
                        .join(pt2,
                              onclause=pt1.player_id == pt2.player_id)
                        .join(pt3,
                              onclause=and_(pt1.team_id == pt3.team_id, pt1.year == pt3.year, pt3.player_id == value1))
                        .join(pt4,
                              onclause=and_(pt2.team_id == pt4.team_id, pt2.year == pt4.year, pt4.player_id == value2)))
            case _:
                print('error', type1, type2, value1, value2)
                raise 'error'

        for model in await self.get_all(stmt.distinct()):
            schemas.append(PlayersSlimSchema(**model.to_dict()))

        return schemas
