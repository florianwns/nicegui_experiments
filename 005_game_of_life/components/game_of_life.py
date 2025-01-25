from nicegui import ui


class GameOfLife(ui.element, component="game_of_life.js"):
    def __init__(self):
        # A 'Game Of Life' canvas
        super().__init__()
        self._props['speed']: float = 1.0
        self._props['playing']: bool = False
        self._props['generation_num']: int = 0
        self._props['drawing']: str = "draw"

    @property
    def speed(self):
        return self._props['speed']

    @speed.setter
    def speed(self, value):
        self._props['speed'] = min(4., max(0.25, float(value)))

    def decrease_speed(self, *args, **kwarg):
        self.speed /= 2

    def increase_speed(self, *args, **kwarg):
        self.speed *= 2

    @property
    def playing(self):
        return self._props['playing']

    @playing.setter
    def playing(self, value: bool):
        self._props['playing'] = value

    def play(self):
        self.playing = True

    def pause(self):
        self.playing = False

    def toggle_play(self, *args, **kwarg):
        self.playing = not self.playing

    @property
    def generation_num(self):
        return self._props['generation_num']

    def generate(self, *args, **kwarg):
        self._props['generation_num'] += 1
