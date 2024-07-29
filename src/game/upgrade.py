from dataclasses import dataclass
from typing import Callable, Any

from shared import ResourceType, ProducerType, UpgradeType, Status, style_info


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
    UpgradeType.SUGAR_WATER: Upgrade(
        name=UpgradeType.SUGAR_WATER,
        cost={ResourceType.FOOD: 100},
        status=Status.ENABLED,
        modifiers={'CLICK': 2.0},  # This upgrade is handled manually in the code check
        check_fn=lambda state: not bought(UpgradeType.SUGAR_WATER, state),
        info=style_info('2x "Gather" rate'),
    ),
    UpgradeType.FIRST_QUEEN: Upgrade(
        name=UpgradeType.FIRST_QUEEN,
        cost={ResourceType.FOOD: 250},
        modifiers={ProducerType.ANT: 2.0},
        check_fn=lambda state: not bought(UpgradeType.FIRST_QUEEN, state)
        and state.producers[ProducerType.ANT].total >= 25,
        info=style_info('2x Ant rate; Unlocks Worker'),
    ),
    UpgradeType.STILTS: Upgrade(
        name=UpgradeType.STILTS,
        cost={ResourceType.FOOD: 500, ResourceType.STICKS: 250},
        modifiers={ProducerType.ANT: 3.0},
        check_fn=lambda state: not bought(UpgradeType.STILTS, state)
        and state.producers[ProducerType.WORKER].status == Status.ENABLED,
        info=style_info('3x Ant rate'),
    ),
    UpgradeType.PACK_FRAME: Upgrade(
        name=UpgradeType.PACK_FRAME,
        cost={ResourceType.FOOD: 1000, ResourceType.STICKS: 500},
        modifiers={ProducerType.ANT: 2.0, ProducerType.WORKER: 2.0},
        check_fn=lambda state: not bought(UpgradeType.PACK_FRAME, state)
        and state.producers[ProducerType.WORKER].status == Status.ENABLED,
        info=style_info('2x Ant/Worker rate'),
    ),
    UpgradeType.WHEEL: Upgrade(
        name=UpgradeType.WHEEL,
        cost={ResourceType.FOOD: 3000, ResourceType.STICKS: 750, ResourceType.STONES: 250},
        modifiers={ProducerType.HAULER: 2.0, ProducerType.WORKER: 2.0},
        check_fn=lambda state: not bought(UpgradeType.WHEEL, state)
        and state.producers[ProducerType.HAULER].status == Status.ENABLED,
        info=style_info('2x Hauler/Worker rate'),
    ),
    UpgradeType.CLUB: Upgrade(
        name=UpgradeType.CLUB,
        cost={ResourceType.FOOD: 5000, ResourceType.STICKS: 2000, ResourceType.STONES: 600},
        modifiers={},
        check_fn=lambda state: not bought(UpgradeType.CLUB, state)
        and state.producers[ProducerType.HAULER].status == Status.ENABLED,
        info=style_info('Unlocks Soldier'),
    ),
    # TODO:  DO WE WANT THIS HERE?  INCREASES CLICK RATE FOR FOO BUT MIGHT NOT BE USEFUL BY THIS POINT.
    # UpgradeType.ENERGY_DRINK: Upgrade(
    #     name=UpgradeType.ENERGY_DRINK,
    #     cost={ResourceType.FOOD: 7500, ResourceType.STICKS: 3500, ResourceType.STONES: 1500},
    #     modifiers={'CLICK': 4.0},
    #     check_fn=lambda state: not bought(UpgradeType.ENERGY_DRINK, state) and bought(UpgradeType.CLUB, state),
    #     info=style_info('4x "Gather" rate'),
    # ),
    UpgradeType.FARMING: Upgrade(
        name=UpgradeType.FARMING,
        cost={ResourceType.FOOD: 3000, ResourceType.LAND: 250},
        modifiers={ProducerType.ANT: 2.0},
        check_fn=lambda state: not bought(UpgradeType.FARMING, state)
        and state.producers[ProducerType.SOLDIER].status == Status.ENABLED,
        info=style_info('2x Ant rate'),
    ),
    UpgradeType.FOREST: Upgrade(
        name=UpgradeType.FOREST,
        cost={ResourceType.FOOD: 5000, ResourceType.STICKS: 750, ResourceType.LAND: 500},
        modifiers={ProducerType.WORKER: 2.0},
        check_fn=lambda state: not bought(UpgradeType.FOREST, state)
        and state.producers[ProducerType.SOLDIER].status == Status.ENABLED,
        info=style_info('2x Worker rate'),
    ),
    UpgradeType.OUTPOST: Upgrade(
        name=UpgradeType.OUTPOST,
        cost={ResourceType.FOOD: 7500, ResourceType.STICKS: 3500, ResourceType.LAND: 1000},
        modifiers={ProducerType.SOLDIER: 2.0},
        check_fn=lambda state: not bought(UpgradeType.OUTPOST, state)
        and state.producers[ProducerType.SOLDIER].status == Status.ENABLED,
        info=style_info('2x Soldier rate'),
    ),
    UpgradeType.QUARRY: Upgrade(
        name=UpgradeType.QUARRY,
        cost={ResourceType.STICKS: 5000, ResourceType.STONES: 1500, ResourceType.LAND: 750},
        modifiers={ProducerType.HAULER: 2.0},
        check_fn=lambda state: not bought(UpgradeType.QUARRY, state)
        and state.producers[ProducerType.SOLDIER].status == Status.ENABLED,
        info=style_info('2x Hauler rate'),
    ),
    UpgradeType.MINING: Upgrade(
        name=UpgradeType.MINING,
        cost={ResourceType.STICKS: 6000, ResourceType.STONES: 2000, ResourceType.LAND: 1500},
        modifiers={ProducerType.HAULER: 2.0, ProducerType.WORKER: 2.0},
        check_fn=lambda state: not bought(UpgradeType.MINING, state) and state.upgrades[UpgradeType.QUARRY].purchased,
        info=style_info('Unlocks Miner'),
    ),
    UpgradeType.METAL_WEAPONS: Upgrade(
        name=UpgradeType.METAL_WEAPONS,
        cost={ResourceType.FOOD: 10000, ResourceType.STICKS: 7000, ResourceType.METAL: 500},
        modifiers={ProducerType.SOLDIER: 2.0},
        check_fn=lambda state: not bought(UpgradeType.METAL_WEAPONS, state)
        and state.producers[ProducerType.MINER].status == Status.ENABLED,
        info=style_info('2x Soldier rate'),
    ),
    UpgradeType.METAL_TOOLS: Upgrade(
        name=UpgradeType.METAL_TOOLS,
        cost={ResourceType.FOOD: 12000, ResourceType.STICKS: 8000, ResourceType.METAL: 750},
        modifiers={ProducerType.ANT: 2.0, ProducerType.HAULER: 2.0, ProducerType.MINER: 2.0},
        check_fn=lambda state: not bought(UpgradeType.METAL_TOOLS, state)
        and state.producers[ProducerType.MINER].status == Status.ENABLED,
        info=style_info('2x Ant/Hauler/Miner rate'),
    ),
}
