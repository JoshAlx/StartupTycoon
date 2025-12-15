import sqlite3


class PayrollProcessor:
    def __init__(self, db_manager):
        self.db = db_manager

    def calcular_nomina_mensual(self, periodo):
        """
        Simula un Stored Procedure complejo.
        Realiza cálculos masivos, aplica lógica de juego (Bonos/Castigos)
        y guarda todo atómicamente.
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()

        try:
            conn.execute("BEGIN TRANSACTION")  # Inicio de transacción manual

            # 1. Obtener empleados activos
            cursor.execute("SELECT * FROM empleados WHERE estado='ACTIVO'")
            empleados = cursor.fetchall()

            total_nomina = 0
            total_deducciones_mes = 0

            # Crear cabecera de nómina
            cursor.execute("INSERT INTO nomina_historial (periodo) VALUES (?)", (periodo,))
            nomina_id = cursor.lastrowid

            # 2. Iterar y procesar lógica compleja (El "Cerebro" del SP)
            for emp in empleados:
                emp_id, nombre, rol, email, base, nivel, xp, _, _ = emp

                # --- LÓGICA DE JUEGO ---
                # Bono por nivel (5% por nivel)
                bono_nivel = base * (0.05 * (nivel - 1))

                # Deducción "Impuesto Tecnológico" (Simulado 12%)
                impuesto = (base + bono_nivel) * 0.12

                # Evento Aleatorio: Multa por romper producción (1% probabilidad)
                multa_bug = 500 if (id % 7 == 0) else 0

                neto = (base + bono_nivel) - (impuesto + multa_bug)

                # Insertar detalle
                cursor.execute("""
                               INSERT INTO detalles_nomina
                               (nomina_id, empleado_id, salario_bruto, bono_rendimiento, deduccion_impuestos,
                                deduccion_falla_servidor, neto_pagado)
                               VALUES (?, ?, ?, ?, ?, ?, ?)
                               """, (nomina_id, emp_id, base, bono_nivel, impuesto, multa_bug, neto))

                total_nomina += neto
                total_deducciones_mes += (impuesto + multa_bug)

            # 3. Actualizar totales en cabecera
            cursor.execute("""
                           UPDATE nomina_historial
                           SET total_pagado      = ?,
                               total_deducciones = ?
                           WHERE id = ?
                           """, (total_nomina, total_deducciones_mes, nomina_id))

            conn.commit()  # ¡ÉXITO! Se guardan los cambios
            return {"status": "success", "total": total_nomina, "msg": "Nómina procesada exitosamente."}

        except Exception as e:
            conn.rollback()  # ¡ERROR! Se deshace todo para evitar corrupción de datos
            return {"status": "error", "msg": str(e)}
        finally:
            conn.close()