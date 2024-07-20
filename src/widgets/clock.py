from time import monotonic

from textual.timer import Timer
from textual.reactive import reactive
from textual.widgets import Static


class GameClock(Static):
    start_time: reactive[float] = reactive(monotonic())
    time: reactive[float] = reactive(0.0)
    update_timer: Timer | None = None

    def on_mount(self) -> None:
        self.update_timer = self.set_interval(interval=1, callback=self.update_time)

    def update_time(self) -> None:
        self.time = monotonic() - self.start_time

    def watch_time(self, time: float) -> None:
        min, sec = divmod(time, 60)
        hr, min = divmod(min, 60)
        d, hr = divmod(hr, 24)
        wk, d = divmod(d, 7)
        mt, wk = divmod(wk, 4)
        yr, mt = divmod(mt, 12)
        result = 'Elapsed Time: '
        if yr:
            result += f'{yr:,.0f}y, '
        if mt:
            result += f'{mt:,.0f}m, '
        if wk:
            result += f'{wk:,.0f}w, '
        if d:
            result += f'{d:,.0f}d, '
        result += f'{hr:02,.0f}:{min:02,.0f}:{sec:02.0f}'
        self.update(result)
