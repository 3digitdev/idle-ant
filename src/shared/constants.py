from enum import Enum, auto, StrEnum


class ResourceType(StrEnum):
    FOOD = 'Food'
    STICKS = 'Sticks'
    STONES = 'Stones'
    LAND = 'Land'

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
    STILTS = 'Stilts'
    PACK_FRAME = 'Pack Frame'
    WHEEL = 'Wheel'
    CLUB = 'Club'
    FARMING = 'Farming'
    QUARRY = 'Quarry'
    OUTPOST = 'Outpost'

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
