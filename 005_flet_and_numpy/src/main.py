import flet as ft
import numpy as np


def main(page: ft.Page):
    counter = ft.Text("0", size=50, data=0)

    def random_click(e):
        counter.data = np.random.randint(100, size=5)
        counter.value = str(counter.data)
        counter.update()

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.SHUFFLE, on_click=random_click
    )
    page.add(
        ft.SafeArea(
            ft.Container(
                counter,
                alignment=ft.alignment.center,
            ),
            expand=True,
        )
    )


ft.app(main)
