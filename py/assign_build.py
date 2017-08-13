import json
import random
import requests

from py.grab_from_api import BASE_URL, VERSION_DATA

ABILITIES = ['Q', 'W', 'E']

def main():
    from py.data_types import Build
    from py.generate_types import Items, Maps, Champions, SummonerSpells
    from py.generate_data import items_by_map, map_name_to_id, map_id_to_mode

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

    # To set CHAMPION to a specific one, uncomment line below
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

    assert (FEROCITY + CUNNING + RESOLVE == 30)

    MASTERIES = tuple([FEROCITY, CUNNING, RESOLVE])

    map_modes = map_id_to_mode[map_value]
    summoner_choice = [
        summoner for summoner in SummonerSpells
        if bool(set(map_modes) & set(summoner.getModes()))
    ]

    SUMMONERS = set()
    while len(SUMMONERS) < 2:
        SUMMONERS.add(random.choice(summoner_choice))

    ability_q = random.random()
    ability_w = random.random()
    ability_e = random.random()

    if ability_q == max(ability_q, ability_w, ability_e):
        ABILITY_IDX = 0
    elif ability_w == max(ability_q, ability_w, ability_e):
        ABILITY_IDX = 1
    else:
        ABILITY_IDX = 2

    ABILITY = ABILITIES[ABILITY_IDX]

    if CHAMPION.getStats()['attackrange'] <= 250:
        # Melee Champ, so remove ranged items
        RANGE_LIMITATIONS = ['Runaan\'s Hurricane']
    else:
        # Ranged Champ, so remove melee items
        RANGE_LIMITATIONS = ['Ravenous Hydra', 'Titanic Hydra', 'Tiamat']

    item_choices = [
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
        and item.getName() not in RANGE_LIMITATIONS
    ]

    BOOT_SET = [item for item in item_choices if 'Boots' in item.getTags()]
    ITEMS_WITHOUT_BOOTS = [item for item in item_choices if item not in BOOT_SET]

    # Makes sure Cassiopeia doesn't get boots
    CANNOT_BUY_BOOTS = ['Cassiopeia']
    BOOT_CHOICE = [random.choice(BOOT_SET)] if CHAMPION.getName() not in CANNOT_BUY_BOOTS else []
    ITEM_SET = [item for item in ITEMS_WITHOUT_BOOTS if item.getRequired() == CHAMPION.getName()]

    # Must do this for Viktor, future champions with a required starting item
    ITEMS_WITHOUT_BOOTS = [item for item in ITEMS_WITHOUT_BOOTS if item not in ITEM_SET]

    while len(ITEM_SET) + len(BOOT_CHOICE) < 6:
        ITEM_SET.append(random.choice(ITEMS_WITHOUT_BOOTS))

    random.shuffle(ITEM_SET)
    ITEM_SET = BOOT_CHOICE + ITEM_SET

    BUILD = Build(CHAMPION, tuple(SUMMONERS), ABILITY, MASTERIES, tuple(ITEM_SET))
    # BUILD_DICT = {
    #     "name": CHAMPION.getName(),
    #     "summoners": sorted([summ.getName() for summ in list(SUMMONERS)]),
    #     "ability": ABILITY,
    #     "masteries": list(MASTERIES),
    #     "items": sorted([item.getName() for item in ITEM_SET]),
    # }
    #
    # with open('../json/current_build.json', 'w') as build_file:
    #     json.dump(BUILD_DICT, build_file)

if __name__ == "__main__":
    main()
