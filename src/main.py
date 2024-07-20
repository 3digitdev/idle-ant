from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer
from widgets.containers import GameContainer
from widgets.clock import GameClock


class IdleApp(App):
    CSS_PATH = 'idle.tcss'
    BINDINGS = [
        ('q', 'quit', 'Quit'),
    ]

    def on_mount(self) -> None:
        self.title = 'Antics'

    def compose(self) -> ComposeResult:
        yield Header()
        yield GameContainer(id='game_container')
        yield Container(GameClock(), id='clock_container')
        yield Footer()


if __name__ == '__main__':
    app = IdleApp()
    app.run()
