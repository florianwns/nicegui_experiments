from pathlib import Path

from nicegui import ui


class GameOfLife(
    ui.element,
    component="game_of_life.js",
):
    def __init__(self):
        # A 'Game Of Life' canvas
        super().__init__()
        self.add_resource(Path(__file__).parent.parent / 'libs')
        self._props['speed']: float = 1.0
        self._props['playing']: bool = False
        self._props['drawing']: str = "draw"

        # Add event listener
        self.generation_num = 0
        ui.on('gol__generation_num', lambda e: setattr(self, "generation_num", e.args))

    @property
    def speed(self):
        return self._props['speed']

    @speed.setter
    def speed(self, value):
        self._props['speed'] = min(4., max(0.25, float(value)))
        self.update()

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
        self.update()

    def toggle_play(self, *args, **kwarg):
        self.playing = not self.playing
