import collections
import inspect
import json
from typing import List, Tuple

from py.generate_data import EXCEPTIONS


class ObjectEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "to_json"):
            return self.default(obj.to_json())
        elif hasattr(obj, "__dict__"):
            d = dict(
                (key, value)
                for key, value in inspect.getmembers(obj)
                if not key.startswith("__")
                and not inspect.isabstract(value)
                and not inspect.isbuiltin(value)
                and not inspect.isfunction(value)
                and not inspect.isgenerator(value)
                and not inspect.isgeneratorfunction(value)
                and not inspect.ismethod(value)
                and not inspect.ismethoddescriptor(value)
                and not inspect.isroutine(value)
            )
            return self.default(d)
        return obj


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
        self._image = initializeValue(dictionary, 'image')


    def getID(self):
        return self._id

    def getName(self):
        return self._name

    def getImage(self):
        return self._image

    def __str__(self):
        return str({
            "id": self._id,
            "name": self._name,
        })

    def __repr__(self):
        return json.dumps(self.__dict__)


class Item:
    def __init__(self, item_id, dictionary: dict) -> None:
        self._id = int(item_id)
        self._name = initializeValue(dictionary, 'name')
        self._description = initializeValue(dictionary, 'description')
        self._image = initializeValue(dictionary, 'image')
        self._gold = initializeValue(dictionary, 'gold')
        self._required = initializeValue(dictionary, 'requiredChampion')
        self._consumed = initializeValue(dictionary, 'consumed')
        self._hidefromall = initializeValue(dictionary, 'hideFromAll')
        self._instore = initializeValue(dictionary, 'inStore')
        self._tags = initializeValue(dictionary, 'tags')
        self._plaintext = initializeValue(dictionary, 'plaintext')
        self._stats = initializeValue(dictionary, 'stats')
        self._depth = initializeValue(dictionary, 'depth')

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

    def getGold(self):
        return self._gold

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

    def getPlaintext(self):
        return self._plaintext

    def getStats(self):
        return self._stats

    def getDepth(self):
        return self._depth

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
            "gold": self._gold,
            "required": self._required,
            "consumed": self._consumed,
            "hidefromall": self._hidefromall,
            "instore": self._instore,
            "tags": self._tags,
            "plaintext": self._plaintext,
            "stats": self._stats,
            "depth": self._depth,
            "from": self._from,
            "into": self._into,
            "maps": self._maps,
        })

    def __repr__(self):
        return json.dumps(self.__dict__)


class Champion:
    def __init__(self, dictionary: dict) -> None:
        self._id = initializeValue(dictionary, 'id')
        self._name = initializeValue(dictionary, 'name')
        self._key = initializeValue(dictionary, 'key')
        self._title = initializeValue(dictionary, 'title')
        self._blurb = initializeValue(dictionary, 'blurb')
        self._info = initializeValue(dictionary, 'info')
        self._image = initializeValue(dictionary, 'image')
        self._tags = initializeValue(dictionary, 'tags')
        self._partype = initializeValue(dictionary, 'partype')
        self._stats = initializeValue(dictionary, 'stats')

    def getID(self):
        return self._id

    def getName(self):
        return self._name

    def getKey(self):
        return self._key

    def getTitle(self):
        return self._title

    def getBlurb(self):
        return self._blurb

    def getInfo(self):
        return self._info

    def getImage(self):
        return self._image

    def getTags(self):
        return self._tags

    def getParType(self):
        return self._partype

    def getStats(self):
        return self._stats

    def __str__(self):
        return str({
            "id": self._id,
            "name": self._name,
            "key": self._key,
            "title": self._title,
            "blurb": self._blurb,
            "info": self._info,
            "tags": self._tags,
            "partype": self._partype,
            "stats": self._stats,
        })

    def __repr__(self):
        return json.dumps(self.__dict__)


class SummonerSpell:
    def __init__(self, dictionary: dict) -> None:
        self._id = initializeValue(dictionary, 'id')
        self._name = initializeValue(dictionary, 'name')
        self._description = initializeValue(dictionary, 'description')
        self._key = initializeValue(dictionary, 'key')
        self._modes = initializeValue(dictionary, 'modes')
        self._image = initializeValue(dictionary, 'image')

    def getID(self):
        return self._id

    def getName(self):
        return self._name

    def getDescription(self):
        return self._description

    def getKey(self):
        return self._key

    def getModes(self):
        return self._modes

    def getImage(self):
        return self._image

    def __str__(self):
        return str({
            "id": self._id,
            "name": self._name,
            "description": self._description,
            "key": self._key,
            "modes": self._modes,
        })

    def __repr__(self):
        return json.dumps(self.__dict__)

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
        return json.dumps(self.__dict__)