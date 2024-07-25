from textual.widgets import Button
from textual.reactive import reactive
from game import GameState
from shared import type_class


class BuyButton(Button):
    game_state: reactive[GameState] = reactive(GameState())

    def __init__(self, key_type: any, amount: int, **kwargs):
        super().__init__(id=f'{type_class(key_type)}-{amount}', classes='buy', disabled=True, **kwargs)
        self.amount = amount

    def on_mount(self) -> None:
        self.label = f'+{self.amount}'
