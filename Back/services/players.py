from typing import List,Optional

from sqlalchemy import select
from unidecode import unidecode


from models.players import PlayerModel
from schemas.players import PlayerSchema, PlayersSlimSchema
from services.base import (
    BaseDataManager,
    BaseService,
)


class PlayerService(BaseService):
    def get_player(self, player_id: int) -> PlayerSchema:
        """Get player by ID."""

        return PlayerDataManager(self.session).get_player(player_id)

    def get_players(self) -> List[PlayerSchema]:
        """Select all players"""

        return PlayerDataManager(self.session).get_players()

    def search_players(self, name: str, nationality: str) -> List[PlayersSlimSchema]:
        """Search players by name"""
        return PlayerDataManager(self.session).search_players(name=name, nationality=nationality)

    def get_nationalities(self) -> List[str]:
        return PlayerDataManager(self.session).get_nationalities()


class PlayerDataManager(BaseDataManager):
    def get_player(self, player_id: int) -> PlayerSchema:
        stmt = select(PlayerModel).where(PlayerModel.player_id == player_id)
        model = self.get_one(stmt)

        return PlayerSchema(**model.to_dict())

    def get_players(self) -> List[PlayerSchema]:
        schemas: List[PlayerSchema] = list()

        stmt = select(PlayerModel).limit(100)

        for model in self.get_all(stmt):
            schemas += [PlayerSchema(**model.to_dict())]

        return schemas

    def search_players(self, name: str, nationality: str) -> List[PlayersSlimSchema]:
        schemas: List[PlayersSlimSchema] = list()
        stmt = select(PlayerModel).where(PlayerModel.name_unaccented.like('%' + unidecode(name) + '%')).where(PlayerModel.nationality.like('%'+nationality+'%')).limit(100)
        for model in self.get_all(stmt):
            schemas += [PlayersSlimSchema(**model.to_dict())]
        return schemas

    def get_nationalities(self) -> list[str]:
        stmt = select(PlayerModel.nationality).group_by(PlayerModel.nationality)
        result = self.get_all(stmt)
        result.remove(None)
        return result
