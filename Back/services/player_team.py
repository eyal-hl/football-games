from typing import List

from sqlalchemy import select, join, and_
from unidecode import unidecode
from sqlalchemy.orm import aliased

from models.player_team import PlayerTeamModel
from schemas.player_team import PlayerTeamSchema, PlayerTeamHumanSchema
from models.players import PlayerModel
from services.base import (
    BaseDataManager,
    BaseService,
)


class PlayerTeamService(BaseService):
    def get_playerTeam(self, playerTeam_id: int) -> PlayerTeamSchema:
        """Get playerTeam by ID."""

        return PlayerTeamDataManager(self.session).get_playerTeam(playerTeam_id)

    def search_playerTeams(self, name: str, nationality: str, year: str, player_number: str, age_at_club: str,
                           position: str,
                           team: str) -> List[PlayerTeamSchema]:
        """Search playerTeams by name"""
        return PlayerTeamDataManager(self.session).search_playerTeams(name=name, nationality=nationality, year=year,
                                                                      player_number=player_number,
                                                                      age_at_club=age_at_club, position=position,
                                                                      team=team)


class PlayerTeamDataManager(BaseDataManager):
    def get_playerTeam(self, playerTeam_id: int) -> PlayerTeamSchema:
        stmt = select(PlayerTeamModel).where(PlayerTeamModel.playerTeam_id == playerTeam_id)
        model = self.get_one(stmt)

        return PlayerTeamSchema(**model.to_dict())

    def search_playerTeams(self, name: str, nationality: str, year: str, player_number: str, age_at_club: str,
                           position: str,
                           team: str) -> List[PlayerTeamSchema]:
        schemas: List[PlayerTeamSchema] = list()

        conditions = []

        # Add conditions based on input values
        if name:
            conditions.append(PlayerModel.name_unaccented.like('%' + unidecode(name) + '%'))

        if nationality:
            conditions.append(PlayerModel.nationality.like('%' + nationality + '%'))

        if year:
            conditions.append(PlayerTeamModel.year.like(year))

        if player_number:
            conditions.append(PlayerTeamModel.player_number.like(player_number))

        if age_at_club:
            conditions.append(PlayerTeamModel.age_at_club.like(age_at_club))

        if position:
            conditions.append(PlayerTeamModel.position.like(position))

        if team:
            conditions.append(PlayerTeamModel.team_id.like('%' + team + '%'))

        # Build the final where clause
        where_clause = and_(*conditions)

        stmt = (select(PlayerTeamModel, PlayerModel.name.label('name'), PlayerModel.birth_date.label('birth_date'),
                      PlayerModel.nationality.label('nationality')).select_from(
            join(PlayerTeamModel, PlayerModel, PlayerModel.player_id == PlayerTeamModel.player_id)
        ).where(
            where_clause
        ).order_by(PlayerTeamModel.year, ).add_columns(PlayerModel.name, PlayerModel.nationality, PlayerModel.birth_date).limit(100))

        print(stmt)
        for model in self.get_all(stmt):

            schemas += [PlayerTeamSchema(**model.to_dict())]
        return schemas
