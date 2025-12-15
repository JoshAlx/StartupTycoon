import flet as ft
from src.utils.styles import GameColors, card_style, title_style  # Ojo: importamos card_style


class StatCard(ft.Container):
    def __init__(self, icon, title, value, color_icon):
        # CORRECCIÓN: Desempaquetamos el estilo aquí
        super().__init__(**card_style())

        self.expand = 1
        self.padding = 15
        self.content = ft.Column([
            ft.Icon(icon, color=color_icon, size=30),
            ft.Text(value, size=20, weight="bold", color=GameColors.TEXT_MAIN),
            ft.Text(title, size=12, color=GameColors.TEXT_SEC)
        ], spacing=5)


class Dashboard(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.expand = True
        self.scroll = ft.ScrollMode.HIDDEN

        self.stats_grid = ft.ResponsiveRow([
            ft.Column([StatCard(ft.Icons.ATTACH_MONEY, "Capital", "$150,000", GameColors.MONEY)], col=6),
            ft.Column([StatCard(ft.Icons.PEOPLE, "Empleados", "12", GameColors.ACCENT)], col=6),
            ft.Column([StatCard(ft.Icons.TRENDING_UP, "Burn Rate", "-$12k/mes", GameColors.ERROR)], col=6),
            ft.Column([StatCard(ft.Icons.BUG_REPORT, "Bugs Activos", "54", ft.Colors.ORANGE)], col=6),
        ], run_spacing=10)

        self.chart_placeholder = ft.Container(
            height=200,
            padding=20,
            **card_style(),  # CORRECCIÓN: Desempaquetamos estilos aquí también
            content=ft.Column([
                ft.Text("Tendencia de Mercado", style=ft.TextStyle(weight="bold", color="white")),
                ft.Container(
                    expand=True,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.bottom_left,
                        end=ft.alignment.top_right,
                        colors=[ft.Colors.with_opacity(0.1, GameColors.ACCENT), GameColors.ACCENT]
                    ),
                    border_radius=10,
                    alignment=ft.alignment.center,
                    content=ft.Text("Gráfico Interactivo", color=ft.Colors.WHITE24)
                )
            ])
        )

        self.actions = ft.Row([
            ft.ElevatedButton("Auditoría", icon=ft.Icons.PIE_CHART, bgcolor=GameColors.BG_CARD, color="white"),
            ft.ElevatedButton("Inversores", icon=ft.Icons.ROCKET_LAUNCH, bgcolor=GameColors.ACCENT, color="black"),
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

        self.controls = [
            ft.Container(height=10),
            ft.Text("Resumen Ejecutivo", style=title_style()),
            ft.Container(height=10),
            self.stats_grid,
            ft.Container(height=20),
            self.chart_placeholder,
            ft.Container(height=20),
            self.actions
        ]