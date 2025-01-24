#!/usr/bin/env python3
"""The Game of Life implemented with nicegui

A remake of : https://halimb.github.io/gol/
"""

from nicegui import ui


class GameOfLife:
    def __init__(self):
        self._speed = 1

    def build(self):
        ui.label('This page is defined in a class.')

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = min(4, max(0.25, value))

    def decrease_speed(self, *args, **kwarg):
        self.speed /= 2

    def increase_speed(self, *args, **kwarg):
        self.speed *= 2


def ti_icon(name: str, color="gray-500", size="sm", *args, **kwargs):
    return ui.button(icon=f"ti-{name}", color=color, *args, **kwargs) \
        .props(f'padding="{size}" size="{size}"') \
        .classes("text-white")


@ui.page('/')
def home():
    gol = GameOfLife()

    ui.add_head_html(
        '<link href="https://cdn.jsdelivr.net/themify-icons/0.1.2/css/themify-icons.css" rel="stylesheet" />'
    )
    ui.colors(primary="white")
    with ui.header().classes(
            replace='text-black bg-white flex items-center px-2 shadow-2'
    ) as header:
        ui.label("Conway’s Game of Life").classes('font-bold text-2xl')
        ui.space()
        with ui.tabs().props("inline-label") as tabs:
            ui.tab('Board', icon="apps")
            ui.tab('Lexicon', icon="menu_book")
            ui.tab('Help', icon="info")

    with ui.footer().classes(
            "bg-white text-black flex items-center px-4 shadow-2"
    ) as footer:
        with ui.row().classes("items-center"):
            ti_icon("star")
            ui.label('Generation : 0')
        ui.space()
        with ui.row().classes("items-center"):
            ti_icon("control-shuffle")
            ti_icon("trash").classes("q-mr-xl")
            ti_icon("control-pause")
            ti_icon("control-play")
            ti_icon("control-skip-forward").classes("q-mr-xl")
            ti_icon("pencil")
            ti_icon("eraser")
        ui.space()
        with ui.row().classes("items-center"):
            ti_icon("minus", size="xs", on_click=gol.decrease_speed)
            ui.label('Speed : 1x').bind_text_from(gol, "speed", lambda value: f"Speed : {value}x")
            ti_icon("plus", size="xs", on_click=gol.increase_speed)

    with (ui.tab_panels(tabs, value='Board').classes('w-full')):
        with ui.tab_panel('Board'):
            gol.build()
        with ui.tab_panel('Lexicon'):
            ui.label('Lexicon')
        with ui.tab_panel('Help'):
            ui.label('Help')


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(port=49374)
