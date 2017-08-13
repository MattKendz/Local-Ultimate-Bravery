import collections
import json
from typing import List, Tuple

from py.generate_data import EXCEPTIONS


def initializeValue(*args):
    dictionary = args[0]
    key = dictionary
    for value in args[1:]:
        if isinstance(key, collections.Iterable) and value in key:
            key = key[value]
        elif value.lower() in EXCEPTIONS:
            return EXCEPTIONS[value.lower()]
        else:
            return None
    return key

class Map:
    def __init__(self, dictionary: dict) -> None:
        self._id = initializeValue(dictionary, 'MapId')
        self._name = initializeValue(dictionary, 'MapName')

    def getID(self):
        return self._id

    def getName(self):
        return self._name

    def __str__(self):
        return str({
            "id": self._id,
            "name": self._name,
        })

    def __repr__(self):
        return str(self)


class Item:
    def __init__(self, item_id, dictionary: dict) -> None:
        self._id = int(item_id)
        self._name = initializeValue(dictionary, 'name')
        self._description = initializeValue(dictionary, 'description')
        self._image = initializeValue(dictionary, 'image', 'full')
        self._purchasable = initializeValue(dictionary, 'gold', 'purchasable')
        self._required = initializeValue(dictionary, 'requiredChampion')
        self._consumed = initializeValue(dictionary, 'consumed')
        self._hidefromall = initializeValue(dictionary, 'hideFromAll')
        self._instore = initializeValue(dictionary, 'inStore')
        self._tags = initializeValue(dictionary, 'tags')

        self._from = [int(item_id) for item_id in dictionary['from']] \
            if 'from' in dictionary else []
        self._into = [int(item_id) for item_id in dictionary['into']] \
            if 'into' in dictionary else []
        self._maps = [
            int(map_id) for map_id, condition in dictionary['maps'].items() \
            if condition
        ] if 'maps' in dictionary else []

    def getID(self):
        return self._id

    def getName(self):
        return self._name

    def getDescription(self):
        return self._description

    def getImage(self):
        return self._image

    def getPurchasable(self):
        return self._purchasable

    def getRequired(self):
        return self._required

    def getConsumed(self):
        return self._consumed

    def getHideFromAll(self):
        return self._hidefromall

    def getInStore(self):
        return self._instore

    def getTags(self):
        return self._tags

    def buildsFrom(self) -> List[int]:
        return self._from

    def buildsInto(self) -> List[int]:
        return self._into

    def getMaps(self) -> List[int]:
        return self._maps

    def __str__(self):
        return str({
            "id": self._id,
            "name": self._name,
            "description": self._description,
            "purchasable": self._purchasable,
            "required": self._required,
            "consumed": self._consumed,
            "hidefromall": self._hidefromall,
            "instore": self._instore,
            "tags": self._tags,
            "from": self._from,
            "into": self._into,
            "maps": self._maps,
        })

    def __repr__(self):
        return str(self)


class Champion:
    def __init__(self, dictionary: dict) -> None:
        self._id = initializeValue(dictionary, 'id')
        self._name = initializeValue(dictionary, 'name')
        self._key = initializeValue(dictionary, 'key')
        self._title = initializeValue(dictionary, 'title')
        self._image = initializeValue(dictionary, 'image', 'full')
        self._stats = initializeValue(dictionary, 'stats')

    def getID(self):
        return self._id

    def getName(self):
        return self._name

    def getKey(self):
        return self._key

    def getTitle(self):
        return self._title

    def getImage(self):
        return self._image

    def getStats(self):
        return self._stats

    def __str__(self):
        return str({
            "id": self._id,
            "name": self._name,
            "key": self._key,
            "title": self._title,
            "stats": self._stats,
        })

    def __repr__(self):
        return str(self)


class SummonerSpell:
    def __init__(self, dictionary: dict) -> None:
        self._id = initializeValue(dictionary, 'id')
        self._name = initializeValue(dictionary, 'name')
        self._description = initializeValue(dictionary, 'description')
        self._modes = initializeValue(dictionary, 'modes')
        self._image = initializeValue(dictionary, 'image', 'full')

    def getID(self):
        return self._id

    def getName(self):
        return self._name

    def getDescription(self):
        return self._description

    def getModes(self):
        return self._modes

    def getImage(self):
        return self._image

    def __str__(self):
        return str({
            "id": self._id,
            "name": self._name,
            "description": self._description,
            "modes": self._modes,
        })

    def __repr__(self):
        return str(self)

# TODO: Make this class JSON Serializable
class Build:
    def __init__(
        self,
        champion: Champion,
        summoners: Tuple[SummonerSpell, SummonerSpell],
        ability: str,
        masteries: Tuple[int, int, int],
        items: Tuple[Item, Item, Item, Item, Item, Item]
    ) -> None:
        assert ability in ['Q', 'W', 'E', 'R']
        assert (masteries[0] + masteries[1] + masteries[2] == 30)

        self._champion = champion
        self._summoners = summoners
        self._ability = ability
        self._masteries = masteries
        self._items = items

    def getChampion(self):
        return self._champion

    def getSummoners(self):
        return self._summoners

    def getAbility(self):
        return self._ability

    def getMasteries(self):
        return self._masteries

    def getItems(self):
        return self._items

    def __str__(self):
        return str({
            "champion": self._champion,
            "summoners": self._summoners,
            "ability": self._ability,
            "masteries": self._masteries,
            "items": self._items,
        })

    def __repr__(self):
        return str(self)