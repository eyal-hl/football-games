from typing import List

from sqlalchemy import select, desc, func, and_, not_
from sqlalchemy.orm import aliased

from models.leagues import LeagueModel
from models.player_team import PlayerTeamModel
from schemas.player_team import PlayerTeamSchema
from schemas.players import PlayersSlimSchema
from schemas.teams import ConnectionSchema
from models.teams import TeamModel
from services.players import PlayerDataManager
from services.base import (
    BaseDataManager,
    BaseService,
)
from utils import format_team_years
import asyncio

class connectedPlayersService(BaseService):
    async def get_connection_details(self, player1: int, player2: int) -> List[ConnectionSchema]:
        return await connectedPlayersManager(self.session).getConnection(player1, player2)


    async def get_path(self, player1: int, player2: int, players_to_ignore: list[int], teams_to_ignore: list[str]) -> List[
        PlayersSlimSchema]:
        return await connectedPlayersManager(self.session).getPath(player1=player1, player2=player2,
                                                                   players_to_ignore=players_to_ignore,
                                                                   teams_to_ignore=teams_to_ignore)


class connectedPlayersManager(BaseDataManager):
    async def getConnection(self, player1: int, player2: int) -> List[ConnectionSchema]:
        pt1 = aliased(PlayerTeamModel)
        pt2 = aliased(PlayerTeamModel)

        stmt = select(pt1, TeamModel.name, TeamModel.team_id).join(pt2, onclause=and_(
            pt1.team_id == pt2.team_id, pt1.year == pt2.year)).join(
            TeamModel, onclause=pt1.team_id == TeamModel.team_id).where(
            and_(pt1.player_id == player1, pt2.player_id == player2)).group_by(pt1.team_id, pt1.year)

        results = []
        models = await asyncio.create_task(self.session.execute(stmt))
        for model in models.fetchall():
            results.append({'team_id': model[2], 'team_name': model[1], 'year': model[0].to_dict()['year']})
        formatted = format_team_years(results)
        return [ConnectionSchema(**a) for a in formatted]

    async def getPath(self, player1: int, player2: int, players_to_ignore: list[int], teams_to_ignore: list[str]) -> \
    List[
        PlayersSlimSchema]:
        path = await self._bi_directional_search(player1, player2, players_to_ignore, teams_to_ignore)
        result = []
        for id in path:
            result.append(await PlayerDataManager(self.session).get_player(id))
        return result

    async def _get_connected_players(self, player, teams_to_ignore):
        pt1 = aliased(PlayerTeamModel)
        pt2 = aliased(PlayerTeamModel)
        stmt = (select(func.distinct(pt1.player_id)).join(pt2, onclause=and_(pt1.team_id == pt2.team_id,
                                                                             pt1.year == pt2.year))
                .where(and_(pt2.player_id == player, pt1.player_id != player, not_(pt1.team_id.in_(teams_to_ignore)))))
        response = await asyncio.create_task(self.session.execute(stmt))

        return [row[0] for row in response.fetchall()]

    async def _bi_directional_search(self, start, goal, players_to_ignore, teams_to_ignore):
        # Check if start and goal are equal.
        if start == goal:
            return [start]
        # Get dictionary of currently active vertices with their corresponding paths.
        active_vertices_path_dict = {start: [start], goal: [goal]}
        # Vertices we have already examined.
        inactive_vertices = set(players_to_ignore)
        while len(active_vertices_path_dict) > 0:
            # Make a copy of active vertices so we can modify the original dictionary as we go.
            active_vertices = list(active_vertices_path_dict.keys())
            for vertex in active_vertices:
                # Get the path to where we are.
                current_path = active_vertices_path_dict[vertex]
                # Record whether we started at start or goal.
                origin = current_path[0]
                # Check for new neighbours.

                current_neighbours = set(await self._get_connected_players(vertex, teams_to_ignore)) - inactive_vertices
                # Check if our neighbours hit an active vertex
                if len(current_neighbours.intersection(active_vertices)) > 0:
                    for meeting_vertex in current_neighbours.intersection(active_vertices):
                        # Check the two paths didn't start at same place. If not, then we've got a path from start to goal.
                        if origin != active_vertices_path_dict[meeting_vertex][0]:
                            # Reverse one of the paths.
                            active_vertices_path_dict[meeting_vertex].reverse()
                            # return the combined results
                            return active_vertices_path_dict[vertex] + active_vertices_path_dict[meeting_vertex]
                # No hits, so check for new neighbours to extend our paths.
                if len(set(current_neighbours) - inactive_vertices - set(active_vertices)) == 0:
                    # If none, then remove the current path and record the endpoint as inactive.
                    active_vertices_path_dict.pop(vertex, None)
                    inactive_vertices.add(vertex)
                else:
                    # Otherwise extend the paths, remove the previous one and update the inactive vertices.
                    for neighbour_vertex in current_neighbours - inactive_vertices - set(active_vertices):
                        active_vertices_path_dict[neighbour_vertex] = current_path + [neighbour_vertex]
                        active_vertices.append(neighbour_vertex)
                    active_vertices_path_dict.pop(vertex, None)
                    inactive_vertices.add(vertex)
        return []
