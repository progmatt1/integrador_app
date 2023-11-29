from flet_route import path
from views.inicio import inicio

app_routes = [
    path(url="/", view=inicio, clear=True),
]