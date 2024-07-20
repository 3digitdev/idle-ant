from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widgets import Button, Static
from textual.containers import Horizontal
from constants import ResourceType, ProducerType, UpgradeType, Status
from game import GameState
from widgets import BuyButton


class RowEntry(Horizontal):
    game_state: reactive[GameState] = reactive(GameState())
    is_food: bool = False
    is_producer: bool = False
    is_upgrade: bool = False

    def __init__(self, obj_type: ResourceType | ProducerType | UpgradeType, status: Status):
        super().__init__()
        self.obj_type = obj_type
        self.status = status
        match self.obj_type:
            case ResourceType.FOOD:
                self.is_food = True
            case t if t in ProducerType:
                self.is_producer = True
            case t if t in UpgradeType:
                self.is_upgrade = True
            case _:
                pass
        classes = ['entry-row']
        if self.is_food:
            classes.append('food-row')
        if self.status == Status.DISABLED:
            classes.append('hidden')
        self.classes = classes

    def compose(self) -> ComposeResult:
        yield Static(str(self.obj_type), classes='entry-text' + (' food' if self.is_food else ''))
        yield Static('-', classes='entry-value' + (' food' if self.is_food else ''))
        if self.is_food:
            yield Button('Gather', id='gather', classes='gather-btn', variant='success')
        if self.is_producer or self.is_upgrade:
            yield Horizontal(
                BuyButton(key_type=self.obj_type, amount=1, id=f'{self.obj_type}-1', classes='buy', disabled=True),
                BuyButton(key_type=self.obj_type, amount=5, id=f'{self.obj_type}-5', classes='buy', disabled=True),
                classes='entry-buttons',
            )

    def btn_state(self, btn: BuyButton) -> bool:
        if self.is_producer:
            resource, cost = self.game_state.producers[self.obj_type].cost
        elif self.is_upgrade:
            resource, cost = self.game_state.upgrades[self.obj_type].cost
        can_buy = {str(k): self.game_state.resources[resource].total >= cost * k for k in [1, 5]}
        return can_buy[str(btn.amount)]

    def watch_game_state(self, game_state: GameState) -> None:
        self.game_state = game_state
        self.status = game_state.get_status(self.obj_type)
        if self.status != Status.DISABLED:
            self.classes = [x for x in self.classes if x != 'hidden']
        if self.is_producer:
            self.query_one('.entry-value', Static).update(str(game_state.producers[self.obj_type].total))
            btns = self.query('.buy')
            for btn in btns:
                btn.disabled = not self.btn_state(btn)
        elif self.is_upgrade:
            self.query_one('.entry-value', Static).update(str(game_state.upgrades[self.obj_type].total))
            btns = self.query('.buy')
            for btn in btns:
                btn.disabled = not self.btn_state(btn)
        else:
            self.query_one('.entry-value', Static).update(str(game_state.resources[self.obj_type].total))
