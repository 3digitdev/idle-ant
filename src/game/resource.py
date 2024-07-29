from dataclasses import dataclass
from typing import Self, Callable, Any

from shared import ResourceType, Status, ProducerType


@dataclass
class Resource:
    """A base 'resource' type, which helps calculate progress to a future full value."""

    name: ResourceType
    total: int = 0
    progress: float = 0.0
    status: Status = Status.DISABLED
    # A function that returns whether status should be enabled
    # "Any" here is actually GameState, but we can't import it here due to circular imports
    check_fn: Callable[[Any], bool] = lambda _: True

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


ALL_RESOURCES = {
    ResourceType.FOOD: Resource(
        name=ResourceType.FOOD,
        status=Status.ENABLED,
    ),
    ResourceType.STICKS: Resource(
        name=ResourceType.STICKS,
        check_fn=lambda state: state.producers[ProducerType.WORKER].total > 0,
    ),
    ResourceType.STONES: Resource(
        name=ResourceType.STONES,
        check_fn=lambda state: state.producers[ProducerType.HAULER].total > 0,
    ),
    ResourceType.LAND: Resource(
        name=ResourceType.LAND,
        check_fn=lambda state: state.producers[ProducerType.SOLDIER].total > 0,
    ),
    ResourceType.METAL: Resource(
        name=ResourceType.METAL,
        check_fn=lambda state: state.producers[ProducerType.MINER].total > 0,
    ),
}
