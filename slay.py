import requests
import json
from bs4 import BeautifulSoup

strike_found = False
bash_found = False

def clean_string(text):
    return text.strip().replace('\n', ' ').replace('\xa0', ' ')

def get_card(card, class_text=''):
    data = card.find_all('td')
    name = card.find('a')['title']
    rarity = clean_string(data[2].get_text()) + class_text
    card_type = clean_string(data[3].get_text())
    cost = clean_string(data[4].get_text())
    text = clean_string(data[5].get_text())

    return {
        "name": name,
        "rarity": rarity,
        "type": card_type,
        "cost": cost,
        "text": text,
    }

items = [
    ('https://slay-the-spire.fandom.com/wiki/Ironclad_Cards', ' (Ironclad only)'),
    ('https://slay-the-spire.fandom.com/wiki/Silent_Cards', ' (Silent only)'),
    ('https://slay-the-spire.fandom.com/wiki/Defect_Cards', ' (Defect only)'),
    ('https://slay-the-spire.fandom.com/wiki/Watcher_Cards', ' (Watcher only)'),
    ('https://slay-the-spire.fandom.com/wiki/Colorless_Cards', ' (Colourless)'),
]

data = []

for url, character_text in items:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    cards = table.find_all('tr')

    for card in cards[1:]:
        result = get_card(card, character_text)
        data.append(result)
