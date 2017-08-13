import json
import os
import requests
import webbrowser

from py.assign_build import ABILITIES
from py.grab_from_api import BASE_URL, VERSION_DATA

def main():
    with open('../json/current_build.json', 'r') as build_file:
        build_info = json.load(build_file)

    MASTERIES = build_info['masteries']
    CHAMPION = build_info['champion']
    ABILITY = build_info['ability']
    BUILD = build_info

    champion_url = BASE_URL.format(
        VERSION_DATA['champion'], 'champion/{}'.format(CHAMPION.getID())
    )
    champion = requests.get(champion_url)
    champion_data = champion.json()['data'][CHAMPION.getID()]
    SPELL = champion_data['spells'][ABILITIES.index(CHAMPION.getAbility())]

    CHAMPION_URL = 'http://ddragon.leagueoflegends.com/cdn/{}/img/champion/{}'.format(
        VERSION_DATA['champion'], CHAMPION.getImage()
    )

    SPELL_URL = 'http://ddragon.leagueoflegends.com/cdn/{}/img/spell/{}.png'.format(
        VERSION_DATA['champion'], SPELL['id']
    )

    SUMMONER_URLS = ['http://ddragon.leagueoflegends.com/cdn/{}/img/spell/{}'.format(
        VERSION_DATA['summoner'], summ.getImage()
    ) for summ in list(BUILD.getSummoners())]

    ITEM_URLS = ['http://ddragon.leagueoflegends.com/cdn/{}/img/item/{}'.format(
        VERSION_DATA['item'], item.getImage()
    ) for item in list(BUILD.getItems())]

    print('Champion: {}'.format(CHAMPION_URL))
    print('Masteries: {} / {} / {}'.format(MASTERIES[0], MASTERIES[1], MASTERIES[2]))
    print('First Max: {} -> {}'.format(ABILITY, SPELL_URL))
    print('Summoner Spells: {}'.format(SUMMONER_URLS))
    print('Items: {}'.format(ITEM_URLS))

    with open('../html/test_file.html', 'w') as html_file:
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
            MASTERIES[0],
            MASTERIES[1],
            MASTERIES[2],
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

        webbrowser.open('file://' + os.path.realpath('../html/test_file.html'))

if __name__ == "__main__":
    main()
