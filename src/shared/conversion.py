import re

from shared import ResourceType, ProducerType, UpgradeType


def format_num(number: int | float) -> str:
    """Formats a number to have commas every 3 digits"""
    return f'{float(number):,.2f}'.rstrip('0').rstrip('.')


def abbrev_num(number: int | float) -> str:
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
            return f'{format_num(number / threshold)}{suffix}'
    return format_num(number)


def type_class(type: ResourceType | ProducerType | UpgradeType) -> str:
    """Returns the class name for the given type"""
    return type.replace(' ', '-')


def style_info(info: str) -> str:
    def is_producer(word: str) -> bool:
        if not word.endswith('s'):
            word += 's'
        try:
            ProducerType(word)
            return True
        except ValueError:
            return False

    words = info.split(' ')
    for i, word in enumerate(words):
        if '/' in word:
            parts = word.split('/')
            for j, sub in enumerate(parts):
                if is_producer(sub):
                    parts[j] = f'[b cyan]{sub}[/]'
            words[i] = '/'.join(parts)
        elif is_producer(word):
            words[i] = f'[b cyan]{word}[/]'
        elif re.match(r'\d+x', word):
            words[i] = f'[green]{word}[/]'
        elif word == '"Gather"':
            words[i] = f'[b]{word}[/]'
    return ' '.join(words)
