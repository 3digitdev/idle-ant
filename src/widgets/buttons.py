from textual.widgets import Button
from textual.reactive import reactive

from constants import ProducerType
from game import GameState


class BuyButton(Button):
    game_state: reactive[GameState] = reactive(GameState())

    def __init__(self, *args, key_type: ProducerType, amount: int, **kwargs):
        super().__init__(*args, **kwargs)
        self.key_type = key_type
        self.amount = amount

    def on_mount(self) -> None:
        self.label = f'+{self.amount}'
