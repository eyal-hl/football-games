import requests
from bs4 import BeautifulSoup

url = 'https://www.transfermarkt.com/maccabi-tel-aviv/kader/verein/119/plus/0/galerie/0?saison_id=2023'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', class_='items')

    if table:
        rows = table.find_all('tr')
        print(rows[0])
        for row in rows:
            cells = row.find_all(['td', 'th'])
            row_data = [cell.get_text(strip=True) for cell in cells]
            print(row_data)
    else:
        print("Table with class 'items' not found.")
else:
    print(f"Failed to retrieve the web page. Status code: {response.status_code}")

#test