import requests
from bs4 import BeautifulSoup
from const import HEADERS, BASE_URL, DB_PATH
import time
import sqlite3
from datetime import datetime
def handle_teams(teams):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    create_players_table(cursor)
    conn.commit()
    create_teams_table(cursor)
    conn.commit()

    insert_teams_to_teams_table(cursor, teams)
    conn.commit()
    for team in teams:
        players = get_players_from_team(team[2])
        create_team_table(cursor, team[3])
        conn.commit()
        insert_players_to_team_table(cursor, team[3], players)
        conn.commit()
        insert_players_to_players_table(cursor, players)
        conn.commit()
    conn.close()


def insert_teams_to_teams_table(cursor, teams_data):
    cursor.executemany('''
        INSERT OR IGNORE INTO teams (name, league, ref, table_code, img_ref)
        VALUES (?, ?, ?, ?, ?)
    ''', teams_data)
def create_teams_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            league TEXT,
            ref TEXT,
            table_code TEXT UNIQUE,
            img_ref TEXT
        )
    ''')

def create_players_table(cursor):
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                player_id INTEGER PRIMARY KEY,
                player_name TEXT,
                image_link TEXT,
                birth_date DATE,
                nationality TEXT,
                profile_ref TEXT
            )
        ''')

def convert_player_tuple(tuple_input):
    player_id, year, player_name, player_number, image_link, birth_date, age_at_club, nationality, profile_ref, position = tuple_input
    return (player_id, player_name, image_link, birth_date, nationality, profile_ref)


def insert_players_to_players_table(cursor, players_data):
    converted_player_data = [convert_player_tuple(player_tuple) for player_tuple in players_data]
    cursor.executemany('''
            INSERT OR IGNORE INTO players (player_id, player_name, image_link, birth_date, nationality, profile_ref)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', converted_player_data)

def create_team_table(cursor, team_table_name):
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {team_table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id INTEGER NOT NULL,
        year INTEGER NOT NULL,
        player_name TEXT,
        player_number INTEGER,
        image_link TEXT,
        birth_date DATE,
        age_at_club INTEGER,
        nationality TEXT,
        profile_ref TEXT,
        position TEXT,
        UNIQUE (player_id, year)
    );
    ''')


def insert_players_to_team_table(cursor, team_table_name, players_list):
    cursor.executemany(f'''
    INSERT OR IGNORE INTO {team_table_name} (
        player_id, year, player_name, player_number, image_link, birth_date, age_at_club, nationality, profile_ref, position
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    ''', players_list)


def get_players_from_team(team_url):
    year = int(team_url.split("/")[-1])
    squad_url = "/".join(team_url.split("/")[:-1]) + "/"
    all_players = []
    print("Starting with", team_url)
    start_team_time = time.time()
    while True:
        output = get_players_from_squad(squad_url, year)
        if output == "Error":
            break
        all_players += output

        year -= 1

    end_team_time = time.time()
    print(team_url, "took", str(end_team_time - start_team_time), "seconds")
    return all_players


def get_players_from_squad(team_url: str, year: int):
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
                rows = items_table.find_all('tr', class_=["odd", "even"])
                for row in rows:
                    player_number_elem = row.select_one('.rn_nummer')
                    player_number = player_number_elem.text.strip() if player_number_elem else None
                    player_number = int(player_number) if player_number != '-' else None

                    # Extracting image link
                    image_link_elem = row.select_one('.bilderrahmen-fixed.lazy')
                    image_link = image_link_elem['data-src'] if image_link_elem else None

                    # Extracting player name
                    player_name_elem = row.select_one('.hauptlink')
                    player_name = player_name_elem.text.strip() if player_name_elem else None

                    # Extracting birth date
                    birth_date_elem = row.select_one('td.zentriert:nth-of-type(3)')
                    birth_date_text = birth_date_elem.text.strip() if birth_date_elem else None

                    birth_date, age_at_club = map(str.strip,
                                                  birth_date_text.rsplit('(', 1) if birth_date_text else (None, None))
                    age_at_club = int(age_at_club[:-1]) if age_at_club != '-)' else None
                    birth_date = datetime.strptime(birth_date, '%b %d, %Y') if birth_date != "-" else None

                    # Extracting nationality
                    nationality_elem = row.select_one('.flaggenrahmen')
                    nationality = nationality_elem['title'] if nationality_elem else None

                    # Extracting profile reference
                    profile_ref_elem = row.select_one('.hauptlink a')
                    profile_ref = profile_ref_elem['href'] if profile_ref_elem else None
                    player_id = int(profile_ref.split('/')[-1])

                    position_elem = row.select('.posrela table td:nth-of-type(1)')[-1]
                    position = position_elem.text.strip() if position_elem else None
                    # position = None if position == player_name else position

                    # # Printing the results
                    # print("\nplayer_id", player_id)
                    # print("Year:", year)
                    # print("Player Name:", player_name)
                    # print("Player Number:", player_number)
                    # print("Image Link:", image_link)
                    # print("Birth Date:", birth_date)
                    # print("Age at Club:", age_at_club)
                    # print("Nationality:", nationality)
                    # print("Profile Reference:", profile_ref)
                    # print("Position:", position)

                    player_list.append((
                        player_id, year, player_name, player_number, image_link, birth_date, age_at_club,
                        nationality, profile_ref, position))
                # print(rows[-1])
                # Print or return the rows as needed
                return player_list
            else:
                print("Table with class 'items' not found.")
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
                    data_list.append((title, league_code, href, href.split('/')[1].replace("-","_"),img_src))

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
    return []


def print_tuple_list(tuple_list):
    print("\n".join(list(map(lambda x: str(x), tuple_list))))


# test
# league = input()
start_time = datetime.now()
teams = get_teams_from_league("/ligat-haal/startseite/wettbewerb/ISR1")
handle_teams(teams)
end_time = datetime.now()
print("Finished in " + str(end_time - start_time))
# teams = [('Maccabi Tel Aviv', '/maccabi-tel-aviv/startseite/verein/119/saison_id/2023', 'https://tmssl.akamaized.net/images/wappen/tiny/119.png?lm=1626682937')]
# result = get_players_from_team("/maccabi-tel-aviv/startseite/verein/119/saison_id/2023")
