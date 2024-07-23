from dataclasses import dataclass

from shared import ResourceType, ProducerType, Status


@dataclass
class Producer:
    """
    A base 'producer' type, which can produce resources at given rates.

    A single producer may produce many different resources, and the rates may change
    from modifiers due to other factors.
    """

    name: ProducerType
    cost: list[tuple[ResourceType, int]]
    rates: dict[ResourceType, float]
    total: int = 0
    status: Status = Status.DISABLED

    def __getitem__(self, resource: ResourceType) -> float:
        return self.rates[resource]

    def __setitem__(self, resource: ResourceType, value: float) -> None:
        self.rates[resource] = value
