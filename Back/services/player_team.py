from typing import List

from sqlalchemy import select, and_, desc, asc, func

from unidecode import unidecode
from models.player_team import PlayerTeamModel
from schemas.player_team import PlayerTeamSchema, CombinedPlayerTeamSchema
from models.players import PlayerModel
from models.teams import TeamModel
from models.leagues import LeagueModel
from services.base import (
    BaseDataManager,
    BaseService,
)
from datetime import date


class PlayerTeamService(BaseService):
    def get_playerTeam(self, player_id: int) -> List[PlayerTeamSchema]:
        """Get playerTeam by ID."""

        return PlayerTeamDataManager(self.session).get_playerTeam(player_id)

    def search_playerTeams(self, name: str, nationality: str, year: str, player_number: str, age_at_club: str,
                           position: str,
                           team: str, team_id: str, league: str, league_id: str) -> List[CombinedPlayerTeamSchema]:
        """Search playerTeams by name"""
        return PlayerTeamDataManager(self.session).search_playerTeams(name=name, nationality=nationality, year=year,
                                                                      player_number=player_number,
                                                                      age_at_club=age_at_club, position=position,
                                                                      team=team, team_id=team_id, league=league,
                                                                      league_id=league_id)


class PlayerTeamDataManager(BaseDataManager):
    def get_playerTeam(self, player_id: int) -> List[PlayerTeamSchema]:
        stmt = select(PlayerTeamModel).where(PlayerTeamModel.player_id == player_id)
        schemas = []
        for model in self.get_all(stmt):
            schemas += [PlayerTeamSchema(**model.to_dict())]
        return schemas

    def search_playerTeams(self, name: str, nationality: str, year: str, player_number: str, age_at_club: str,
                           position: str, team: str, team_id: str, league: str, league_id: str) -> List[
        CombinedPlayerTeamSchema]:
        schemas: List[CombinedPlayerTeamSchema] = []

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

        if team_id:
            conditions.append(PlayerTeamModel.team_id.ilike('%' + team_id + "%"))

        if league:
            conditions.append(LeagueModel.name.ilike('%' + league + "%"))

        if league_id:
            conditions.append(TeamModel.league_id.ilike('%' + league_id + "%"))

        # Build the final where clause

        if len(conditions) == 0:
            return [CombinedPlayerTeamSchema(name='name', nationality='nationality',
                                             team='name', player_number=0, age_at_club=0,
                                             position='Attacking Midfield, Central Midfield, Centre-Back, Centre-Forward, Defender, Defensive Midfield, Goalkeeper, Left Midfield, Left Winger, Left-Back, Mittelfeld, Right Midfield, Right Winger, Right-Back, Second Striker, Striker, Sweeper',
                                             birth_date=date(2001, 4, 3), years="year", league='name', team_id='team_id',
                                             league_id='league_id', player_id=0
                                             )]

        where_clause = and_(*conditions)

        stmt = (
            select(PlayerTeamModel, PlayerModel, TeamModel, LeagueModel, func.min(PlayerTeamModel.year), func.max(PlayerTeamModel.year))
            .join(PlayerModel, onclause=PlayerTeamModel.player_id == PlayerModel.player_id)
            .join(TeamModel, onclause=PlayerTeamModel.team_id == TeamModel.team_id)
            .join(LeagueModel, onclause=TeamModel.league_id == LeagueModel.league_id)
            .where(where_clause)
            .order_by(desc(PlayerTeamModel.year), asc(PlayerTeamModel.player_number))
            .group_by(PlayerTeamModel.player_id, PlayerTeamModel.team_id)
            .limit(100)
        )
        result = self.session.execute(stmt)
        for row in result.fetchall():
            playerTeam: dict = row[0].to_dict()
            player: dict = row[1].to_dict()
            team: dict = row[2].to_dict()
            league: dict = row[3].to_dict()
            schemas += [
                CombinedPlayerTeamSchema(player_id=playerTeam['player_id'], team_id=playerTeam['team_id'], years=f"{row[4]} - {row[5]}",
                                         player_number=playerTeam['player_number'],
                                         age_at_club=playerTeam['age_at_club'], position=playerTeam['position'],
                                         name=player['name'], nationality=player['nationality'],
                                         team=team['name'],
                                         birth_date=player['birth_date'],
                                         league_id=team['league_id'],
                                         league=league['name'])]
        return schemas
