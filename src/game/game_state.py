from dataclasses import dataclass, field
from math import prod
from typing import Self

from shared import ResourceType, ProducerType, Status, UpgradeType
from game.resource import Resource
from game.producer import Producer
from game.upgrade import Upgrade


@dataclass
class GameState:
    # This can be modified to speed the game production up for debugging purposes
    DEBUG_MULTIPLIER = 1

    resources: dict[ResourceType, Resource] = field(
        default_factory=lambda: {
            ResourceType.FOOD: Resource(name=ResourceType.FOOD, status=Status.ENABLED),
            ResourceType.STICKS: Resource(name=ResourceType.STICKS),
        }
    )
    producers: dict[ProducerType, Producer] = field(
        default_factory=lambda: {
            ProducerType.WORKER: Producer(
                name=ProducerType.WORKER,
                status=Status.ENABLED,
                cost=(ResourceType.FOOD, 10),
                rates={ResourceType.FOOD: 0.5, ResourceType.STICKS: 0.25},
            ),
        }
    )
    # NOTE:  ALL UPGRADES' MODIFIERS SHOULD BE 1.0 OR GREATER TO AVOID NEGATIVE PRODUCTION RATES!
    upgrades: dict[UpgradeType, Upgrade] = field(
        default_factory=lambda: {
            UpgradeType.STILTS: Upgrade(
                name=UpgradeType.STILTS, cost=(ResourceType.STICKS, 10), total=0, modifiers={ProducerType.WORKER: 1.5}
            ),
        }
    )

    def tick(self) -> None:
        for rtype, resource in self.resources.items():
            self.resources[rtype] += calculate_resource_value(
                rtype, list(self.producers.values()), list(self.upgrades.values())
            )
        self.update_visibilities()

    def get_status(self, key_type: ResourceType | ProducerType | UpgradeType) -> Status:
        match key_type:
            case t if t in ResourceType:
                return self.resources[t].status
            case t if t in ProducerType:
                return self.producers[t].status
            case t if t in UpgradeType:
                return self.upgrades[t].status
        return Status.DISABLED

    def purchase_producer(self, producer: ProducerType, amount: int) -> None:
        if self.producers[producer].cost:
            resource, cost = self.producers[producer].cost
            if not self.resources[resource].total >= cost * amount:
                return
            self.resources[resource].total -= cost * amount
            self.producers[producer].total += amount

    def purchase_upgrade(self, upgrade: UpgradeType, amount: int) -> None:
        if self.upgrades[upgrade].cost:
            resource, cost = self.upgrades[upgrade].cost
            if not self.resources[resource].total >= cost * amount:
                return
            self.resources[resource].total -= cost * amount
            self.upgrades[upgrade].total += amount

    def update_visibilities(self: Self) -> None:
        # TODO:  [FUTURE]:  Some animation or effect to show new entities being revealed!
        for rtype, resource in self.resources.items():
            if resource.total > 0:
                resource.status = Status.ENABLED
            self.resources[rtype] = resource
        for ptype, producer in self.producers.items():
            resource, _ = producer.cost
            if self.resources[resource].status == Status.ENABLED:
                producer.status = Status.ENABLED
            self.producers[ptype] = producer
        for utype, upgrade in self.upgrades.items():
            resource, _ = upgrade.cost
            if self.resources[resource].status == Status.ENABLED:
                upgrade.status = Status.ENABLED
            self.upgrades[utype] = upgrade


def calculate_resource_value(resource: ResourceType, producers: list[Producer], upgrades: list[Upgrade]) -> Resource:
    """
    Given a list of producers, calculate the total value of a resource
    produced by them all combined.
    """
    produced: float = 0.0
    for p in [pr for pr in producers if resource in pr.rates]:
        # Collect all applicable upgrades for this producer
        usable = [u[p.name] * u.total for u in upgrades if p.name in u.modifiers]
        # Calculate the total produced by this producer by multiplying upgrades and producer rates
        produced += prod([*[u for u in usable if u > 0.0], p[resource], p.total]) * GameState.DEBUG_MULTIPLIER
        print(f'{p.name} produces {produced} {resource.name}(s) with {usable} upgrades.')
    total, progress = divmod(produced, 1)
    return Resource(resource, total, progress)
