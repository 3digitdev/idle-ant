from textual.app import ComposeResult
from textual.reactive import reactive
from textual.containers import ScrollableContainer
from shared import ResourceType, ProducerType, UpgradeType
from game import GameState
from widgets.rows import ResourceRow, ProducerRow, UpgradeRow


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

    def on_mount(self) -> None:
        for producer in ProducerType:
            cost_str = '[b]Cost:[/b]\n  '
            costs = '\n  '.join([f'[b]{c}[/b] {r}' for r, c in self.game_state.producers[producer].cost])
            self.query_one(f'.{producer.lower()}-row', ProducerRow).tooltip = cost_str + costs

    def compose(self) -> ComposeResult:
        for producer in ProducerType:
            yield ProducerRow(ProducerType(producer), self.game_state.get_status(producer)).data_bind(
                ProducersColumn.game_state
            )


class UpgradesColumn(ScrollableContainer):
    BORDER_TITLE = 'Upgrades'
    DEFAULT_CLASSES = 'display-column'

    game_state: reactive[GameState] = reactive(GameState())

    def on_mount(self) -> None:
        for upgrade in UpgradeType:
            cost_str = '[b]Cost:[/b]\n  '
            costs = '\n  '.join([f'[b]{c}[/b] {r}' for r, c in self.game_state.upgrades[upgrade].cost])
            self.query_one(f'.{upgrade.lower()}-row', UpgradeRow).tooltip = cost_str + costs

    def compose(self) -> ComposeResult:
        for upgrade in UpgradeType:
            yield UpgradeRow(UpgradeType(upgrade), self.game_state.get_status(upgrade)).data_bind(
                UpgradesColumn.game_state
            )
