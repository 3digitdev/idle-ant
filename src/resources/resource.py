from dataclasses import dataclass
from typing import Self

from constants import ResourceType, Status


@dataclass
class Resource:
    """A base 'resource' type, which helps calculate progress to a future full value."""

    name: ResourceType
    total: int = 0
    progress: float = 0.0
    status: Status = Status.DISABLED

    def __add__(self, other: Self | float) -> Self:
        if not isinstance(other, float):
            extra, self.progress = divmod(self.progress + other.progress, 1)
            self.total += int(other.total + extra)
        else:
            total, self.progress = divmod(self.total + self.progress + other, 1)
            self.total = int(total)
        return self

    def __str__(self) -> str:
        return f'{self.name}: {self.total}'
