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
        yield UpgradeRow(UpgradeType.STILTS, self.game_state.get_status(UpgradeType.STILTS)).data_bind(
            UpgradesColumn.game_state
        )


class ProducersColumn(ScrollableContainer):
    BORDER_TITLE = 'Producers'
    DEFAULT_CLASSES = 'display-column'

    game_state: reactive[GameState] = reactive(GameState())

    def compose(self) -> ComposeResult:
        yield ProducerRow(ProducerType.WORKER, self.game_state.get_status(ProducerType.WORKER)).data_bind(
            ProducersColumn.game_state
        )


class ResourcesColumn(ScrollableContainer):
    BORDER_TITLE = 'Resources'
    DEFAULT_CLASSES = 'display-column'

    game_state: reactive[GameState] = reactive(GameState())

    def compose(self) -> ComposeResult:
        yield ResourceRow(ResourceType.FOOD, self.game_state.get_status(ResourceType.FOOD)).data_bind(
            ResourcesColumn.game_state
        )
        yield ResourceRow(ResourceType.STICKS, self.game_state.get_status(ResourceType.STICKS)).data_bind(
            ResourcesColumn.game_state
        )
