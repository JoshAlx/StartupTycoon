import flet as ft


class GameColors:
    BG_DARK = "#111827"
    BG_CARD = "#1F2937"
    ACCENT = "#00F0FF"
    MONEY = "#00FF9D"
    ERROR = "#FF0055"
    TEXT_MAIN = "#FFFFFF"
    TEXT_SEC = "#9CA3AF"


def title_style():
    return ft.TextStyle(size=22, weight=ft.FontWeight.BOLD, color=GameColors.TEXT_MAIN)


def subtitle_style():
    return ft.TextStyle(size=14, color=GameColors.TEXT_SEC)


# CORRECCIÓN: Ahora devuelve un diccionario de propiedades
def card_style():
    return {
        "bgcolor": GameColors.BG_CARD,
        "border_radius": 15,
        "shadow": ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
        )
    }