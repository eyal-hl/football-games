import sqlite3
from datetime import datetime

db_connection = sqlite3.connect('../db.db')
cursor = db_connection.cursor()


def shortest_path(node1, node2, nodes_to_ignore):
    path_list = [[node1]]
    path_index = 0
    # To keep track of previously visited nodes
    previous_nodes = {node1}
    if node1 == node2:
        return path_list[0]

    while path_index < len(path_list):
        current_path = path_list[path_index]
        last_node = current_path[-1]
        next_nodes = get_connected_players(last_node)
        # Search goal node
        if node2 in next_nodes:
            current_path.append(node2)
            return current_path
        # Add new paths
        for next_node in next_nodes:
            if next_node in nodes_to_ignore:
                previous_nodes.add(next_node)
            elif not next_node in previous_nodes:
                new_path = current_path[:]
                new_path.append(next_node)
                path_list.append(new_path)
                # To avoid backtracking
                previous_nodes.add(next_node)
        # Continue to next path in list
        path_index += 1
    # No path is found
    return []


def bi_directional_search(start, goal, players_to_ignore, teams_to_ignore):
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

            current_neighbours = set(get_connected_players(vertex, teams_to_ignore)) - inactive_vertices
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
    return None


def get_connected_players(node1, teams_to_ignore):
    cursor.execute(
        f"""SELECT DISTINCT pt1.player_id
    FROM playerTeam pt1
    JOIN playerTeam pt2 ON pt1.team_id = pt2.team_id AND pt1.year = pt2.year
    WHERE pt2.player_id = {node1}
      AND pt1.player_id <> {node1}
      AND pt1.team_id not in ({teams_to_ignore});""")
    connections = [a[0] for a in cursor.fetchall()]
    return connections


def connection_details(node1, node2):
    cursor.execute(
        "select pt1.team_id, pt1.year, pt1.age_at_club, pt2.age_at_club from playerTeam as pt1 join playerTeam as pt2 on pt1.team_id == pt2.team_id and pt1.year == pt2.year where pt1.player_id == ? and pt2.player_id == ? order by pt1.year desc limit 1",
        (node1, node2))
    team_id, year, player1_age, player2_age = cursor.fetchone()
    cursor.execute("select name from teams where team_id = ?", (team_id,))
    return (f"{cursor.fetchone()[0]} {str(year)}", player1_age, player2_age)


def player_id_to_name(player_id):
    cursor.execute("select name from players where player_id = ?", (player_id,))
    return cursor.fetchone()[0]


def path_to_text(path: list[int]):
    result = ""
    max_name1_length = max(len(player_id_to_name(player_id)) for player_id in path[:-1])
    max_name2_length = max(len(player_id_to_name(player_id)) for player_id in path[1:])

    for i in range(len(path) - 1):
        team, player1_age, player2_age = connection_details(path[i], path[i + 1])
        player1_name = player_id_to_name(path[i])
        player2_name = player_id_to_name(path[i + 1])

        # Calculate the number of spaces for indentation

        # Construct the formatted line
        result += f"{player1_name}({player1_age}){' ' * (max_name1_length - len(player1_name))} + {player2_name}({player2_age}){' ' * (max_name2_length - len(player2_name))} - {team}\n"
    result = result[:-1]
    return result


start_time = datetime.now()
src_player_id = 14273
dst_player_id = 4248
players_to_ignore = []
teams_to_ignore = []
teams_to_ignore = ','.join([f"'{team}'" for team in teams_to_ignore])

amount_of_paths = 1
for i in range(amount_of_paths):
    path_start_time = datetime.now()
    path = bi_directional_search(src_player_id , dst_player_id, players_to_ignore, teams_to_ignore)
    print(path_to_text(path))
    path_end_time = datetime.now()
    print(f"Path took  {str(path_end_time - path_start_time)}\n")
    players_to_ignore += path[1:-1]
end_time = datetime.now()
print("Finished in " + str(end_time - start_time))
db_connection.close()
