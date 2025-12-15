import sqlite3
import random
import os
from datetime import datetime


class DatabaseManager:
    def __init__(self, db_name="data/game.db"):
        self.db_name = db_name
        self._ensure_directory_exists()  # <--- Nueva validación de infraestructura
        self.init_db()

    def _ensure_directory_exists(self):
        """
        Verifica si el directorio 'data/' existe.
        Si no, lo crea para evitar el error 'unable to open database file'.
        """
        directory = os.path.dirname(self.db_name)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Directorio '{directory}' creado automáticamente.")

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        """Inicializa las tablas y ejecuta Seed Data si es necesario."""
        query_empleados = """
                          CREATE TABLE IF NOT EXISTS empleados \
                          ( \
                              id \
                              INTEGER \
                              PRIMARY \
                              KEY \
                              AUTOINCREMENT, \
                              nombre \
                              TEXT \
                              NOT \
                              NULL, \
                              rol \
                              TEXT \
                              NOT \
                              NULL, \
                              email \
                              TEXT \
                              UNIQUE, \
                              salario_base \
                              REAL, \
                              nivel \
                              INTEGER \
                              DEFAULT \
                              1, \
                              xp \
                              INTEGER \
                              DEFAULT \
                              0, \
                              fecha_contratacion \
                              TEXT, \
                              estado \
                              TEXT \
                              DEFAULT \
                              'ACTIVO'
                          ); \
                          """

        # Tablas adicionales necesarias para que no falle el resto del sistema
        query_nomina = """
                       CREATE TABLE IF NOT EXISTS nomina_historial \
                       ( \
                           id \
                           INTEGER \
                           PRIMARY \
                           KEY \
                           AUTOINCREMENT, \
                           periodo \
                           TEXT, \
                           total_pagado \
                           REAL, \
                           total_deducciones \
                           REAL, \
                           fecha_proceso \
                           TIMESTAMP \
                           DEFAULT \
                           CURRENT_TIMESTAMP
                       ); \
                       """

        query_detalles = """
                         CREATE TABLE IF NOT EXISTS detalles_nomina \
                         ( \
                             id \
                             INTEGER \
                             PRIMARY \
                             KEY \
                             AUTOINCREMENT, \
                             nomina_id \
                             INTEGER, \
                             empleado_id \
                             INTEGER, \
                             salario_bruto \
                             REAL, \
                             bono_rendimiento \
                             REAL, \
                             deduccion_impuestos \
                             REAL, \
                             deduccion_falla_servidor \
                             REAL, \
                             neto_pagado \
                             REAL
                         ); \
                         """

        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query_empleados)
                cursor.execute(query_nomina)
                cursor.execute(query_detalles)

                # Verificar si está vacía para Seed Data
                cursor.execute("SELECT COUNT(*) FROM empleados")
                if cursor.fetchone()[0] == 0:
                    self.seed_data(cursor)
                conn.commit()
        except Exception as e:
            print(f"Error inicializando DB: {e}")

    def seed_data(self, cursor):
        """Mecanismo de Onboarding: Datos iniciales."""
        roles = ["Backend Dev", "Frontend Dev", "DevOps", "QA Tester", "Product Owner"]
        nombres = ["Alice Code", "Bob Server", "Charlie Bug", "Diana Design", "Eve Hacker"]

        print("🌱 Sembrando datos iniciales para el nuevo juego...")

        for i, nombre in enumerate(nombres):
            rol = roles[i]
            salario = random.randint(2500, 8000)
            email = f"{nombre.split(' ')[0].lower()}@startup.com"
            fecha = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("""
                           INSERT INTO empleados (nombre, rol, email, salario_base, nivel, fecha_contratacion)
                           VALUES (?, ?, ?, ?, ?, ?)
                           """, (nombre, rol, email, salario, 1, fecha))