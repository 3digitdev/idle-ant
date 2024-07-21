from textual.app import ComposeResult
from textual.reactive import reactive
from textual.containers import ScrollableContainer
from textual.widgets import Button
from constants import ResourceType, ProducerType, UpgradeType
from game import GameState
from widgets.containers import ResourceRow, ProducerRow, UpgradeRow


class ResourcesColumn(ScrollableContainer):
    BORDER_TITLE = 'Resources'
    DEFAULT_CLASSES = 'display-column'

    game_state: reactive[GameState] = reactive(GameState())

    def compose(self) -> ComposeResult:
        for resource in ResourceType:
            yield ResourceRow(ResourceType(resource), self.game_state.get_status(resource)).data_bind(
                ResourcesColumn.game_state
            )


class ProducersColumn(ScrollableContainer):
    BORDER_TITLE = 'Producers'
    DEFAULT_CLASSES = 'display-column'

    game_state: reactive[GameState] = reactive(GameState())

    def compose(self) -> ComposeResult:
        for producer in ProducerType:
            yield ProducerRow(ProducerType(producer), self.game_state.get_status(producer)).data_bind(
                ProducersColumn.game_state
            )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        match event.button.id.split('-'):
            case [obj_type, num] if obj_type in ProducerType:
                self.game_state.purchase_producer(ProducerType(obj_type), int(num))
                self.mutate_reactive(ProducersColumn.game_state)
            case _:
                pass


class UpgradesColumn(ScrollableContainer):
    BORDER_TITLE = 'Upgrades'
    DEFAULT_CLASSES = 'display-column'

    game_state: reactive[GameState] = reactive(GameState())

    def compose(self) -> ComposeResult:
        for upgrade in UpgradeType:
            yield UpgradeRow(UpgradeType(upgrade), self.game_state.get_status(upgrade)).data_bind(
                UpgradesColumn.game_state
            )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        match event.button.id.split('-'):
            case [obj_type, num] if obj_type in UpgradeType:
                self.game_state.purchase_upgrade(UpgradeType(obj_type), int(num))
                self.mutate_reactive(ProducersColumn.game_state)
            case _:
                pass
