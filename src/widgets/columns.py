from textual.app import ComposeResult
from textual.reactive import reactive
from textual.containers import ScrollableContainer

from game.producer import Producer
from game.resource import Resource
from game.upgrade import Upgrade
from shared import ResourceType, ProducerType, UpgradeType, abbrev_num
from game import GameState
from widgets.rows import ResourceRow, ProducerRow, UpgradeRow


type T = ProducerType | UpgradeType
type U = Producer | Upgrade


def build_cost_subtitle(record: dict[T, U], resources: dict[ResourceType, Resource], key: T) -> str:
    out = []
    for resource, cost in record[key].cost.items():
        if resources[resource].total < cost:
            out.append(f'[red]{abbrev_num(cost)} {resource}[/red]')
        else:
            out.append(f'[green]{abbrev_num(cost)} {resource}[/green]')
    return f'{" | ".join(out)}'


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
            row.border_title = f'[b cyan]{producer}[/] ({self.game_state.producers[producer].total})'
            row.border_subtitle = build_cost_subtitle(self.game_state.producers, self.game_state.resources, producer)
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
            # TODO: Add back parenthetical total here...?
            row.border_title = f'[b]{upgrade}[/b]'
            row.border_subtitle = build_cost_subtitle(self.game_state.upgrades, self.game_state.resources, upgrade)
            yield row
