from shared import ResourceType, ProducerType, UpgradeType


def abbrev_num(number: int) -> str:
    """Helpful for displaying large numbers as the game progresses"""
    suffixes = [
        (1e30, 'Non'),
        (1e27, 'Oct'),
        (1e24, 'Sept'),
        (1e21, 'Sext'),
        (1e18, 'Quint'),
        (1e15, 'Quad'),
        (1e12, 'T'),
        (1e9, 'B'),
        (1e6, 'M'),
        (1e3, 'K'),
    ]
    for threshold, suffix in suffixes:
        if number >= threshold:
            return f'{number / threshold:.2f}{suffix}'
    return str(number)


def type_class(type: ResourceType | ProducerType | UpgradeType) -> str:
    """Returns the class name for the given type"""
    return type.replace(' ', '-')
