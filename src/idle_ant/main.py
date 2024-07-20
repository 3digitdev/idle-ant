from collections import defaultdict
from dataclasses import dataclass, field
from enum import StrEnum, Enum, auto
from time import monotonic
from typing import Self

from textual.timer import Timer
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer, HorizontalScroll, Container, Horizontal
from textual.reactive import reactive
from textual.widgets import Header, Footer, Static, Button


class GameClock(Static):
    start_time: reactive[float] = reactive(monotonic())
    time: reactive[float] = reactive(0.0)
    update_timer: Timer | None = None

    def on_mount(self) -> None:
        self.update_timer = self.set_interval(interval=1, callback=self.update_time)

    def update_time(self) -> None:
        self.time = monotonic() - self.start_time

    def watch_time(self, time: float) -> None:
        min, sec = divmod(time, 60)
        hr, min = divmod(min, 60)
        d, hr = divmod(hr, 24)
        wk, d = divmod(d, 7)
        mt, wk = divmod(wk, 4)
        yr, mt = divmod(mt, 12)
        result = 'Elapsed Time: '
        if yr:
            result += f'{yr:,.0f}y, '
        if mt:
            result += f'{mt:,.0f}m, '
        if wk:
            result += f'{wk:,.0f}w, '
        if d:
            result += f'{d:,.0f}d, '
        result += f'{hr:02,.0f}:{min:02,.0f}:{sec:02.0f}'
        self.update(result)


class ResourceType(StrEnum):
    FOOD = 'Food'
    STICKS = 'Sticks'


class ProducerType(StrEnum):
    IDLE = 'Idle'
    WORKER = 'Workers'


class Status(Enum):
    DISABLED = auto()
    ENABLED = auto()
    SOON = auto()


@dataclass
class Resource:
    """A base 'resource' type, which helps calculate progress to a future full value."""

    name: ResourceType
    total: int = 0
    progress: float = 0.0
    status: Status = Status.DISABLED

    def __add__(self, other: Self | float) -> Self:
        if not isinstance(other, float):
            extra, self.progress = divmod(self.progress + other.progress, 1)
            self.total += int(other.total + extra)
        else:
            total, self.progress = divmod(self.total + self.progress + other, 1)
            self.total = int(total)
        return self

    def __str__(self) -> str:
        return f'{self.name}: {self.total}'


@dataclass
class Producer:
    """
    A base 'producer' type, which can produce resources at given rates.

    A single producer may produce many different resources, and the rates may change
    from modifiers due to other factors.
    """

    name: ProducerType
    cost: tuple[ResourceType, int] | None = None
    total: int = 0
    rates: dict[ResourceType, float] = field(default_factory=lambda: defaultdict(float))

    def __getitem__(self, resource: ResourceType) -> float:
        return self.rates[resource]

    def __setitem__(self, resource: ResourceType, value: float) -> None:
        self.rates[resource] = value


def calculate_resource_value(resource: ResourceType, producers: list[Producer]) -> Resource:
    """
    Given a list of producers, calculate the total value of a resource
    produced by them all combined.
    """
    total, progress = divmod(sum(p[resource] * p.total for p in producers), 1)
    return Resource(resource, total, progress)


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


class BuyButton(Button):
    game_state: reactive[GameState] = reactive(GameState())

    def __init__(self, *args, key_type: ProducerType, amount: int, **kwargs):
        super().__init__(*args, **kwargs)
        self.key_type = key_type
        self.amount = amount

    def on_mount(self) -> None:
        self.label = f'+{self.amount}'


class RowEntry(Horizontal):
    game_state: reactive[GameState] = reactive(GameState())

    def __init__(self, obj_type: ResourceType | ProducerType):
        super().__init__()
        self.obj_type = obj_type
        self.is_food = isinstance(self.obj_type, ResourceType) and self.obj_type == ResourceType.FOOD
        self.is_producer = isinstance(self.obj_type, ProducerType)
        self.classes = [x for x in ['entry-row', 'food-row' if self.is_food else ''] if x != '']

    def compose(self) -> ComposeResult:
        yield Static(str(self.obj_type), classes='entry-text' + (' food' if self.is_food else ''))
        yield Static('-', classes='entry-value' + (' food' if self.is_food else ''))
        if self.is_food:
            yield Button('Gather', id='gather', classes='gather-btn', variant='success')
        if self.is_producer:
            yield Horizontal(
                BuyButton(key_type=self.obj_type, amount=1, id=f'{self.obj_type}-1', classes='buy', disabled=True),
                BuyButton(key_type=self.obj_type, amount=5, id=f'{self.obj_type}-5', classes='buy', disabled=True),
                classes='entry-buttons',
            )

    def btn_state(self, btn: BuyButton) -> bool:
        resource, cost = self.game_state.producers[self.obj_type].cost
        can_buy = {str(k): self.game_state.resources[resource].total >= cost * k for k in [1, 5]}
        return can_buy[str(btn.amount)]

    def watch_game_state(self, game_state: GameState) -> None:
        self.game_state = game_state
        if self.is_producer:
            self.query_one('.entry-value', Static).update(str(game_state.producers[self.obj_type].total))
            btns = self.query('.buy')
            for btn in btns:
                btn.disabled = not self.btn_state(btn)
        else:
            self.query_one('.entry-value', Static).update(str(game_state.resources[self.obj_type].total))


class ProducersColumn(ScrollableContainer):
    game_state: reactive[GameState] = reactive(GameState())

    def on_mount(self) -> None:
        self.border_title = 'Producers'
        self.classes = ['display-column']

    def compose(self) -> ComposeResult:
        yield RowEntry(ProducerType.WORKER).data_bind(ProducersColumn.game_state)

    def watch_game_state(self, game_state: GameState) -> None:
        self.game_state = game_state


class ResourcesColumn(ScrollableContainer):
    game_state: reactive[GameState] = reactive(GameState())

    def on_mount(self) -> None:
        self.border_title = 'Resources'
        self.classes = ['display-column']

    def compose(self) -> ComposeResult:
        yield RowEntry(ResourceType.FOOD).data_bind(ResourcesColumn.game_state)

    def watch_game_state(self, game_state: GameState) -> None:
        self.game_state = game_state


class ColumnsContainer(HorizontalScroll):
    game_state: reactive[GameState] = reactive(GameState())

    def compose(self) -> ComposeResult:
        yield ResourcesColumn().data_bind(ColumnsContainer.game_state)
        yield ProducersColumn().data_bind(ColumnsContainer.game_state)

    def watch_game_state(self, game_state: GameState) -> None:
        self.game_state = game_state


class GameContainer(Static):
    game_state: reactive[GameState] = reactive(GameState(), recompose=True)

    def on_mount(self) -> None:
        self.set_interval(interval=1, callback=self.update_game_state)

    def compose(self) -> ComposeResult:
        yield ColumnsContainer().data_bind(GameContainer.game_state)

    def update_game_state(self) -> None:
        self.game_state.tick()
        self.mutate_reactive(GameContainer.game_state)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        match event.button.id.split('-'):
            case ['gather']:
                self.game_state.resources[ResourceType.FOOD].total += 1
            case [obj_type, num]:
                self.game_state.purchase(ProducerType(obj_type), int(num))
            case _:
                pass
        self.mutate_reactive(GameContainer.game_state)


class IdleApp(App):
    CSS_PATH = 'idle.tcss'
    BINDINGS = [
        ('q', 'quit', 'Quit'),
    ]

    def on_mount(self) -> None:
        self.title = 'Antics'

    def compose(self) -> ComposeResult:
        yield Header()
        yield GameContainer(id='game_container')
        yield Container(GameClock(), id='clock_container')
        yield Footer()


if __name__ == '__main__':
    app = IdleApp()
    app.run()
