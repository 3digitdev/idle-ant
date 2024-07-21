from textual.app import ComposeResult
from textual.reactive import reactive
from textual.containers import ScrollableContainer
from constants import ResourceType, ProducerType, UpgradeType
from game import GameState
from widgets.containers import ResourceRow, ProducerRow, UpgradeRow


class UpgradesColumn(ScrollableContainer):
    BORDER_TITLE = 'Upgrades'
    DEFAULT_CLASSES = 'display-column'

    game_state: reactive[GameState] = reactive(GameState())

    def compose(self) -> ComposeResult:
        for upgrade in UpgradeType:
            yield UpgradeRow(upgrade, self.game_state.get_status(upgrade)).data_bind(UpgradesColumn.game_state)


class ProducersColumn(ScrollableContainer):
    BORDER_TITLE = 'Producers'
    DEFAULT_CLASSES = 'display-column'

    game_state: reactive[GameState] = reactive(GameState())

    def compose(self) -> ComposeResult:
        for producer in ProducerType:
            yield ProducerRow(producer, self.game_state.get_status(producer)).data_bind(ProducersColumn.game_state)


class ResourcesColumn(ScrollableContainer):
    BORDER_TITLE = 'Resources'
    DEFAULT_CLASSES = 'display-column'

    game_state: reactive[GameState] = reactive(GameState())

    def compose(self) -> ComposeResult:
        for resource in ResourceType:
            yield ResourceRow(resource, self.game_state.get_status(resource)).data_bind(ResourcesColumn.game_state)
