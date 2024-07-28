from textual.app import App, ComposeResult
from textual.containers import Container
from textual.events import Key
from textual.widgets import Header, Footer
from widgets import GameContainer
from widgets.clock import GameClock


class IdleApp(App):
    game_container: GameContainer | None = None
    CSS_PATH = 'styles/idle.tcss'
    BINDINGS = [('space', 'space', 'Gather Food'), ('q', 'quit', 'Quit')]
    TITLE = 'Antics'

    def compose(self) -> ComposeResult:
        yield Header()
        self.game_container = GameContainer(id='game_container')
        yield self.game_container
        yield Container(GameClock(), id='clock_container')
        yield Footer()

    def action_space(self):
        pass

    def on_key(self, event: Key) -> None:
        print('main:', event.key)
        self.game_container.key_handler(event)


if __name__ == '__main__':
    app = IdleApp()
    app.run()
