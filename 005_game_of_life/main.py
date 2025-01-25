#!/usr/bin/env python3
"""The Game of Life implemented with nicegui

A remake of : https://halimb.github.io/gol/
"""
from typing import Optional

from nicegui import ui
from nicegui.events import Handler, ClickEventArguments, GenericEventArguments


class GameOfLife(ui.element):
    def __init__(self):
        self._speed: float = 1.
        self._playing: bool = False
        self._generation_num: int = 0

    def ui_init(self):
        super().__init__("div")

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = min(4., max(0.25, float(value)))

    def decrease_speed(self, *args, **kwarg):
        self.speed /= 2

    def increase_speed(self, *args, **kwarg):
        self.speed *= 2

    @property
    def playing(self):
        return self._playing

    @playing.setter
    def playing(self, value: bool):
        self._playing = value

    def play(self):
        self.playing = True

    def pause(self):
        self.playing = False

    def toggle_play(self, *args, **kwarg):
        self.playing = not self.playing

    def on_container_resize(self, event: GenericEventArguments):
        if "width" in event.args and "height" in event.args:
            self.build(**event.args)

    @property
    def generation_num(self):
        return self._generation_num

    def generate(self, *args, **kwarg):
        self._generation_num += 1
        print("generation", self.generation_num)
        pass

    def build(self, width: int = 100, height: int = 100) -> None:
        # Clear all children
        self.clear()
        with self:
            ui.label(f"Build {width}x{height}")


def custom_icon(
        name: str,
        on_click: Optional[Handler[ClickEventArguments]] = None,
        color="gray-500",
        size="sm",
        *args, **kwargs
):
    return ui.button(icon=f"{name}", on_click=on_click, color=color, *args, **kwargs) \
        .props(f'padding="{size}" size="{size}"') \
        .classes("text-white")


@ui.page('/')
def home():
    # Init Game engine
    gol = GameOfLife()

    # Add icons CSS
    ui.add_head_html(
        '<link href="https://cdn.jsdelivr.net/themify-icons/0.1.2/css/themify-icons.css" rel="stylesheet" />'
    )

    # Remove padding of the nicegui-content element
    ui.query(".nicegui-content").classes("p-0")
    ui.add_head_html('''
        <script>
        function emitContainerSizeEvent() {
            container = document.getElementById("c2")
            emitEvent('container_resize', {
                width: container.offsetWidth,
                height: container.offsetHeight,
            });
        }
        window.onresize = emitContainerSizeEvent;
        </script>
    ''')

    # Add event listeners
    ui.on('container_resize', gol.on_container_resize)

    # Build main theme
    ui.colors(primary="white")

    # --------------------------------------- #
    # ============ Build UI ================= #
    # --------------------------------------- #

    # ============= Header  ================= #
    with ui.header().classes(
            replace='text-black bg-white flex items-center px-2 shadow-2'
    ):
        ui.label("Conway’s Game of Life").classes('font-bold text-2xl')
        ui.space()
        with ui.tabs().props("inline-label") as tabs:
            ui.tab('Board', icon="apps")
            ui.tab('Lexicon', icon="menu_book")
            ui.tab('Help', icon="info")

    # ======== Footer / Controls ============ #
    with ui.footer().classes(
            "bg-white text-black flex items-center px-4 shadow-2"
    ):
        with ui.row().classes("items-center"):
            custom_icon("ti-star")
            ui.label('Generation : 0').bind_text_from(
                gol,
                target_name="generation_num",
                backward=lambda value: f"Generation : {value}"
            )
        ui.space()
        with ui.row().classes("items-center"):
            custom_icon("ti-control-shuffle")
            custom_icon("ti-trash").classes("q-mr-xl")
            custom_icon("ti-control-play", on_click=gol.toggle_play).bind_icon_from(
                gol,
                target_name="playing",
                backward=lambda value: "ti-control-play" if value else "ti-control-pause"
            )
            custom_icon("ti-control-skip-forward", on_click=lambda value: (gol.pause(), gol.generate())) \
                .classes("q-mr-xl")
            custom_icon("ti-pencil")
            custom_icon("ti-eraser")
        ui.space()
        with ui.row().classes("items-center"):
            custom_icon("ti-minus", size="xs", on_click=gol.decrease_speed)
            ui.label('Speed : 1x').bind_text_from(
                gol,
                target_name="speed",
                backward=lambda value: f"Speed : {value}x"
            )
            custom_icon("ti-plus", size="xs", on_click=gol.increase_speed)

    # ================ Tabs ================= #
    with ui.tab_panels(tabs, value='Board'):
        with ui.tab_panel('Board'):
            gol.ui_init()
        with ui.tab_panel('Lexicon'):
            ui.label('Lexicon')
        with ui.tab_panel('Help'):
            ui.label('Help')

    # Emit container size event
    ui.run_javascript("emitContainerSizeEvent()")


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(port=49374)
