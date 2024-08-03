from dataclasses import dataclass, field
from datetime import datetime
from math import prod
from typing import Self

from shared import ResourceType, ProducerType, Status, UpgradeType, abbrev_num, style_info
from game.resource import Resource, ALL_RESOURCES
from game.producer import Producer, ALL_PRODUCERS
from game.upgrade import Upgrade, ALL_UPGRADES

# Cookie Clicker implemented a .15 increase in cost for each purchase and scales well
COST_SCALE = 1.15
BOOST_PER_20 = 0.5


@dataclass
class GameState:
    # This can be modified to speed the game production up for debugging purposes
    DEBUG_MULTIPLIER = 5.0

    resources: dict[ResourceType, Resource] = field(default_factory=lambda: ALL_RESOURCES)
    producers: dict[ProducerType, Producer] = field(default_factory=lambda: ALL_PRODUCERS)
    upgrades: dict[UpgradeType, Upgrade] = field(default_factory=lambda: ALL_UPGRADES)
    click_modifier: float = 1.0

    def tick(self) -> None:
        for rtype, resource in self.resources.items():
            self.resources[rtype] += calculate_resource_value(
                rtype, list(self.producers.values()), list(self.upgrades.values())
            )
        self.update_entities()

    def get_status(self, key_type: ResourceType | ProducerType | UpgradeType) -> Status:
        match key_type:
            case t if t in ResourceType:
                if t not in self.resources:
                    return Status.DISABLED
                return self.resources[t].status
            case t if t in ProducerType:
                if t not in self.producers:
                    return Status.DISABLED
                return self.producers[t].status
            case t if t in UpgradeType:
                return self.upgrades[t].status
        return Status.DISABLED

    def gather_rates(self, key_type: ProducerType) -> str:
        p = self.producers[key_type]
        boost_rate = 1.0
        if p.boost:
            boost_rate += p.boost.rate
        gather_txt = '[i]'
        gather_txt += ', '.join([f'{abbrev_num(r * p.total * boost_rate)} {n}' for n, r in p.rates.items()])
        gather_txt += '/s[/i]'
        return gather_txt

    def purchase_producer(self, producer: ProducerType, amount: int, spend: bool = True) -> None:
        purchased = 0
        # We must loop here to allow cost to scale in between purchases of more than 1 producer
        while True:
            new_cost = self.producers[producer].cost
            if spend and not all(self.resources[r].total >= c for r, c in new_cost.items()):
                # Can't afford it with one or more resources
                break
            for resource, cost in new_cost.items():
                if spend:
                    self.resources[resource].total -= cost
                new_cost[resource] = int(round(cost * COST_SCALE))
            self.producers[producer].total += 1
            self.producers[producer].cost = new_cost
            purchased += 1
            # If amount is 0, we're 'buying MAX' and we should keep going until we can't afford more
            if amount > 0 and purchased == amount:
                break

    def purchase_upgrade(self, upgrade: UpgradeType) -> None:
        if not all(self.resources[r].total >= c for r, c in self.upgrades[upgrade].cost.items()):
            # Can't afford it with one or more resources
            return
        for resource, cost in self.upgrades[upgrade].cost.items():
            self.resources[resource].total -= cost
        self.upgrades[upgrade].total = 1
        self.upgrades[upgrade].purchased = True
        for producer, modifier in self.upgrades[upgrade].modifiers.items():
            if producer == 'CLICK':
                self.click_modifier *= modifier
                continue
            for resource, rate in self.producers[producer].rates.items():
                self.producers[producer][resource] = rate * modifier
        if boost := self.upgrades[upgrade].boost:
            self.producers[boost.target].boost = boost
            old_producer = self.producers[boost.cost]
            self.producers[boost.cost].status = Status.DISABLED
            self.producers[boost.target].boost.rate = old_producer.total / 20 * BOOST_PER_20
            for resource in old_producer.rates.keys():
                self.resources[resource].status = Status.DISABLED
            # Probably not necessary but helps with double-clicking accidentally.
            self.upgrades[upgrade].boost = None
        if replace := self.upgrades[upgrade].replace:
            replace.created = replace.created
            for resource in self.producers[replace.created].rates.keys():
                self.resources[resource].status = Status.DISABLED
            self.producers[replace.old].status = Status.DISABLED
            new_total = round(self.producers[replace.old].total / replace.divisor)
            # This will simulate purchasing the new producer, updating totals, rates, and costs
            self.purchase_producer(replace.created, new_total, spend=False)
        if all(u.purchased for u in self.upgrades.values()):
            self.write_stats()

    def write_stats(self: Self) -> None:
        with open('stats.txt', 'a') as f:
            f.write(f'\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:\n')
            for rtype, resource in self.resources.items():
                f.write(f'  {rtype}: {resource.total}\n')
            for ptype, producer in self.producers.items():
                f.write(f'  {ptype}: {producer.total}\n')
            f.write('-> CHANGES: \n')

    def update_entities(self: Self) -> None:
        # TODO:  [FUTURE]:  Some animation or effect to show new entities being revealed!
        for rtype, resource in self.resources.items():
            self.resources[rtype].status = Status.from_bool(resource.check_fn(self))
        for ptype, producer in self.producers.items():
            self.producers[ptype].status = Status.from_bool(producer.check_fn(self))
            if producer.boost:
                producer.boost.timer -= 1
                if producer.boost.timer < 0:
                    self.producers[ptype].boost = None
        for utype, upgrade in self.upgrades.items():
            upgrade.status = Status.from_bool(upgrade.check_fn(self))
            if boost := upgrade.boost:
                new_rate = round(1.0 + (self.producers[boost.cost].total / 20 * BOOST_PER_20), 2)
                self.upgrades[utype].boost.rate = new_rate
                self.upgrades[utype].info = style_info(f'[green]⬆[/] {boost.target} rate by {new_rate}x for 30s')


def calculate_resource_value(resource: ResourceType, producers: list[Producer], upgrades: list[Upgrade]) -> Resource:
    """
    Given a list of producers, calculate the total value of a resource
    produced by them all combined.
    """
    # TODO: Fix this;  It should be centered on Producers, since no two producers produce the same
    #       resource, but it's currently centered on resources.
    produced: float = 0.0
    for p in [pr for pr in producers if resource in pr.rates]:
        # Calculate the total produced by this producer by multiplying producer rates
        boost = 1.0 if not p.boost else p.boost.rate
        produced += prod([p[resource], boost, p.total, GameState.DEBUG_MULTIPLIER])
    total, progress = divmod(produced, 1)
    return Resource(resource, int(total), progress)
