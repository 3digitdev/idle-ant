from textual.app import ComposeResult
from textual.reactive import reactive
from textual.containers import ScrollableContainer
from shared import ResourceType, ProducerType, UpgradeType
from game import GameState
from widgets.rows import ResourceRow, ProducerRow, UpgradeRow


class ResourcesColumn(ScrollableContainer):
    BORDER_TITLE = '[b]Resources[/b]'
    DEFAULT_CLASSES = 'display-column'

    game_state: reactive[GameState] = reactive(GameState())

    def compose(self) -> ComposeResult:
        for resource in ResourceType:
            yield ResourceRow(ResourceType(resource), self.game_state.get_status(resource)).data_bind(
                ResourcesColumn.game_state
            )


class ProducersColumn(ScrollableContainer):
    BORDER_TITLE = '[b]Producers[/b]'
    DEFAULT_CLASSES = 'display-column'

    game_state: reactive[GameState] = reactive(GameState())

    def compose(self) -> ComposeResult:
        for producer in ProducerType:
            row = ProducerRow(
                key_type=ProducerType(producer),
                status=self.game_state.get_status(producer),
                gather_rates=self.game_state.gather_rates(producer),
            ).data_bind(ProducersColumn.game_state)
            row.border_title = f'[b]{producer}[/b] ({self.game_state.producers[producer].total})'
            row.border_subtitle = '[b]Cost:[/b] ' + ' | '.join(
                [f'{c} {r}' for r, c in self.game_state.producers[producer].cost.items()]
            )
            yield row


class UpgradesColumn(ScrollableContainer):
    BORDER_TITLE = '[b]Upgrades[/b]'
    DEFAULT_CLASSES = 'display-column'

    game_state: reactive[GameState] = reactive(GameState())

    def compose(self) -> ComposeResult:
        for upgrade in UpgradeType:
            row = UpgradeRow(
                key_type=UpgradeType(upgrade),
                status=self.game_state.get_status(upgrade),
                upgrade_text=self.game_state.upgrades[upgrade].info,
            ).data_bind(UpgradesColumn.game_state)
            row.border_title = f'[b]{upgrade}[/b] ({self.game_state.upgrades[upgrade].total})'
            row.border_subtitle = '[b]Cost:[/b] ' + ' | '.join(
                [f'{c} {r}' for r, c in self.game_state.upgrades[upgrade].cost.items()]
            )
            yield row
