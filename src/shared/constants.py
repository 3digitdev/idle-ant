from dataclasses import dataclass
from enum import Enum, auto, StrEnum


class ResourceType(StrEnum):
    FOOD = 'Food'
    STICKS = 'Sticks'
    STONES = 'Stones'
    LAND = 'Land'
    METAL = 'Metal'
    ENERGY = 'Energy'
    LUMBER = 'Lumber'

    def __contains__(self, item):
        if '-' in item:
            item = item.replace('-', ' ')
        try:
            self(item)
        except ValueError:
            return False
        return True


class ProducerType(StrEnum):
    ANT = 'Ants'
    WORKER = 'Workers'
    HAULER = 'Haulers'
    SOLDIER = 'Soldiers'
    MINER = 'Miners'
    ENGINEER = 'Engineers'
    LUMBERJACK = 'Lumberjacks'

    def __contains__(self, item):
        if '-' in item:
            item = item.replace('-', ' ')
        try:
            self(item)
        except ValueError:
            return False
        return True


class UpgradeType(StrEnum):
    FIRST_QUEEN = 'First Queen'
    SUGAR_WATER = 'Sugar Water'
    STILTS = 'Stilts'
    PACK_FRAME = 'Pack Frame'
    WHEEL = 'Wheel'
    CLUB = 'Club'
    FARMING = 'Farming'
    FOREST = 'Forest'
    QUARRY = 'Quarry'
    OUTPOST = 'Outpost'
    MINING = 'Mining'
    METAL_TOOLS = 'Metal Tools'
    METAL_WEAPONS = 'Metal Weapons'
    INDUSTRIAL_REVOLUTION = 'Industrial Revolution'
    INDUSTRIAL_FARMING = 'Industrial Farming'
    TREE_FARMING = 'Tree Farming'

    def __contains__(self, item):
        if '-' in item:
            item = item.replace('-', ' ')
        try:
            self(item)
        except ValueError:
            return False
        return True


# TODO: [FUTURE]:  Add more statuses for more complex interactions.
#                  Alternatively, simplify this to a boolean if we can
class Status(Enum):
    DISABLED = auto()
    ENABLED = auto()

    @classmethod
    def from_bool(cls, value: bool):
        return cls.ENABLED if value else cls.DISABLED


@dataclass
class Boost:
    # This is the Producer that will get spent to buy the boost
    cost: ProducerType
    target: ProducerType
    # This is the temporary boost rate that will be applied to the Producer being boosted
    # The value will change based on the boost_cost Producer's current total
    rate: float = 1.0
    # This is how many seconds remain on the boost
    timer: int = 30


@dataclass
class Replace:
    old: ProducerType
    created: ProducerType
    # How much of the old Producer's total will be transferred to the new Producer
    divisor: int = 2
