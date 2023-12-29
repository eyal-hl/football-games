from typing import List

from sqlalchemy import select, join, and_

from unidecode import unidecode
from models.player_team import PlayerTeamModel
from schemas.player_team import PlayerTeamSchema, CombinedPlayerTeamSchema
from models.players import PlayerModel
from models.teams import TeamModel
from services.base import (
    BaseDataManager,
    BaseService,
)


class PlayerTeamService(BaseService):
    def get_playerTeam(self, player_id: int) -> List[PlayerTeamSchema]:
        """Get playerTeam by ID."""

        return PlayerTeamDataManager(self.session).get_playerTeam(player_id)

    def search_playerTeams(self, name: str, nationality: str, year: str, player_number: str, age_at_club: str,
                           position: str,
                           team: str) -> List[CombinedPlayerTeamSchema]:
        """Search playerTeams by name"""
        return PlayerTeamDataManager(self.session).search_playerTeams(name=name, nationality=nationality, year=year,
                                                                      player_number=player_number,
                                                                      age_at_club=age_at_club, position=position,
                                                                      team=team)


class PlayerTeamDataManager(BaseDataManager):
    def get_playerTeam(self, player_id: int) -> List[PlayerTeamSchema]:
        stmt = select(PlayerTeamModel).where(PlayerTeamModel.player_id == player_id)
        schemas = []
        for model in self.get_all(stmt):
            schemas += [PlayerTeamSchema(**model.to_dict())]
        return schemas

    def search_playerTeams(self, name: str, nationality: str, year: str, player_number: str, age_at_club: str,
                           position: str, team: str) -> List[CombinedPlayerTeamSchema]:
        schemas: List[CombinedPlayerTeamSchema] = list()

        conditions = []

        # Add conditions based on input values
        if name:
            conditions.append(PlayerModel.name_unaccented.ilike('%' + unidecode(name) + '%'))

        if nationality:
            conditions.append(PlayerModel.nationality.ilike('%' + nationality + '%'))

        if year:
            conditions.append(PlayerTeamModel.year.like(year))

        if player_number:
            conditions.append(PlayerTeamModel.player_number.like(player_number))

        if age_at_club:
            conditions.append(PlayerTeamModel.age_at_club.like(age_at_club))

        if position:
            conditions.append(PlayerTeamModel.position.like(position))

        if team:
            conditions.append(TeamModel.name.ilike('%' + team + "%"))

        # Build the final where clause
        where_clause = and_(*conditions)

        stmt = (
            select(PlayerTeamModel, PlayerModel, TeamModel)
            .join(PlayerModel, onclause=PlayerTeamModel.player_id == PlayerModel.player_id)
            .join(TeamModel, onclause=PlayerTeamModel.team_id == TeamModel.team_id)
            .where(where_clause)
            .order_by(PlayerTeamModel.year)
            .limit(100)
        )
        result = self.session.execute(stmt)
        for row in result.fetchall():
            playerTeam: dict = row[0].to_dict()
            player: dict = row[1].to_dict()
            team: dict = row[2].to_dict()
            schemas += [CombinedPlayerTeamSchema(**playerTeam, name=player['name'], nationality=player['nationality'], team=team['name'],
                              birth_date=player['birth_date'])]
        return schemas
