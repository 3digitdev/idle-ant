from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widgets import Button, Static
from constants import ResourceType, ProducerType, UpgradeType
from game import GameState
from widgets.containers import ColumnsContainer


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
            case [obj_type, num] if obj_type in ProducerType:
                self.game_state.purchase_producer(ProducerType(obj_type), int(num))
            case [obj_type, num] if obj_type in UpgradeType:
                self.game_state.purchase_upgrade(UpgradeType(obj_type), int(num))
            case _:
                pass
        self.mutate_reactive(GameContainer.game_state)
