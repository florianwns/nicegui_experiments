#!/usr/bin/env python3
"""The Game of Life implemented with nicegui

A remake of : https://playgameoflife.com/
"""

from nicegui import ui


class GameOfLife:
    def __init__(self):
        ui.label('This page is defined in a class.')


@ui.page('/')
def game_of_life_page():
    with ui.header().classes(replace='flex items-center px-2') as header:
        ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat color=white')
        ui.space()
        ui.label("Conway’s Game of Life").classes('font-bold text-2xl')
        ui.space()
        with ui.tabs().props("inline-label") as tabs:
            ui.tab('Board', icon="apps")
            ui.tab('Lexicon', icon="menu_book")
            ui.tab('Help', icon="info")

    with ui.footer(value=False) as footer:
        ui.label('Footer')

    with ui.left_drawer().classes('bg-gray-50') as left_drawer:
        ui.label('Side menu')

    with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
        ui.button(on_click=footer.toggle, icon='contact_support').props('fab')

    with ui.tab_panels(tabs, value='Board').classes('w-full'):
        with ui.tab_panel('Board'):
            gol = GameOfLife()
        with ui.tab_panel('Lexicon'):
            ui.label('Lexicon')
        with ui.tab_panel('Help'):
            ui.label('Help')


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(port=49374)
