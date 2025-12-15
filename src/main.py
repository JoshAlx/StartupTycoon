import flet as ft
from src.models.database import DatabaseManager
from src.views.dashboard import Dashboard
from src.views.hr_view import HRView
from src.utils.styles import GameColors


def main(page: ft.Page):
    # --- Configuración Global Estética ---
    page.title = "Startup Tycoon"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = GameColors.BG_DARK
    page.padding = 0
    # SafeArea es VITAL para móviles (evita el notch de la cámara)
    page.safe_area = ft.SafeArea(ft.Container())

    db_manager = DatabaseManager()

    # Contenedor principal donde cambiaremos las vistas
    body_container = ft.Container(expand=True, padding=10)

    def change_tab(e):
        idx = e.control.selected_index
        body_container.content = None  # Limpiar

        if idx == 0:
            body_container.content = Dashboard(page)
        elif idx == 1:
            body_container.content = HRView(page, db_manager)
        elif idx == 2:
            body_container.content = ft.Container(
                alignment=ft.alignment.center,
                content=ft.Text("Mercado (WIP)", color="white")
            )

        body_container.update()

    # Barra de Navegación Inferior (Estilo App Nativa)
    nav_bar = ft.NavigationBar(
        bgcolor=GameColors.BG_CARD,
        selected_index=0,
        on_change=change_tab,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.DASHBOARD_ROUNDED, label="Oficina"),
            ft.NavigationBarDestination(icon=ft.Icons.PEOPLE_ALT_ROUNDED, label="RRHH"),
            ft.NavigationBarDestination(icon=ft.Icons.MONETIZATION_ON_ROUNDED, label="Finanzas"),
        ]
    )

    page.navigation_bar = nav_bar

    # Cargar vista inicial
    body_container.content = Dashboard(page)
    page.add(body_container)


if __name__ == "__main__":
    ft.app(target=main)