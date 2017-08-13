import random
import requests
import webbrowser

import grab_from_api


def main():
    from generate_types import Items, Maps, Champions, SummonerSpells
    from generate_data import items_by_map, map_name_to_id, item_id_to_name, map_id_to_mode

    Map_Idx = dict(enumerate([map.getName() for map in Maps]))

    for idx, name in Map_Idx.items():
        print('\t{}: {}'.format(idx + 1, name))

    map_id = None
    map_name = None
    while not isinstance(map_id, int):
        try:
            map_id = int(input('Which map are you playing on?: '))
            print(map_id)
            map_name = Map_Idx[map_id - 1]
        except ValueError:
            map_id = None
            print("That's not an integer...")
        except KeyError:
            map_id = None
            print("That number is not in range...")

    map_value = map_name_to_id[map_name]
    CHAMPION = random.choice(Champions)

    # CHAMPION = [c for c in Champions if c.getName() == 'Viktor'][0]

    FEROCITY = random.randint(0, 30)
    CUNNING = random.randint(0, 30)
    RESOLVE = random.randint(0, 30)

    if FEROCITY == max(FEROCITY, CUNNING, RESOLVE):
        FEROCITY = min(18, FEROCITY)
        CUNNING = min(18, random.randint(0, 30 - FEROCITY))
        RESOLVE = 30 - FEROCITY - CUNNING
        if RESOLVE > 18:
            difference = RESOLVE - 18
            CUNNING += difference / 2
            FEROCITY += difference - difference / 2
    elif CUNNING == max(FEROCITY, CUNNING, RESOLVE):
        CUNNING = min(18, CUNNING)
        RESOLVE = min(18, random.randint(0, 30 - CUNNING))
        FEROCITY = 30 - CUNNING - RESOLVE
        if FEROCITY > 18:
            difference = FEROCITY - 18
            RESOLVE += difference / 2
            CUNNING += difference - difference / 2
    else:
        RESOLVE = min(18, RESOLVE)
        FEROCITY = min(18, random.randint(0, 30 - RESOLVE))
        CUNNING = 30 - RESOLVE - FEROCITY
        if CUNNING > 18:
            difference = CUNNING - 18
            FEROCITY += difference / 2
            RESOLVE += difference - difference / 2

    print('Masteries: {} / {} / {}'.format(FEROCITY, CUNNING, RESOLVE))
    assert (FEROCITY + CUNNING + RESOLVE == 30)

    map_modes = map_id_to_mode[map_value]
    summoner_choice = [
        summoner for summoner in SummonerSpells
        if bool(set(map_modes) & set(summoner.getModes()))
    ]

    SUMMONER_SET = set()
    while(len(SUMMONER_SET) < 2):
        SUMMONER_SET.add(random.choice(summoner_choice))

    SUMMONER_URLS = ['http://ddragon.leagueoflegends.com/cdn/{}/img/spell/{}'.format(
        grab_from_api.VERSION_DATA['summoner'], summ.getImage()
    ) for summ in SUMMONER_SET]

    ability_q = random.random()
    ability_w = random.random()
    ability_e = random.random()
    ABILITIES = ['Q', 'W', 'E']

    if ability_q == max(ability_q, ability_w, ability_e):
        ABILITY = 0
    elif ability_w == max(ability_q, ability_w, ability_e):
        ABILITY = 1
    else:
        ABILITY = 2

    champion_url = grab_from_api.BASE_URL.format(
        grab_from_api.VERSION_DATA['champion'], 'champion/{}'.format(CHAMPION.getID())
    )

    champion = requests.get(champion_url)
    champion_data = champion.json()['data'][CHAMPION.getID()]
    spell = champion_data['spells'][ABILITY]

    SPELL_URL = 'http://ddragon.leagueoflegends.com/cdn/{}/img/spell/{}.png'.format(
        grab_from_api.VERSION_DATA['champion'], spell['id']
    )

    item_set = [
        item for item in Items
        if item.getID() in items_by_map[map_value]
        and not item.getConsumed()
        and item.getInStore()
        and (not item.getRequired() or item.getRequired() == CHAMPION.getName())
        and item.getPurchasable()
        and not item.buildsInto()
        and item.buildsFrom()
        and 'Trinket' not in item.getTags()
        and 'Consumable' not in item.getTags()
        and not item.getHideFromAll()
    ]
    BOOT_SET = [item for item in item_set if 'Boots' in item.getTags()]
    items_without_boots = [item for item in item_set if item not in BOOT_SET]

    BOOT_CHOICE = [random.choice(BOOT_SET)] if CHAMPION.getName() != 'Cassiopeia' else []
    ITEM_SET = [item for item in items_without_boots if item.getRequired() == CHAMPION.getName()]

    # Must do this for Viktor, future champions with a required starting item
    items_without_boots = [item for item in items_without_boots if item not in ITEM_SET]

    while(len(ITEM_SET) + len(BOOT_CHOICE) < 6):
        ITEM_SET.append(random.choice(items_without_boots))

    random.shuffle(ITEM_SET)
    ITEM_SET = BOOT_CHOICE + ITEM_SET

    CHAMPION_URL = 'http://ddragon.leagueoflegends.com/cdn/{}/img/champion/{}'.format(
        grab_from_api.VERSION_DATA['champion'], CHAMPION.getImage()
    )

    ITEM_URLS = ['http://ddragon.leagueoflegends.com/cdn/{}/img/item/{}'.format(
        grab_from_api.VERSION_DATA['item'], item.getImage()
    ) for item in ITEM_SET]

    print('Champion: {}'.format(CHAMPION_URL))
    print('First Max: {} -> {}'.format(ABILITIES[ABILITY], SPELL_URL))
    print('Summoner Spells: {}'.format(SUMMONER_URLS))
    print('Items: {}'.format(ITEM_URLS))

    html_file = open('test_file.html', 'w')

    message = """
    <html><head><body>
    <div>
    <img src={}>
    </div><br><div>
    <img src={}>
    <b><font size="7">{} / {} / {}</font></b>
    </div><br><div>
    <img src={}>
    <img src={}>
    </div><br><div>
    <img src={}>
    <img src={}>
    <img src={}>
    <img src={}>
    <img src={}>
    <img src={}>
    </div>
    </body></head></html>
    """.format(
        CHAMPION_URL,
        SPELL_URL,
        FEROCITY,
        CUNNING,
        RESOLVE,
        SUMMONER_URLS[0],
        SUMMONER_URLS[1],
        ITEM_URLS[0],
        ITEM_URLS[1],
        ITEM_URLS[2],
        ITEM_URLS[3],
        ITEM_URLS[4],
        ITEM_URLS[5],
    )

    html_file.write(message)
    html_file.close()

    webbrowser.open_new_tab('test_file.html')


if __name__ == "__main__":
    # grab_from_api.main()
    main()
