# =====================================================
# PROYECTO SUNBURST - SOLARWINDS
# Rol 1: Diseñador de Datos
# Generación de datos sintéticos
# =====================================================

# =========================
# IMPORTACIÓN DE LIBRERÍAS
# =========================

import pandas as pd
import numpy as np
from faker import Faker
import random

# =========================
# CONFIGURACIÓN INICIAL
# =========================

fake = Faker()

random.seed(42)
np.random.seed(42)

# =========================================
# FUNCIÓN PARA GENERAR CLIENTES
# =========================================

def generar_cliente(cliente_id):

    tipos_org = [
        "Gobierno",
        "Empresa Privada",
        "Proveedor TI",
        "Entidad Financiera",
        "Universidad"
    ]

    sectores = [
        "Tecnología",
        "Finanzas",
        "Salud",
        "Educación",
        "Defensa",
        "Telecomunicaciones"
    ]

    criticidades = [
        "Alta",
        "Media",
        "Baja"
    ]

    return {

        "cliente_id": cliente_id,

        "nombre_organizacion": fake.company(),

        "tipo_org": random.choice(tipos_org),

        "pais": fake.country(),

        "sector": random.choice(sectores),

        "criticidad": random.choice(criticidades)
    }

# =========================================
# GENERAR DATAFRAME CLIENTES
# =========================================

clientes_lista = []

for i in range(1, 51):

    clientes_lista.append(
        generar_cliente(i)
    )

clientes = pd.DataFrame(clientes_lista)

print("\n===== DATAFRAME CLIENTES =====")
print(clientes.head())
# =========================================
# FUNCIÓN VERSIONES SOFTWARE
# =========================================

def generar_versiones():

    return [

        {
            "version_id": 1,
            "nombre_version": "Orion 2019.4",
            "fecha_release": "2019-06-10",
            "contiene_sunburst": True,
            "fecha_compilacion": "2019-09-12"
        },

        {
            "version_id": 2,
            "nombre_version": "Orion 2019.4 HF1",
            "fecha_release": "2019-08-15",
            "contiene_sunburst": True,
            "fecha_compilacion": "2019-11-04"
        },

        {
            "version_id": 3,
            "nombre_version": "Orion 2019.4 HF5",
            "fecha_release": "2020-03-26",
            "contiene_sunburst": False,
            "fecha_compilacion": "2020-03-20"
        },

        {
            "version_id": 4,
            "nombre_version": "Orion 2020.2",
            "fecha_release": "2020-05-20",
            "contiene_sunburst": True,
            "fecha_compilacion": "2020-02-20"
        },

        {
            "version_id": 5,
            "nombre_version": "Orion 2020.2 HF1",
            "fecha_release": "2020-06-15",
            "contiene_sunburst": True,
            "fecha_compilacion": "2020-04-15"
        },

        {
            "version_id": 6,
            "nombre_version": "Orion 2020.2.1",
            "fecha_release": "2020-12-15",
            "contiene_sunburst": False,
            "fecha_compilacion": "2020-12-10"
        },

        {
            "version_id": 7,
            "nombre_version": "Orion 2021.1",
            "fecha_release": "2021-02-10",
            "contiene_sunburst": False,
            "fecha_compilacion": "2021-01-28"
        },

        {
            "version_id": 8,
            "nombre_version": "Orion 2022.1",
            "fecha_release": "2022-04-12",
            "contiene_sunburst": False,
            "fecha_compilacion": "2022-03-30"
        }
    ]

# =========================================
# GENERAR DATAFRAME VERSIONES SOFTWARE
# =========================================

versiones_software = pd.DataFrame(
    generar_versiones()
)

print("\n===== DATAFRAME VERSIONES SOFTWARE =====")
print(versiones_software.head())

# =========================================
# FUNCIÓN PARA GENERAR INSTALACIONES
# =========================================

def generar_instalacion(instalacion_id):

    niveles_datos = [
        "Alto",
        "Medio",
        "Bajo"
    ]

    return {

        "instalacion_id": instalacion_id,

        "cliente_id": random.randint(1, 50),

        "version_id": random.randint(1, 8),

        "fecha_instalacion": fake.date_between(
            start_date='-3y',
            end_date='today'
        ),

        "nivel_datos_sensibles": random.choice(
            niveles_datos
        )
    }

# =========================================
# GENERAR DATAFRAME INSTALACIONES
# =========================================

instalaciones_lista = []

for i in range(1, 101):

    instalaciones_lista.append(
        generar_instalacion(i)
    )

instalaciones = pd.DataFrame(
    instalaciones_lista
)

print("\n===== DATAFRAME INSTALACIONES =====")
print(instalaciones.head())

# =========================================
# EXPORTAR DATAFRAMES A CSV
# =========================================

import os

# Ruta de la carpeta donde está el script
ruta_actual = os.path.dirname(os.path.abspath(__file__))

# Exportar archivos CSV
clientes.to_csv(
    os.path.join(ruta_actual, "clientes.csv"),
    index=False
)

versiones_software.to_csv(
    os.path.join(ruta_actual, "versiones_software.csv"),
    index=False
)

instalaciones.to_csv(
    os.path.join(ruta_actual, "instalaciones.csv"),
    index=False
)

print("\nArchivos CSV generados correctamente.")