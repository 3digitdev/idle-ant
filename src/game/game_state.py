from dataclasses import dataclass, field

from constants import ResourceType, ProducerType, Status
from resources import Resource
from producers import Producer


@dataclass
class GameState:
    resources: dict[ResourceType, Resource] = field(
        default_factory=lambda: {
            ResourceType.FOOD: Resource(name=ResourceType.FOOD, status=Status.ENABLED),
            ResourceType.STICKS: Resource(name=ResourceType.STICKS, status=Status.SOON),
        }
    )
    producers: dict[ProducerType, Producer] = field(
        default_factory=lambda: {
            ProducerType.IDLE: Producer(name=ProducerType.IDLE, cost=None, total=1, rates={ResourceType.FOOD: 1}),
            ProducerType.WORKER: Producer(
                name=ProducerType.WORKER, cost=(ResourceType.FOOD, 10), total=1, rates={ResourceType.FOOD: 1}
            ),
        }
    )

    def tick(self) -> None:
        for rtype, resource in self.resources.items():
            if resource.status != Status.ENABLED:
                continue
            self.resources[rtype] += calculate_resource_value(rtype, list(self.producers.values()))

    def purchase(self, producer: ProducerType, amount: int) -> None:
        if self.producers[producer].cost:
            resource, cost = self.producers[producer].cost
            if not self.resources[resource].total >= cost * amount:
                return
            self.resources[resource].total -= cost * amount
            self.producers[producer].total += amount


def calculate_resource_value(resource: ResourceType, producers: list[Producer]) -> Resource:
    """
    Given a list of producers, calculate the total value of a resource
    produced by them all combined.
    """
    total, progress = divmod(sum(p[resource] * p.total for p in producers), 1)
    return Resource(resource, total, progress)
