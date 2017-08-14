import json
import os
import requests
import webbrowser

from py.constants import ABILITIES
from py.grab_from_api import BASE_URL, VERSION_DATA

def main():
    with open('../json/current_build.json', 'r') as build_file:
        build_info = json.load(build_file)

    MASTERIES = build_info['_masteries']
    CHAMPION = build_info['_champion']
    ABILITY = build_info['_ability']
    ITEMS = build_info['_items']
    SUMMONERS = build_info['_summoners']

    champion_url = BASE_URL.format(
        VERSION_DATA['champion'], 'champion/{}'.format(CHAMPION['_id'])
    )
    champion = requests.get(champion_url)
    champion_data = champion.json()['data'][CHAMPION['_id']]
    SPELL = champion_data['spells'][ABILITIES.index(ABILITY)]

    CHAMPION_URL = 'http://ddragon.leagueoflegends.com/cdn/{}/img/champion/{}'.format(
        VERSION_DATA['champion'], CHAMPION['_image']['full']
    )

    SPELL_URL = 'http://ddragon.leagueoflegends.com/cdn/{}/img/spell/{}.png'.format(
        VERSION_DATA['champion'], SPELL['id']
    )

    SUMMONER_URLS = ['http://ddragon.leagueoflegends.com/cdn/{}/img/spell/{}'.format(
        VERSION_DATA['summoner'], summ['_image']['full']
    ) for summ in SUMMONERS]

    ITEM_URLS = ['http://ddragon.leagueoflegends.com/cdn/{}/img/item/{}'.format(
        VERSION_DATA['item'], item['_image']['full']
    ) for item in ITEMS]

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
        </div><br><div>
        <table style="table-layout: fixed; width: 200px;"><tr>
        <td align="center" style="background-color:red;"><b><font size="7">{}</b></td>
        <td align="center" style="background-color:blue;"><b><font size="7">{}</b></td>
        <td align="center" style="background-color:green;"><b><font size="7">{}</b></td>
        </tr></table>
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
