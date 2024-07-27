from textual.app import ComposeResult
from textual.containers import HorizontalScroll
from textual.reactive import reactive
from textual.widgets import Button, Static
from shared import ResourceType, ProducerType, UpgradeType
from game import GameState
from widgets import ResourcesColumn, ProducersColumn, UpgradesColumn


class GameContainer(Static):
    # Disabling recompose here causes it to stop updating after the first button press...
    game_state: reactive[GameState] = reactive(GameState(), recompose=True)

    def on_mount(self) -> None:
        self.set_interval(interval=1, callback=self.tick)

    def compose(self) -> ComposeResult:
        yield HorizontalScroll(
            ResourcesColumn().data_bind(GameContainer.game_state),
            ProducersColumn().data_bind(GameContainer.game_state),
            UpgradesColumn().data_bind(GameContainer.game_state),
        )

    def tick(self) -> None:
        self.game_state.tick()
        self.mutate_reactive(GameContainer.game_state)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Event handler called when a button is pressed.

        HISTORICAL NOTE:  These cases were once put into their respective
        child widgets.  When I did that, the game would "freeze" the button pressed until
        the next game tick happened for some reason.  Didn't investigate much.

        IF you have a lot of spare time later, feel free to do a deeper dive.  Until then,
        they will remain here...
        """
        match event.button.id.split('-'):
            case ['gather']:
                self.game_state.resources[ResourceType.FOOD].total += int(
                    1 * self.game_state.DEBUG_MULTIPLIER * self.game_state.click_modifier
                )
                self.mutate_reactive(GameContainer.game_state)
            case [*obj_type, num] if ' '.join(obj_type) in ProducerType:
                obj_type = ' '.join(obj_type)
                self.game_state.purchase_producer(ProducerType(obj_type), int(num))
                self.mutate_reactive(GameContainer.game_state)
            case [*obj_type, 'upgrade'] if ' '.join(obj_type) in UpgradeType:
                obj_type = ' '.join(obj_type)
                self.game_state.purchase_upgrade(UpgradeType(obj_type))
                self.mutate_reactive(GameContainer.game_state)
            case _:
                pass
