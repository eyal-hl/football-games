from typing import List

from sqlalchemy import select, and_, func

from models.player_team import PlayerTeamModel
from models.players import PlayerModel
from models.teams import TeamModel
from schemas.players import PlayersSlimSchema
from services.base import (
    BaseDataManager,
    BaseService,
)


class GridService(BaseService):
    def all_answers(self, team1: str, team2: str, nationality: str, league1: str, league2: str) -> List[
        PlayersSlimSchema]:

        return GridDataManager(self.session).all_answers(team1=team1, team2=team2, nationality=nationality,
                                                         league1=league1, league2=league2)

class GridDataManager(BaseDataManager):
    def all_answers(self, team1: str, team2: str, nationality: str, league1: str, league2) -> List[
        PlayersSlimSchema]:
        schemas: List[PlayersSlimSchema] = list()

        if team1 and team2:
            stmt = (
                select(PlayerModel).join(PlayerTeamModel,
                                         onclause=PlayerTeamModel.player_id == PlayerModel.player_id)
                .where(
                    PlayerTeamModel.team_id.in_([team1, team2])
                )
                .group_by(PlayerModel.player_id)
                .having(func.count(func.distinct(PlayerTeamModel.team_id)) == 2)
            )
        elif team1 and nationality:
            pass
        elif team1 and league1:
            pass
        elif nationality and league1:
            pass
        elif league1 and league2:
            pass
        else:
            raise 'error'

        for model in self.get_all(stmt):
            schemas.append(PlayersSlimSchema(**model.to_dict()))

        return schemas
