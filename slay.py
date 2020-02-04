import requests
import json
from bs4 import BeautifulSoup

strike_found = False
defend_found = False

def find_items(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    return table.find_all('tr')

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
        "type": card_type,
        "rarity": rarity,
        "cost": cost,
        "text": text,
    }

def get_status(card):
    data = card.find_all('td')
    name = card.find('a')['title']
    text = clean_string(data[3].get_text())

    return {
        "name": name,
        "type": "Status",
        "text": text,
    }

def get_curse(card):
    data = card.find_all('td')
    name = card.find('a')['title']
    text = clean_string(data[2].get_text())

    return {
        "name": name,
        "type": "Curse",
        "text": text,
    }

def get_noncard(relic, type):
    data = relic.find_all('td')
    name = clean_string(data[1].get_text())
    rarity = clean_string(data[2].get_text())
    text = clean_string(data[3].get_text())

    return {
        "name": name,
        "type": type,
        "rarity": rarity,
        "text": text,
    }

# Get regular cards
items = [
    ('https://slay-the-spire.fandom.com/wiki/Ironclad_Cards', ' (Ironclad only)'),
    ('https://slay-the-spire.fandom.com/wiki/Silent_Cards', ' (Silent only)'),
    ('https://slay-the-spire.fandom.com/wiki/Defect_Cards', ' (Defect only)'),
    ('https://slay-the-spire.fandom.com/wiki/Watcher_Cards', ' (Watcher only)'),
    ('https://slay-the-spire.fandom.com/wiki/Colorless_Cards', ' (Colourless)'),
]

data = []

for url, character_text in items:
    cards = find_items(url)

    # [1:] to skip table header
    for card in cards[1:]:
        result = get_card(card, character_text)

        if result['name'] == 'Strike':
            if strike_found:
                continue
            else:
                result['rarity'] = 'Starter'
                strike_found = True

        if result['name'] == 'Defend':
            if defend_found: 
                continue
            else:
                result['rarity'] = 'Starter'
                defend_found = True
        data.append(result)

# Get status cards
cards = find_items('https://slay-the-spire.fandom.com/wiki/Status')
for card in cards[1:]:
    data.append(get_status(card))

# Get curses
cards = find_items('https://slay-the-spire.fandom.com/wiki/Curse')
for card in cards[1:]:
    data.append(get_curse(card))

# Get relics
relics = find_items('https://slay-the-spire.fandom.com/wiki/Relics')
for relic in relics[1:]:
    data.append(get_noncard(relic, 'Relic'))

# Get potions
potions = find_items('https://slay-the-spire.fandom.com/wiki/Potions')
for potion in potions[1:]:
    data.append(get_noncard(potion, 'Potion'))

# Write to file
with open('slaydata.json', 'w') as file:
    file.write(json.dumps(data, indent=2))