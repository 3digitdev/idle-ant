from collections import defaultdict
from dataclasses import field, dataclass

from shared import ResourceType, ProducerType, Status


@dataclass
class Producer:
    """
    A base 'producer' type, which can produce resources at given rates.

    A single producer may produce many different resources, and the rates may change
    from modifiers due to other factors.
    """

    name: ProducerType
    cost: tuple[ResourceType, int] | None = None
    total: int = 0
    status: Status = Status.DISABLED
    rates: dict[ResourceType, float] = field(default_factory=lambda: defaultdict(float))

    def __getitem__(self, resource: ResourceType) -> float:
        return self.rates[resource]

    def __setitem__(self, resource: ResourceType, value: float) -> None:
        self.rates[resource] = value
