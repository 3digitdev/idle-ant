from dataclasses import dataclass
from typing import Callable, Any

from shared import ResourceType, ProducerType, Status, UpgradeType
from shared.constants import Boost


@dataclass
class Product:
    resource: ResourceType
    rate: float


@dataclass
class Producer:
    """
    A base 'producer' type, which can produce resources at given rates.

    A single producer may produce many different resources, and the rates may change
    from modifiers due to other factors.
    """

    name: ProducerType
    cost: dict[ResourceType, int]
    product: Product
    total: int = 0
    status: Status = Status.DISABLED
    # A function that returns whether status should be enabled
    # "Any" here is actually GameState, but we can't import it here due to circular imports
    check_fn: Callable[[Any], bool] = lambda _: True
    # If this is set, it means the boost is ACTIVE and should count down.
    boost: Boost | None = None
    # This is which Producer got replaced by this one
    replaced: ProducerType | None = None


ALL_PRODUCERS = {
    ProducerType.ANT: Producer(
        name=ProducerType.ANT,
        status=Status.ENABLED,
        cost={ResourceType.FOOD: 5},
        product=Product(resource=ResourceType.FOOD, rate=0.5),
        check_fn=lambda state: not state.upgrades[UpgradeType.INDUSTRIAL_FARMING].purchased,
    ),
    ProducerType.WORKER: Producer(
        name=ProducerType.WORKER,
        cost={ResourceType.FOOD: 25},
        product=Product(resource=ResourceType.STICKS, rate=0.5),
        check_fn=lambda state: state.upgrades[UpgradeType.FIRST_QUEEN].purchased
        and not state.upgrades[UpgradeType.TREE_FARMING].purchased,
    ),
    ProducerType.HAULER: Producer(
        name=ProducerType.HAULER,
        cost={ResourceType.FOOD: 500, ResourceType.STICKS: 200},
        product=Product(resource=ResourceType.STONES, rate=0.5),
        check_fn=lambda state: state.resources[ResourceType.STICKS].status == Status.ENABLED,
    ),
    ProducerType.SOLDIER: Producer(
        name=ProducerType.SOLDIER,
        cost={ResourceType.FOOD: 800, ResourceType.STICKS: 500, ResourceType.STONES: 100},
        product=Product(resource=ResourceType.LAND, rate=1.5),
        check_fn=lambda state: state.upgrades[UpgradeType.CLUB].purchased,
    ),
    ProducerType.MINER: Producer(
        name=ProducerType.MINER,
        cost={ResourceType.FOOD: 2000, ResourceType.STICKS: 600, ResourceType.STONES: 300},
        product=Product(resource=ResourceType.METAL, rate=3),
        check_fn=lambda state: state.upgrades[UpgradeType.MINING].purchased,
    ),
    ProducerType.ENGINEER: Producer(
        name=ProducerType.ENGINEER,
        cost={ResourceType.LAND: 200, ResourceType.METAL: 100},
        product=Product(resource=ResourceType.ENERGY, rate=3),
        check_fn=lambda state: state.upgrades[UpgradeType.INDUSTRIAL_REVOLUTION].purchased,
    ),
    # FOOD IS NO LONGER A RESOURCE BY THIS POINT
    # STICKS ARE NO LONGER A RESOURCE BY THIS POINT
    ProducerType.LUMBERJACK: Producer(
        name=ProducerType.LUMBERJACK,
        cost={ResourceType.METAL: 200, ResourceType.ENERGY: 100},
        product=Product(resource=ResourceType.LUMBER, rate=3),  # Rate will be auto-calculated on unlock
        check_fn=lambda state: state.upgrades[UpgradeType.TREE_FARMING].purchased,
        replaced=ProducerType.WORKER,
    ),
}
