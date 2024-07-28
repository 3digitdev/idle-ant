from dataclasses import dataclass
from typing import Callable, Any

from shared import ResourceType, ProducerType, UpgradeType, Status


@dataclass
class Upgrade:
    """
    A base 'upgrade' type, which provides a modifier to specific Producers.

    A single upgrade type SHOULD only modify a single producer type (pending design).
    """

    name: UpgradeType
    cost: dict[ResourceType, int]
    modifiers: dict[ProducerType, float]
    info: str
    total: int = 0
    purchased: bool = False
    status: Status = Status.DISABLED
    # A function that returns whether status should be enabled
    # "Any" here is actually GameState, but we can't import it here due to circular imports
    check_fn: Callable[[Any], bool] = lambda _: True

    def __getitem__(self, producer: ProducerType) -> float:
        return self.modifiers[producer]

    def __setitem__(self, producer: ProducerType, value: float) -> None:
        self.modifiers[producer] = value


def bought(upgrade: UpgradeType, game_state: any) -> bool:
    return game_state.upgrades[upgrade].purchased


# NOTE:  ALL UPGRADES' MODIFIERS SHOULD BE 1.0 OR GREATER TO AVOID NEGATIVE PRODUCTION RATES!
ALL_UPGRADES = {
    UpgradeType.FIRST_QUEEN: Upgrade(
        name=UpgradeType.FIRST_QUEEN,
        cost={ResourceType.FOOD: 250},
        modifiers={ProducerType.ANT: 2.0},
        check_fn=lambda state: not bought(UpgradeType.FIRST_QUEEN, state)
        and state.producers[ProducerType.ANT].total >= 25,
        info='[green]2x[/] [b cyan]Ant[/] rate; Unlocks [b cyan]Worker[/]',
    ),
    UpgradeType.SUGAR_WATER: Upgrade(
        name=UpgradeType.SUGAR_WATER,
        cost={ResourceType.FOOD: 100},
        modifiers={'CLICK': 2.0},  # This upgrade is handled manually in the code check
        check_fn=lambda state: state.upgrades[UpgradeType.SUGAR_WATER].status == Status.ENABLED
        or not bought(UpgradeType.SUGAR_WATER, state)
        and state.resources[ResourceType.FOOD].total >= 50,
        info='[green]2x[/] [b]"Gather"[/] rate',
    ),
    UpgradeType.STILTS: Upgrade(
        name=UpgradeType.STILTS,
        cost={ResourceType.FOOD: 500, ResourceType.STICKS: 250},
        modifiers={ProducerType.ANT: 3.0},
        check_fn=lambda state: not bought(UpgradeType.STILTS, state)
        and state.producers[ProducerType.WORKER].total >= 1,
        info='[green]3x[/] [b cyan]Ant[/] rate',
    ),
    UpgradeType.PACK_FRAME: Upgrade(
        name=UpgradeType.PACK_FRAME,
        cost={ResourceType.FOOD: 1000, ResourceType.STICKS: 500},
        modifiers={ProducerType.ANT: 2.0, ProducerType.WORKER: 2.0},
        check_fn=lambda state: not bought(UpgradeType.PACK_FRAME, state)
        and state.resources[ResourceType.STICKS].total >= 1,
        info='[green]2x[/] [b cyan]Ant[/]/[b cyan]Worker[/] rate',
    ),
    UpgradeType.WHEEL: Upgrade(
        name=UpgradeType.WHEEL,
        cost={ResourceType.FOOD: 3000, ResourceType.STICKS: 750, ResourceType.STONES: 500},
        modifiers={ProducerType.HAULER: 2.0, ProducerType.WORKER: 3.0},
        check_fn=lambda state: not bought(UpgradeType.WHEEL, state) and state.resources[ResourceType.STONES].total >= 1,
        info='[green]2x[/] [b cyan]Hauler[/]/[b cyan]Worker[/] rate',
    ),
    UpgradeType.CLUB: Upgrade(
        name=UpgradeType.CLUB,
        cost={ResourceType.FOOD: 5000, ResourceType.STICKS: 2000, ResourceType.STONES: 1000},
        modifiers={},
        check_fn=lambda state: not bought(UpgradeType.CLUB, state) and state.resources[ResourceType.STONES].total >= 1,
        info='Unlocks [b cyan]Soldier[/]',
    ),
    # TODO:  DO WE WANT THIS HERE?  INCREASES CLICK RATE FOR FOO BUT MIGHT NOT BE USEFUL BY THIS POINT.
    # UpgradeType.ENERGY_DRINK: Upgrade(
    #     name=UpgradeType.ENERGY_DRINK,
    #     cost={ResourceType.FOOD: 7500, ResourceType.STICKS: 3500, ResourceType.STONES: 1500},
    #     modifiers={'CLICK': 4.0},
    #     check_fn=lambda state: not bought(UpgradeType.ENERGY_DRINK, state) and bought(UpgradeType.CLUB, state),
    #     info='[green]4x[/] [b]"Gather"[/] rate',
    # ),
    UpgradeType.FARMING: Upgrade(
        name=UpgradeType.FARMING,
        cost={ResourceType.FOOD: 3000, ResourceType.LAND: 250},
        modifiers={ProducerType.ANT: 2.0},
        check_fn=lambda state: not bought(UpgradeType.FARMING, state) and state.resources[ResourceType.LAND].total >= 1,
        info='[green]2x[/green] [b]Ant[/b] rate',
    ),
    UpgradeType.FOREST: Upgrade(
        name=UpgradeType.FOREST,
        cost={ResourceType.FOOD: 5000, ResourceType.STICKS: 750, ResourceType.LAND: 500},
        modifiers={ProducerType.WORKER: 2.0},
        check_fn=lambda state: not bought(UpgradeType.FOREST, state) and state.resources[ResourceType.LAND].total >= 1,
        info='[green]2x[/green] [b]Worker[/b] rate',
    ),
    UpgradeType.QUARRY: Upgrade(
        name=UpgradeType.QUARRY,
        cost={ResourceType.STICKS: 5000, ResourceType.STONES: 750, ResourceType.LAND: 500},
        modifiers={ProducerType.HAULER: 2.0},
        check_fn=lambda state: not bought(UpgradeType.QUARRY, state) and state.resources[ResourceType.LAND].total >= 1,
        info='[green]2x[/green] [b]Hauler[/b] rate',
    ),
    UpgradeType.OUTPOST: Upgrade(
        name=UpgradeType.OUTPOST,
        cost={ResourceType.FOOD: 7500, ResourceType.STICKS: 3500, ResourceType.LAND: 500},
        modifiers={ProducerType.SOLDIER: 2.0},
        check_fn=lambda state: not bought(UpgradeType.OUTPOST, state) and state.resources[ResourceType.LAND].total >= 1,
        info='[green]2x[/green] [b]Soldier[/b] rate',
    ),
}
