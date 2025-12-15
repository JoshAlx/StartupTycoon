import flet as ft


class EmployeeCard(ft.Container):
    def __init__(self, emp_data, on_fire_click):
        super().__init__()
        self.emp_data = emp_data  # Tupla (id, nombre, rol, email, salario...)
        self.on_fire_click = on_fire_click

        # Diseño visual
        self.padding = 15
        self.border_radius = 10
        self.bgcolor = ft.colors.SURFACE_VARIANT
        self.width = 280

        # Tooltip para ayuda (Requisito UX)
        self.tooltip = f"Nivel {emp_data[5]} - {emp_data[2]}"

        self.content = self._build_content()

    def _build_content(self):
        nombre = self.emp_data[1]
        rol = self.emp_data[2]
        salario = f"${self.emp_data[4]:,.2f}"

        return ft.Column([
            ft.Row([
                ft.Icon(ft.icons.PERSON_ROUNDED, size=40, color=ft.colors.PRIMARY),
                ft.Column([
                    ft.Text(nombre, weight="bold", size=16),
                    ft.Text(rol, size=12, color=ft.colors.ON_SURFACE_VARIANT),
                ], spacing=2)
            ]),
            ft.Divider(),
            ft.Row([
                ft.Text("Salario Base:", size=12),
                ft.Text(salario, weight="bold", size=12, color=ft.colors.GREEN),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

            # Botón de acción con Tooltip
            ft.ElevatedButton(
                "Despedir",
                icon=ft.icons.OUTPUT,
                color=ft.colors.ERROR,
                on_click=lambda e: self.on_fire_click(self.emp_data[0]),
                tooltip="ADVERTENCIA: Despedir reduce la moral de la empresa."
            )
        ])