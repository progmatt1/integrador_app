import flet as ft
from flet_route import path
from views.inicio import inicio
from flet_route import Routing

app_routes = [
    path(url="/", view=inicio, clear=True),
]

def main(page:ft.Page):
    page.title="Escuela"

    Routing(app_routes=app_routes, page=page)
    page.go("/")

ft.app(target = main)