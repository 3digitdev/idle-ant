from dataclasses import dataclass
from typing import Callable, Any

from shared import ResourceType, ProducerType, Status, UpgradeType


@dataclass
class Producer:
    """
    A base 'producer' type, which can produce resources at given rates.

    A single producer may produce many different resources, and the rates may change
    from modifiers due to other factors.
    """

    name: ProducerType
    cost: dict[ResourceType, int]
    # cost: list[tuple[ResourceType, int]]
    rates: dict[ResourceType, float]
    total: int = 0
    status: Status = Status.DISABLED
    # A function that returns whether status should be enabled
    # "Any" here is actually GameState, but we can't import it here due to circular imports
    check_fn: Callable[[Any], bool] = lambda _: True

    def __getitem__(self, resource: ResourceType) -> float:
        return self.rates[resource]

    def __setitem__(self, resource: ResourceType, value: float) -> None:
        self.rates[resource] = value


ALL_PRODUCERS = {
    ProducerType.ANT: Producer(
        name=ProducerType.ANT,
        status=Status.ENABLED,
        cost={ResourceType.FOOD: 5},
        rates={ResourceType.FOOD: 0.5},
    ),
    ProducerType.WORKER: Producer(
        name=ProducerType.WORKER,
        cost={ResourceType.FOOD: 50},
        rates={ResourceType.STICKS: 0.3},
        check_fn=lambda state: state.upgrades[UpgradeType.FIRST_QUEEN].purchased,
    ),
    ProducerType.HAULER: Producer(
        name=ProducerType.HAULER,
        cost={ResourceType.FOOD: 100, ResourceType.STICKS: 50},
        rates={ResourceType.STONES: 0.3},
        check_fn=lambda state: state.resources[ResourceType.STICKS].status == Status.ENABLED,
    ),
    ProducerType.SOLDIER: Producer(
        name=ProducerType.SOLDIER,
        cost={ResourceType.FOOD: 100, ResourceType.STICKS: 100, ResourceType.STONES: 50},
        rates={ResourceType.LAND: 0.3},
        check_fn=lambda state: state.upgrades[UpgradeType.CLUB].purchased,
    ),
}
