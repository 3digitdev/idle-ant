from textual.app import ComposeResult
from textual.reactive import reactive
from textual.containers import ScrollableContainer, HorizontalScroll
from constants import ResourceType, ProducerType
from game import GameState
from widgets.containers import RowEntry


class ProducersColumn(ScrollableContainer):
    game_state: reactive[GameState] = reactive(GameState())

    def on_mount(self) -> None:
        self.border_title = 'Producers'
        self.classes = ['display-column']

    def compose(self) -> ComposeResult:
        yield RowEntry(ProducerType.WORKER).data_bind(ProducersColumn.game_state)

    def watch_game_state(self, game_state: GameState) -> None:
        self.game_state = game_state


class ResourcesColumn(ScrollableContainer):
    game_state: reactive[GameState] = reactive(GameState())

    def on_mount(self) -> None:
        self.border_title = 'Resources'
        self.classes = ['display-column']

    def compose(self) -> ComposeResult:
        yield RowEntry(ResourceType.FOOD).data_bind(ResourcesColumn.game_state)

    def watch_game_state(self, game_state: GameState) -> None:
        self.game_state = game_state


class ColumnsContainer(HorizontalScroll):
    game_state: reactive[GameState] = reactive(GameState())

    def compose(self) -> ComposeResult:
        yield ResourcesColumn().data_bind(ColumnsContainer.game_state)
        yield ProducersColumn().data_bind(ColumnsContainer.game_state)

    def watch_game_state(self, game_state: GameState) -> None:
        self.game_state = game_state
