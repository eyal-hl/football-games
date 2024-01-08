import requests
from bs4 import BeautifulSoup
from const import HEADERS, BASE_URL, DB_PATH
import time
import sqlite3
from datetime import datetime
from unidecode import unidecode

RUN_LAST_YEAR_AGAIN = False


# Custom adapter for datetime objects
def adapt_datetime(dt):
    return dt.strftime("%Y-%m-%d")


# Register the adapter
sqlite3.register_adapter(datetime, adapt_datetime)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


def handle_teams(teams_list):
    conn.commit()
    insert_teams_to_teams_table(cursor, teams_list)
    conn.commit()
    for team in teams_list:
        players, players_team = get_players_from_team(team[2], team[3])
        insert_player_team_to_player_team_table(cursor, players_team)
        conn.commit()
        insert_players_to_players_table(cursor, players)
        conn.commit()


def create_teams_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            name TEXT UNIQUE,
            league_id TEXT,
            ref TEXT,
            team_id TEXT UNIQUE PRIMARY KEY,
            img_ref TEXT
        );
    ''')


def create_players_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            player_id INTEGER UNIQUE PRIMARY KEY,
            name TEXT,
            name_unaccented TEXT,  
            img_ref TEXT,
            birth_date DATE,
            nationality TEXT,
            ref TEXT
        );
    ''')


def create_player_team_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS playerTeam (
            player_id INTEGER,
            year INTEGER,
            player_number INTEGER,
            team_id TEXT,
            age_at_club INTEGER,
            position TEXT,
            PRIMARY KEY (player_id, year, team_id),
            FOREIGN KEY (player_id) REFERENCES players(player_id),
            FOREIGN KEY (team_id) REFERENCES teams(team_id)
        );
    ''')


def create_leagues_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leagues (
            name TEXT UNIQUE,
            league_id TEXT UNIQUE PRIMARY KEY,
            ref TEXT,
            img_ref TEXT
        );
    ''')


def insert_teams_to_teams_table(cursor, teams_list):
    cursor.executemany('''
        INSERT OR IGNORE INTO teams (name, league_id, ref, team_id, img_ref)
        VALUES (?, ?, ?, ?, ?);
    ''', teams_list)


def insert_players_to_players_table(cursor, players_list):
    # Modify the query to include the new column
    cursor.executemany('''
        INSERT OR IGNORE INTO players (player_id, name, name_unaccented, img_ref, birth_date, nationality, ref)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    ''', [(player[0], player[1], unidecode(player[1]), player[2], player[3], player[4], player[5]) for player in players_list])


def insert_player_team_to_player_team_table(cursor, player_team_list):
    cursor.executemany('''
        INSERT OR IGNORE INTO playerTeam (player_id, year, player_number, team_id, age_at_club, position)
        VALUES (?, ?, ?, ?, ?, ?);
    ''', player_team_list)


def insert_league_to_leagues_table(cursor, name, ref, img_ref):
    cursor.execute('''
        INSERT INTO leagues (name, league_id, ref, img_ref)
        VALUES (?, ?, ?, ?);
    ''', (name, ref.split('/')[1].replace('-', '_'), ref, img_ref))

def get_max_year_from_team(cursor, team):
    cursor.execute('''select max(year) from playerTeam where team_id = ?''', (team,))
    return cursor.fetchone()[0]


def get_players_from_team(team_url, team_id):
    year = int(team_url.split("/")[-1])
    squad_url = "/".join(team_url.split("/")[:-1]) + "/"
    all_players = []
    all_playersTeam = []
    print("Starting with", team_url)
    start_team_time = time.time()
    while True:
        players_exists = get_max_year_from_team(cursor, team_id) == year
        if players_exists:
            print(f"{team_id} already have {year} in the database")
        if players_exists and not RUN_LAST_YEAR_AGAIN:
            break

        # if players exist and not DO_LAST_YEAR then break here
        output = get_players_from_squad(squad_url, year, team_id)
        if output == "Error":
            break
        all_players += output[0]
        all_playersTeam += output[1]
        if players_exists and RUN_LAST_YEAR_AGAIN:
            break
        year -= 1

    end_team_time = time.time()
    print(team_url, "took", str(end_team_time - start_team_time), "seconds")
    return all_players, all_playersTeam


def get_players_from_squad(team_url: str, year: int, team_id: str):
    url = BASE_URL + team_url + str(year)

    # Send a GET request to the URL
    response = requests.get(url, headers=HEADERS)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the div with class 'responsive-table'
        responsive_div = soup.find('div', class_='responsive-table')

        # Check if the div was found
        if responsive_div:
            # Find the table with class 'items' inside the responsive div
            items_table = responsive_div.find('table', class_='items')

            # Check if the table was found
            if items_table:
                # Extract all rows from the table

                player_list = []
                player_team_list = []
                rows = items_table.find_all('tr', class_=["odd", "even"])
                for row in rows:
                    player_number_elem = row.select_one('.rn_nummer')
                    player_number = player_number_elem.text.strip() if player_number_elem else None
                    player_number = int(player_number) if player_number != '-' else None

                    # Extracting image link
                    image_link_elem = row.select_one('.bilderrahmen-fixed.lazy')
                    img_ref = image_link_elem['data-src'] if image_link_elem else None

                    # Extracting player name
                    player_name_elem = row.select_one('.hauptlink')
                    player_name = player_name_elem.text.strip() if player_name_elem else None

                    # Extracting birth date
                    birth_date_elem = row.select_one('td.zentriert:nth-of-type(3)')
                    birth_date_text = birth_date_elem.text.strip() if birth_date_elem else None

                    birth_date, age_at_club = map(str.strip,
                                                  birth_date_text.rsplit('(', 1) if birth_date_text else (None, None))
                    age_at_club = int(age_at_club[:-1]) if (age_at_club != '-)' and age_at_club != 'N/A)') else None
                    birth_date = datetime.strptime(birth_date, '%b %d, %Y') if (
                            birth_date != "-" and birth_date != 'N/A') else None

                    # Extracting nationality
                    nationality_elem = row.select_one('.flaggenrahmen')
                    nationality = nationality_elem['title'] if nationality_elem else None

                    # Extracting profile reference
                    profile_ref_elem = row.select_one('.hauptlink a')
                    ref = profile_ref_elem['href'] if profile_ref_elem else None
                    player_id = int(ref.split('/')[-1])

                    position_elem = row.select('.posrela table td:nth-of-type(1)')[-1]
                    position = position_elem.text.strip() if position_elem else None

                    player_list.append((player_id, player_name, img_ref, birth_date, nationality, ref))
                    player_team_list.append((player_id, year, player_number, team_id, age_at_club, position))
                # print(rows[-1])
                # Print or return the rows as needed
                return player_list, player_team_list
            else:
                return "Error"
        else:
            print("Div with class 'responsive-table' not found.")

    # Return an empty list if something went wrong
    return "Error"


def get_teams_from_league(league_url):
    url = BASE_URL + league_url
    league_code = league_url.split('/')[1].replace('-', '_')
    # Send a GET request to the URL
    response = requests.get(url, headers=HEADERS)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the div with class 'responsive-table'
        responsive_div = soup.find('div', class_='responsive-table')

        # Check if the div was found
        if responsive_div:
            # Find the table with class 'items' inside the responsive div
            items_table = responsive_div.find('table', class_='items')

            # Check if the table was found
            if items_table:
                # Extract all rows from the table
                rows = items_table.find_all('td', class_='zentriert no-border-rechts')

                data_list = []

                # Iterate over each row and extract the required information

                for row in rows:
                    # Find the 'a' tag inside each 'td'
                    a_tag = row.find('a')
                    # Extract title and href attributes from the 'a' tag
                    title = a_tag.get('title') if a_tag else None
                    href = a_tag.get('href') if a_tag else None

                    # Find the 'img' tag inside 'td' to get the image source
                    img_src = row.find('img')['src'] if row.find('img') else None

                    # Append the data as a tuple to the list
                    data_list.append((title, league_code, href, href.split('/')[1].replace("-", "_"), img_src))

                # Print or return the rows as needed
                return data_list
            else:
                print("Table with class 'items' not found.")
        else:
            print("Div with class 'responsive-table' not found.")
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")

    # Return an empty list if something went wrong
    raise "Error retrieving the web page. Status code: " + str(response.status_code)


def print_tuple_list(tuple_list):
    print("\n".join(list(map(lambda x: str(x), tuple_list))))


def get_leagues():
    cursor.execute("""select * from leagues""")
    leagues = cursor.fetchall()
    return leagues


start_time = datetime.now()
# insert_league_to_leagues_table(cursor, 'Jupiler Pro League(Belgium)', '/jupiler-pro-league/startseite/wettbewerb/BE1', 'https://tmssl.akamaized.net/images/logo/header/be1.png?lm=1601478124')
leagues = get_leagues()
create_players_table(cursor)
create_teams_table(cursor)
create_player_team_table(cursor)
for league in leagues:
    print(f"--------------------------------------Starting with the {league[0]}--------------------------------------")
    teams = get_teams_from_league(league[2])
    handle_teams(teams)


end_time = datetime.now()
print("Finished in " + str(end_time - start_time))

conn.close()
