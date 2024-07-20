from enum import Enum, auto, StrEnum


class ResourceType(StrEnum):
    FOOD = 'Food'
    STICKS = 'Sticks'


class ProducerType(StrEnum):
    IDLE = 'Idle'
    WORKER = 'Workers'


class Status(Enum):
    DISABLED = auto()
    ENABLED = auto()
    SOON = auto()
