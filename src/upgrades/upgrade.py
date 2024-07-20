from collections import defaultdict
from dataclasses import field, dataclass

from constants import ResourceType, ProducerType, UpgradeType, Status


@dataclass
class Upgrade:
    """
    A base 'upgrade' type, which provides a modifier to specific Producers.

    A single upgrade type SHOULD only modify a single producer type (pending design).
    """

    name: UpgradeType
    cost: tuple[ResourceType, int] | None = None
    total: int = 0
    status: Status = Status.DISABLED
    modifiers: dict[ProducerType, float] = field(default_factory=lambda: defaultdict(float))

    def __getitem__(self, producer: ProducerType) -> float:
        return self.modifiers[producer]

    def __setitem__(self, producer: ProducerType, value: float) -> None:
        self.modifiers[producer] = value
