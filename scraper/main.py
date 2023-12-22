import requests
from bs4 import BeautifulSoup
from const import HEADERS, BASE_URL


def get_squads_from_team(team_url):
    # TODO: loop through all the years until no result
    url = BASE_URL + team_url

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
                rows = items_table.find_all('tr', class_=["odd","even"])
                for row in rows:
                    player_number_elem = row.select_one('.rn_nummer')
                    player_number = player_number_elem.text.strip() if player_number_elem else None

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
                    age_at_club = age_at_club[:-1] if age_at_club else None

                    # Extracting nationality
                    nationality_elem = row.select_one('.flaggenrahmen')
                    nationality = nationality_elem['title'] if nationality_elem else None

                    # Extracting profile reference
                    profile_ref_elem = row.select_one('.hauptlink a')
                    profile_ref = profile_ref_elem['href'] if profile_ref_elem else None

                    position_elem = row.select('.posrela table td:nth-of-type(1)')[-1]
                    position = position_elem.text.strip() if position_elem else None
                    # position = None if position == player_name else position

                    # Printing the results
                    print("\nPlayer Name:", player_name)
                    print("Player Number:", player_number)
                    print("Image Link:", image_link)
                    print("Birth Date:", birth_date)
                    print("Age at Club:", age_at_club)
                    print("Nationality:", nationality)
                    print("Profile Reference:", profile_ref)
                    print("Position:", position)
                # print(rows[-1])
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
                    data_list.append((title, href, img_src))

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

def get_teams_from_league(league_url):
    url = BASE_URL + league_url

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
                    data_list.append((title, href, img_src))

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
# print_tuple_list(get_teams_from_league("/primera-division/startseite/wettbewerb/ES1"))
get_squads_from_team("/maccabi-tel-aviv/startseite/verein/119/saison_id/2016")
