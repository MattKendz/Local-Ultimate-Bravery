import json

from data_types import Map, Item, Champion, SummonerSpell

with open('item_data.json', 'r') as items:
    item_list = json.load(items)['data']

with open('map_data.json', 'r') as maps:
    map_list = json.load(maps)['data']

with open('champion_data.json', 'r') as champions:
    champion_list = json.load(champions)['data']

with open('summoner_spell_data.json', 'r') as summonerspells:
    summoner_spell_list = json.load(summonerspells)['data']

Items = []
Maps = []
Champions = []
SummonerSpells = []

for _, data in map_list.items():
    Maps.append(Map(data))

for item_id, data in item_list.items():
    Items.append(Item(item_id, data))

for _, data in champion_list.items():
    Champions.append(Champion(data))

for _, data in summoner_spell_list.items():
    SummonerSpells.append(SummonerSpell(data))


