import flet as ft
from src.utils.styles import GameColors, card_style, title_style
from src.utils.ui_helpers import show_gamified_message


class EmployeeListCard(ft.Container):
    def __init__(self, emp_data, on_delete):
        # CORRECCIÓN: Desempaquetamos estilo
        super().__init__(**card_style())

        id, nombre, rol, nivel, salario = emp_data
        self.padding = 15
        self.margin = ft.margin.only(bottom=10)

        avatar = ft.CircleAvatar(
            content=ft.Text(nombre[:2].upper()),
            bgcolor=GameColors.ACCENT,
            color=GameColors.BG_DARK
        )

        self.content = ft.Row([
            avatar,
            ft.Column([
                ft.Text(nombre, weight="bold", color=GameColors.TEXT_MAIN),
                ft.Text(f"{rol} | Lvl {nivel}", size=12, color=GameColors.TEXT_SEC),
            ], expand=True),
            ft.Column([
                ft.Text(f"${salario / 1000:.1f}k", weight="bold", color=GameColors.MONEY),
                ft.IconButton(
                    icon=ft.Icons.DELETE_SWEEP,
                    icon_color=GameColors.ERROR,
                    icon_size=20,
                    on_click=lambda e: on_delete(id)
                )
            ])
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)


class HRView(ft.Column):
    def __init__(self, page, db_manager):
        super().__init__()
        self.page = page
        self.db = db_manager
        self.expand = True

        self.employees_list = ft.ListView(expand=True, spacing=10, padding=10)

        self.fab = ft.FloatingActionButton(
            icon=ft.Icons.PERSON_ADD,
            bgcolor=GameColors.ACCENT,
            on_click=self.open_hire_modal
        )

        self.controls = [
            ft.Container(
                content=ft.Text("Plantilla Activa", style=title_style()),
                padding=ft.padding.only(left=10, top=10)
            ),
            self.employees_list
        ]

    def did_mount(self):
        self.page.floating_action_button = self.fab
        self.load_employees()
        self.page.update()

    def will_unmount(self):
        self.page.floating_action_button = None
        self.page.update()

    def load_employees(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, rol, nivel, salario_base FROM empleados WHERE estado='ACTIVO'")
        rows = cursor.fetchall()
        conn.close()

        self.employees_list.controls.clear()
        for row in rows:
            self.employees_list.controls.append(
                EmployeeListCard(row, self.fire_employee)
            )
        self.update()

    def open_hire_modal(self, e):
        name_field = ft.TextField(label="Nombre", border_color=GameColors.ACCENT)
        role_field = ft.Dropdown(
            label="Rol",
            options=[ft.dropdown.Option("Dev"), ft.dropdown.Option("Designer")],
            border_color=GameColors.ACCENT
        )

        def hire_action(e):
            show_gamified_message(self.page, "Contratado (Simulado)", "success")
            bs.open = False
            bs.update()
            self.load_employees()

        bs = ft.BottomSheet(
            ft.Container(
                padding=20,
                bgcolor=GameColors.BG_CARD,
                height=300,
                content=ft.Column([
                    ft.Text("Reclutar Talento", size=20, weight="bold"),
                    name_field,
                    role_field,
                    ft.ElevatedButton("Firmar Contrato", width=300, bgcolor=GameColors.MONEY, color="black",
                                      on_click=hire_action)
                ], spacing=15)
            )
        )
        self.page.overlay.append(bs)
        bs.open = True
        self.page.update()

    def fire_employee(self, id):
        show_gamified_message(self.page, "¡Estás despedido!", "error")