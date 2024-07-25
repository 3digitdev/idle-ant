from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widgets import Button, Static
from textual.containers import Horizontal
from shared import ResourceType, ProducerType, UpgradeType, Status, abbrev_num, type_class
from game import GameState
from widgets import BuyButton


class Row(Horizontal):
    game_state: reactive[GameState] = reactive(GameState())

    def __init__(self, key_type: ResourceType | ProducerType | UpgradeType, status: Status):
        super().__init__()
        self.key_type = key_type
        self.status = status
        classes = ['entry-row', f'{type_class(key_type)}-row']
        if self.key_type == ResourceType.FOOD:
            classes.append('food-row')
        if self.status == Status.DISABLED:
            classes.append('hidden')
        self.classes = classes

    def compose_text(self, is_food: bool = False) -> ComposeResult:
        yield Static(str(self.key_type), classes='entry-text' + (' food' if is_food else ''))
        yield Static('0', classes='entry-value' + (' food' if is_food else ''))

    def compose_non_resource(self) -> ComposeResult:
        yield from self.compose_text(self.key_type == ResourceType.FOOD)
        yield Horizontal(
            BuyButton(key_type=self.key_type, amount=1),
            BuyButton(key_type=self.key_type, amount=5),
            classes='entry-buttons',
        )

    def btn_disabled(self, btn: BuyButton, record: dict) -> bool:
        mult = btn.amount if isinstance(btn, BuyButton) else 1
        for resource, cost in record[self.key_type].cost:
            if self.game_state.resources[resource].total < cost * mult:
                return True
        return False

    def update_btn_states(self, record: dict) -> None:
        btns = self.query('.buy')
        for btn in btns:
            btn.disabled = self.btn_disabled(btn, record)

    def _game_state(self, game_state: GameState, new_total: int) -> None:
        self.status = game_state.get_status(self.key_type)
        if self.status != Status.DISABLED:
            self.classes = [x for x in self.classes if x != 'hidden']
        self.query_one('.entry-value', Static).update(abbrev_num(new_total))


class ResourceRow(Row):
    is_food: bool = False

    def __init__(self, key_type: ResourceType, status: Status):
        super().__init__(key_type=key_type, status=status)
        self.is_food = self.key_type == ResourceType.FOOD

    def compose(self) -> ComposeResult:
        yield from self.compose_text(self.is_food)
        if self.is_food:
            yield Button('Gather', id='gather', classes='gather-btn', variant='success')

    def watch_game_state(self, game_state: GameState) -> None:
        super()._game_state(game_state, game_state.resources[self.key_type].total)


class ProducerRow(Row):
    def compose(self) -> ComposeResult:
        yield from self.compose_text(self.key_type == ResourceType.FOOD)
        yield Horizontal(
            BuyButton(key_type=self.key_type, amount=1),
            BuyButton(key_type=self.key_type, amount=5),
            classes='entry-buttons',
        )

    def on_mount(self) -> None:
        cost_str = '\n'.join([f'{c} {r}' for r, c in self.game_state.producers[self.key_type].cost])
        self.query_one('.entry-value', Static).tooltip = cost_str

    def watch_game_state(self, game_state: GameState) -> None:
        super()._game_state(game_state, game_state.producers[self.key_type].total)
        self.update_btn_states(game_state.producers)


class UpgradeRow(Row):
    def compose(self) -> ComposeResult:
        yield from self.compose_text(self.key_type == ResourceType.FOOD)
        yield Horizontal(
            Button(
                label='Buy',
                id=f'{type_class(self.key_type)}-upgrade',
                classes='buy',
                disabled=True,
            ),
            classes='entry-buttons',
        )

    def watch_game_state(self, game_state: GameState) -> None:
        super()._game_state(game_state, game_state.upgrades[self.key_type].total)
        self.update_btn_states(game_state.upgrades)
