from textual.app import ComposeResult
from textual.reactive import reactive
from textual.containers import ScrollableContainer, HorizontalScroll
from constants import ResourceType, ProducerType, UpgradeType
from game import GameState
from widgets.containers import RowEntry


class UpgradesColumn(ScrollableContainer):
    game_state: reactive[GameState] = reactive(GameState())

    def on_mount(self) -> None:
        self.border_title = 'Upgrades'
        self.classes = ['display-column']

    def compose(self) -> ComposeResult:
        yield RowEntry(UpgradeType.STILTS, self.game_state.get_status(UpgradeType.STILTS)).data_bind(
            UpgradesColumn.game_state
        )

    def watch_game_state(self, game_state: GameState) -> None:
        self.game_state = game_state


class ProducersColumn(ScrollableContainer):
    game_state: reactive[GameState] = reactive(GameState())

    def on_mount(self) -> None:
        self.border_title = 'Producers'
        self.classes = ['display-column']

    def compose(self) -> ComposeResult:
        yield RowEntry(ProducerType.WORKER, self.game_state.get_status(ProducerType.WORKER)).data_bind(
            ProducersColumn.game_state
        )

    def watch_game_state(self, game_state: GameState) -> None:
        self.game_state = game_state


class ResourcesColumn(ScrollableContainer):
    game_state: reactive[GameState] = reactive(GameState())

    def on_mount(self) -> None:
        self.border_title = 'Resources'
        self.classes = ['display-column']

    def compose(self) -> ComposeResult:
        yield RowEntry(ResourceType.FOOD, self.game_state.get_status(ResourceType.FOOD)).data_bind(
            ResourcesColumn.game_state
        )
        yield RowEntry(ResourceType.STICKS, self.game_state.get_status(ResourceType.STICKS)).data_bind(
            ResourcesColumn.game_state
        )

    def watch_game_state(self, game_state: GameState) -> None:
        self.game_state = game_state


class ColumnsContainer(HorizontalScroll):
    game_state: reactive[GameState] = reactive(GameState())

    def compose(self) -> ComposeResult:
        yield ResourcesColumn().data_bind(ColumnsContainer.game_state)
        yield ProducersColumn().data_bind(ColumnsContainer.game_state)
        yield UpgradesColumn().data_bind(ColumnsContainer.game_state)

    def watch_game_state(self, game_state: GameState) -> None:
        self.game_state = game_state
