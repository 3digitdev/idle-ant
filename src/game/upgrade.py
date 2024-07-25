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
    cost: list[tuple[ResourceType, int]]
    modifiers: dict[ProducerType, float]
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
        cost=[(ResourceType.FOOD, 250)],
        modifiers={ProducerType.ANT: 2.0},
        check_fn=lambda state: not bought(UpgradeType.FIRST_QUEEN, state)
        and state.producers[ProducerType.ANT].total >= 100,
    ),
    UpgradeType.STILTS: Upgrade(
        name=UpgradeType.STILTS,
        cost=[(ResourceType.FOOD, 500), (ResourceType.STICKS, 250)],
        modifiers={ProducerType.WORKER: 2.0},
        check_fn=lambda state: not bought(UpgradeType.STILTS, state)
        and state.producers[ProducerType.WORKER].total >= 1,
    ),
}
