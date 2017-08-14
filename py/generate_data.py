import json


with open('../json/item_data.json', 'r') as items:
    item_list = json.load(items)
    EXCEPTIONS = {key.lower(): value for (key, value) in item_list['basic'].items()}
    item_list = item_list['data']

with open('../json/map_data.json', 'r') as maps:
    map_list = json.load(maps)['data']

items_by_map = {}
map_name_to_id = {}
item_id_to_name = {}
map_id_to_mode = {}


def main():
    for map_id, data in map_list.items():
        items_by_map[int(map_id)] = []
        map_name_to_id[data['MapName']] = int(map_id)

    for item_id, data in item_list.items():
        if 'name' in data:
            item_id_to_name[int(item_id)] = data['name']

        if 'maps' in data:
            for map_id, condition in data['maps'].items():
                if condition:
                    items_by_map[int(map_id)].append(int(item_id))

    map_id_to_mode[map_name_to_id['The Twisted Treeline']] = ['CLASSIC',]
    map_id_to_mode[map_name_to_id['Summoner\'s Rift']] = ['CLASSIC',]
    map_id_to_mode[map_name_to_id['Howling Abyss']] = ['ARAM',]

if __name__ == "__main__":
    main()