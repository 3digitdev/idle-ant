from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widgets import Button, Static
from textual.containers import Horizontal
from constants import ResourceType, ProducerType
from game import GameState
from widgets import BuyButton


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
