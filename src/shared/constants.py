from enum import Enum, auto, StrEnum


class ResourceType(StrEnum):
    FOOD = 'Food'
    STICKS = 'Sticks'

    def __contains__(self, item):
        try:
            self(item)
        except ValueError:
            return False
        return True


class ProducerType(StrEnum):
    WORKER = 'Workers'

    def __contains__(self, item):
        try:
            self(item)
        except ValueError:
            return False
        return True


class UpgradeType(StrEnum):
    STILTS = 'Stilts'

    def __contains__(self, item):
        try:
            self(item)
        except ValueError:
            return False
        return True


class Status(Enum):
    DISABLED = auto()
    ENABLED = auto()
    SOON = auto()
