import sqlite3
from datetime import datetime

connection = sqlite3.connect('../db.db')  # Replace with your database connection
cursor = connection.cursor()
# TODO: connect to connections.db, maybe load it to a dict


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


def get_connected_players(node1):
    # TODO: try to read from connections.db(cache), if miss then read from the normal db and write to the connections.db
    cursor.execute(
        """SELECT DISTINCT pt1.player_id
    FROM playerTeam pt1
    JOIN playerTeam pt2 ON pt1.team_id = pt2.team_id AND pt1.year = pt2.year
    WHERE pt2.player_id = ?
      AND pt1.player_id <> ?;""",
        (node1, node1))
    return [a[0] for a in cursor.fetchall()]


def connection_details(node1, node2):
    cursor.execute(
        "select pt1.team_id, pt1.year from playerTeam as pt1 join playerTeam as pt2 on pt1.team_id == pt2.team_id and pt1.year == pt2.year where pt1.player_id == ? and pt2.player_id == ?",
        (node1, node2))
    team_id, year = cursor.fetchone()
    cursor.execute("select name from teams where team_id = ?", (team_id,))
    return (f"{cursor.fetchone()[0]} {str(year)}")


def player_id_to_name(player_id):
    cursor.execute("select name from players where player_id = ?", (player_id,))
    return cursor.fetchone()[0]


def path_to_text(path: list[int]):
    result = ""
    for i in range((len(path) - 1)):
        result += f"{player_id_to_name(path[i])} - {connection_details(path[i], path[i + 1])}\n"
    result += f"{player_id_to_name(path[-1])}"
    return result


start_time = datetime.now()
players_to_ignore = [468539]
path = shortest_path(58342, 58358, players_to_ignore)

print(path_to_text(path))
end_time = datetime.now()
print("Finished in " + str(end_time - start_time))
connection.close()
