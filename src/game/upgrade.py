from dataclasses import dataclass

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
    status: Status = Status.DISABLED

    def __getitem__(self, producer: ProducerType) -> float:
        return self.modifiers[producer]

    def __setitem__(self, producer: ProducerType, value: float) -> None:
        self.modifiers[producer] = value


# NOTE:  ALL UPGRADES' MODIFIERS SHOULD BE 1.0 OR GREATER TO AVOID NEGATIVE PRODUCTION RATES!
ALL_UPGRADES = {
    UpgradeType.STILTS: Upgrade(
        name=UpgradeType.STILTS,
        cost=[(ResourceType.FOOD, 5), (ResourceType.STICKS, 6)],
        modifiers={ProducerType.WORKER: 2.0},
    ),
}
