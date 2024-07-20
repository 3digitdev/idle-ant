from time import monotonic

from textual.timer import Timer
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.reactive import reactive, ReactiveType
from textual.widgets import Header, Footer, Static, Button


class TimeDisplay(Static):
    start_time: ReactiveType = reactive(monotonic)
    time: ReactiveType = reactive(0.0)
    total: ReactiveType = reactive(0.0)
    update_timer: Timer | None = None

    # Called when the widget is first added to the application
    def on_mount(self) -> None:
        # set_interval calls a given function at a specific interval
        # 'interval' param is in SECONDS.
        self.update_timer = self.set_interval(interval=(1 / 60), callback=self.update_time, pause=True)

    def update_time(self) -> None:
        self.time = self.total + (monotonic() - self.start_time)

    # Functions starting with watch_<reactive_variable>
    # will be called anytime that variable is modified
    # These are called "watch methods"
    def watch_time(self, time: float) -> None:
        min, sec = divmod(time, 60)
        hr, min = divmod(min, 60)
        self.update(f'{hr:02,.0f}:{min:02,.0f}:{sec:05,.2f}')

    def start(self) -> None:
        """Button trigger to start/resume a timer"""
        self.start_time = monotonic()
        self.update_timer.resume()

    def stop(self) -> None:
        """Button trigger to pause/stop a timer"""
        self.update_timer.pause()
        self.total += monotonic() - self.start_time
        self.time = self.total

    def reset(self) -> None:
        self.total = 0.0
        self.time = 0.0


class Stopwatch(Static):
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        time_display: TimeDisplay = self.query_one(TimeDisplay)
        match event.button.id:
            case 'start':
                time_display.start()
                self.add_class('started')
            case 'stop':
                time_display.stop()
                self.remove_class('started')
            case 'reset':
                time_display.reset()
            case _:
                pass

    def compose(self) -> ComposeResult:
        yield Button('Start', id='start', variant='success')
        yield Button('Stop', id='stop', variant='error')
        yield Button('Reset', id='reset')
        yield TimeDisplay()


class StopwatchApp(App):
    CSS_PATH = 'stopwatch.tcss'
    BINDINGS = [
        ('q', 'quit', 'Quit'),
        ('d', 'toggle_dark', 'Toggle Dark Mode'),
        ('a', 'add_stopwatch', 'Add Stopwatch'),
        ('r', 'remove_stopwatch', 'Remove Stopwatch'),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield ScrollableContainer(Stopwatch(), Stopwatch(), id='timers')
        yield Footer()

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

    def action_add_stopwatch(self) -> None:
        sw = Stopwatch()
        self.query_one('#timers').mount(sw)
        sw.scroll_visible()

    def action_remove_stopwatch(self) -> None:
        timers = self.query('Stopwatch')
        if timers:
            timers.last().remove()


if __name__ == '__main__':
    app = StopwatchApp()
    app.run()
