import requests
import json

from py import generate_types, generate_data

BASE_URL = 'http://ddragon.leagueoflegends.com/cdn/{}/data/en_US/{}.json'
VERSION_URL = 'https://ddragon.leagueoflegends.com/realms/na.json'
VERSIONS = requests.get(VERSION_URL)
VERSION_DATA = VERSIONS.json()['n']

def main():
    item_url = BASE_URL.format(VERSION_DATA['item'], 'item')
    map_url = BASE_URL.format(VERSION_DATA['map'], 'map')
    champion_url = BASE_URL.format(VERSION_DATA['champion'], 'champion')
    summoner_url = BASE_URL.format(VERSION_DATA['summoner'], 'summoner')

    items = requests.get(item_url)
    with open('../json/item_data.json', 'w') as data_file:
        json.dump(items.json(), data_file)

    maps = requests.get(map_url)
    with open('../json/map_data.json', 'w') as data_file:
        json.dump(maps.json(), data_file)

    champions = requests.get(champion_url)
    with open('../json/champion_data.json', 'w') as data_file:
        json.dump(champions.json(), data_file)

    summoner_spells = requests.get(summoner_url)
    with open('../json/summoner_spell_data.json', 'w') as data_file:
        json.dump(summoner_spells.json(), data_file)

if __name__ == "__main__":
    main()
