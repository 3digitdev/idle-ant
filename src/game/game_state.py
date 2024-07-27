from dataclasses import dataclass, field
from math import prod
from typing import Self

from shared import ResourceType, ProducerType, Status, UpgradeType, abbrev_num
from game.resource import Resource, ALL_RESOURCES
from game.producer import Producer, ALL_PRODUCERS
from game.upgrade import Upgrade, ALL_UPGRADES


@dataclass
class GameState:
    # This can be modified to speed the game production up for debugging purposes
    DEBUG_MULTIPLIER = 2.0

    resources: dict[ResourceType, Resource] = field(default_factory=lambda: ALL_RESOURCES)
    producers: dict[ProducerType, Producer] = field(default_factory=lambda: ALL_PRODUCERS)
    upgrades: dict[UpgradeType, Upgrade] = field(default_factory=lambda: ALL_UPGRADES)

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

    def gather_rates(self, key_type: ProducerType) -> str:
        p = self.producers[key_type]
        gather_txt = '[i]'
        gather_txt += ', '.join([f'{abbrev_num(r * p.total)} {n}' for n, r in p.rates.items()])
        gather_txt += '/s[/i]'
        return gather_txt

    def purchase_producer(self, producer: ProducerType, amount: int) -> None:
        if amount == 0:
            # Purchase as many as possible
            for resource, cost in self.producers[producer].cost:
                bought, rem = divmod(self.resources[resource].total, cost)
                self.resources[resource].total = rem
                self.producers[producer].total += bought
            return
        if not all(self.resources[r].total >= c * amount for r, c in self.producers[producer].cost):
            # Can't afford it with one or more resources
            return
        for resource, cost in self.producers[producer].cost:
            self.resources[resource].total -= cost * amount
        self.producers[producer].total += amount

    def purchase_upgrade(self, upgrade: UpgradeType) -> None:
        if not all(self.resources[r].total >= c for r, c in self.upgrades[upgrade].cost):
            # Can't afford it with one or more resources
            return
        for resource, cost in self.upgrades[upgrade].cost:
            self.resources[resource].total -= cost
        self.upgrades[upgrade].total = 1
        self.upgrades[upgrade].purchased = True
        for producer, modifier in self.upgrades[upgrade].modifiers.items():
            for resource, rate in self.producers[producer].rates.items():
                self.producers[producer][resource] = rate * modifier

    def update_visibilities(self: Self) -> None:
        # TODO:  [FUTURE]:  Some animation or effect to show new entities being revealed!
        for rtype, resource in self.resources.items():
            # TODO: check_fn isn't working properly!
            self.resources[rtype].status = Status.from_bool(resource.check_fn(self))
        for ptype, producer in self.producers.items():
            self.producers[ptype].status = Status.from_bool(producer.check_fn(self))
        for utype, upgrade in self.upgrades.items():
            self.upgrades[utype].status = Status.from_bool(upgrade.check_fn(self))


def calculate_resource_value(resource: ResourceType, producers: list[Producer], upgrades: list[Upgrade]) -> Resource:
    """
    Given a list of producers, calculate the total value of a resource
    produced by them all combined.
    """
    produced: float = 0.0
    for p in [pr for pr in producers if resource in pr.rates]:
        # Calculate the total produced by this producer by multiplying producer rates
        produced += prod([p[resource], p.total, GameState.DEBUG_MULTIPLIER])
    total, progress = divmod(produced, 1)
    return Resource(resource, int(total), progress)
