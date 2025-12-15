from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os


def generate_payroll_report(filename, payroll_data):
    """
    Genera un PDF con el resumen de la nómina para la 'Auditoría'.
    payroll_data: Diccionario con total_pagado, fecha, lista de empleados.
    """
    try:
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter

        # Encabezado "Oficial"
        c.setFont("Helvetica-Bold", 20)
        c.drawString(50, height - 50, "Startup Tycoon - Reporte de Auditoría")

        c.setFont("Helvetica", 12)
        c.drawString(50, height - 80, f"Periodo Auditado: {payroll_data['periodo']}")
        c.drawString(50, height - 100, f"Total Egresos: ${payroll_data['total']:,.2f}")

        # Línea divisoria
        c.line(50, height - 110, width - 50, height - 110)

        # Cuerpo del reporte
        y = height - 140
        c.drawString(50, y, "Detalle de Transacciones Aprobadas:")
        y -= 20

        c.setFont("Courier", 10)
        for emp in payroll_data['detalles']:
            # Formato: Nombre - Neto Pagado
            line = f"{emp['nombre']:<30} | Rol: {emp['rol']:<15} | Pago Neto: ${emp['neto']:,.2f}"
            c.drawString(50, y, line)
            y -= 15

            if y < 50:  # Nueva página si se acaba el espacio
                c.showPage()
                y = height - 50

        c.save()
        return True, f"Reporte guardado en {os.path.abspath(filename)}"
    except Exception as e:
        return False, str(e)