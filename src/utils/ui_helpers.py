import flet as ft


def show_gamified_message(page: ft.Page, message: str, msg_type: str = "success"):
    """
    Muestra un SnackBar estilizado según el contexto del juego.
    """
    if msg_type == "success":
        color = ft.Colors.GREEN_700
        icon = ft.Icons.MONETIZATION_ON
    else:
        color = ft.Colors.RED_700
        icon = ft.Icons.WARNING_AMBER

    snack = ft.SnackBar(
        content=ft.Row([
            ft.Icon(icon, color=ft.Colors.WHITE),
            ft.Text(message, color=ft.Colors.WHITE, weight="bold")
        ]),
        bgcolor=color,
        action="OK",
    )
    page.snack_bar = snack
    snack.open = True
    page.update()