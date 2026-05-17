# 1. IMPORTACIONES
import os
import pandas as pd

# 2. CARGA DE ARCHIVOS 
# Cargar datos generados en el rol 1

# Ruta del archivo actual
ruta_actual = os.path.dirname(os.path.abspath(__file__))

clientes = pd.read_csv(os.path.join(ruta_actual, "clientes.csv"))
versiones_software = pd.read_csv(os.path.join(ruta_actual, "versiones_software.csv"))
instalaciones = pd.read_csv(os.path.join(ruta_actual, "instalaciones.csv"))

# 3. MÉTRICAS DE CALIDAD 
# =========================================
#FUNCIÓN DE COMPLETITUD 
# =========================================

def calcular_completitud(df):

    total_valores = df.size  # filas * columnas
    valores_no_nulos = df.notnull().sum().sum()

    completitud = (valores_no_nulos / total_valores) * 100

    return completitud
print("Completitud clientes:", calcular_completitud(clientes))
print("Completitud versiones:", calcular_completitud(versiones_software))

# =========================================
# FUNCIÓN DE EXACTITUD
# =========================================

def validar_exactitud_clientes(df):

    valores_validos = df[
        df["criticidad"].isin(["Alta", "Media", "Baja"])
    ]

    exactitud = (len(valores_validos) / len(df)) * 100

    return exactitud

def validar_exactitud_versiones(df):

    # Validar que contiene_sunburst sea booleano
    valores_validos = df[
        df["contiene_sunburst"].isin([True, False])
    ]

    exactitud = (len(valores_validos) / len(df)) * 100

    return exactitud

print("Exactitud clientes:", validar_exactitud_clientes(clientes))
print("Exactitud versiones:", validar_exactitud_versiones(versiones_software))

# =========================================
# FUNCIÓN DE CONSISTENCIA
# =========================================

def validar_consistencia_fechas(df):

    # Convertir a datetime
    df["fecha_release"] = pd.to_datetime(df["fecha_release"])
    df["fecha_compilacion"] = pd.to_datetime(df["fecha_compilacion"])

    validos = df[
        df["fecha_compilacion"] <= df["fecha_release"]
    ]

    consistencia = (len(validos) / len(df)) * 100

    return consistencia

print("Consistencia fechas versiones:", validar_consistencia_fechas(versiones_software))

# 4. INTEGRIDAD REFERENCIAL
# =========================================
# VALIDACIÓN DE INTEGRIDAD REFERENCIAL
# =========================================

def validar_integridad_referencial(df_hijo, df_padre, columna_fk, columna_pk):

    # IDs válidos en tabla padre
    ids_validos = set(df_padre[columna_pk])

    # Filtrar registros inválidos
    registros_invalidos = df_hijo[
        ~df_hijo[columna_fk].isin(ids_validos)
    ]

    total = len(df_hijo)
    invalidos = len(registros_invalidos)

    porcentaje_valido = ((total - invalidos) / total) * 100

    return porcentaje_valido, registros_invalidos

validez_clientes, errores_clientes = validar_integridad_referencial(
    instalaciones,
    clientes,
    "cliente_id",
    "cliente_id"
)

print(f"Integridad cliente_id: {validez_clientes:.2f}%")

validez_versiones, errores_versiones = validar_integridad_referencial(
    instalaciones,
    versiones_software,
    "version_id",
    "version_id"
)

print(f"Integridad version_id: {validez_versiones:.2f}%")

print("Errores cliente_id:")
print(errores_clientes)

print("Errores version_id:")
print(errores_versiones)

# 5. ANOMALÍAS
# Anomalías serían: Fechas que no tienen sentido lógico, 
# como fecha de instalación en el futuro, fecha antes de que exista 
# el software, fecha demasiado antigua.

# =========================================
# DETECCIÓN DE FECHAS ANÓMALAS
# =========================================

def detectar_fechas_fuera_rango(df):

    df["fecha_instalacion"] = pd.to_datetime(df["fecha_instalacion"])

    # Definir rango válido
    fecha_min = pd.to_datetime("2018-01-01")
    fecha_max = pd.to_datetime("2025-12-31")

    anomalias = df[
        (df["fecha_instalacion"] < fecha_min) |
        (df["fecha_instalacion"] > fecha_max)
    ]

    return anomalias

fechas_anomalas = detectar_fechas_fuera_rango(instalaciones)

print("Fechas fuera de rango:")
print(fechas_anomalas)

# =========================================
# DETECCIÓN DE OUTLIERS (INSTALACIONES POR CLIENTE)
# =========================================

def detectar_outliers_instalaciones(df):

    conteo = df.groupby("cliente_id").size()

    Q1 = conteo.quantile(0.25)
    Q3 = conteo.quantile(0.75)
    IQR = Q3 - Q1

    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR

    outliers = conteo[
        (conteo < limite_inferior) |
        (conteo > limite_superior)
    ]

    return outliers

outliers = detectar_outliers_instalaciones(instalaciones)

print("Clientes con comportamiento anómalo:")
print(outliers)

print(instalaciones["nivel_datos_sensibles"].value_counts())

#--------------------------------------------------------
# =========================================
# IDENTIFICAR INSTALACIONES AFECTADAS
# =========================================

instalaciones_afectadas = instalaciones.merge(
    versiones_software,
    on="version_id"
)

instalaciones_afectadas = instalaciones_afectadas[
    instalaciones_afectadas["contiene_sunburst"] == True
]

total_afectadas = len(instalaciones_afectadas)

print(f"Instalaciones potencialmente afectadas: {total_afectadas}")

# 6. SIMULACIÓN
# =========================================
# SIMULAR INSTALACIONES COMPROMETIDAS
# =========================================

comprometidas = instalaciones_afectadas.sample(
    n=min(10, len(instalaciones_afectadas)),  # <100 en proporción
    random_state=42
)

total_comprometidas = len(comprometidas)

print(f"Instalaciones realmente comprometidas: {total_comprometidas}")

print("\n--- RESUMEN ---")
print(f"Afectadas (simulación 18,000): {total_afectadas}")
print(f"Comprometidas reales (<100): {total_comprometidas}")

instalaciones["estado_seguridad"] = "Segura"

instalaciones.loc[
    instalaciones["instalacion_id"].isin(instalaciones_afectadas["instalacion_id"]),
    "estado_seguridad"
] = "Vulnerable"

instalaciones.loc[
    instalaciones["instalacion_id"].isin(comprometidas["instalacion_id"]),
    "estado_seguridad"
] = "Comprometida"

#-------------------------------------------------------------------------------------------
# 7. GENERACIÓN DE DATAFRAMES 
# =========================================
# GENERAR EVENTOS DE SEGURIDAD
# =========================================

import numpy as np
from faker import Faker
import random

fake = Faker()

def generar_evento(evento_id):

    tipos_evento = [
        "login",
        "descarga",
        "ejecucion",
        "conexion_remota",
        "cambio_configuracion"
    ]

    severidades = ["Baja", "Media", "Alta", "Crítica"]

    instalacion_id = random.choice(instalaciones["instalacion_id"].values)

    # Definir si es anómalo (más probable en comprometidos)
    if instalacion_id in comprometidas["instalacion_id"].values:
        es_anomalo = random.choice([True, True, False])
        severidad = random.choice(["Alta", "Crítica"])
    else:
        es_anomalo = random.choice([False, False, True])
        severidad = random.choice(severidades)

    return {
        "evento_id": evento_id,
        "instalacion_id": instalacion_id,
        "timestamp": fake.date_time_between(
            start_date='-2y',
            end_date='now'
        ),
        "tipo_evento": random.choice(tipos_evento),
        "severidad": severidad,
        "es_anomalo": es_anomalo
    }

# =========================================
# DATAFRAME EVENTOS SEGURIDAD
# =========================================

eventos_lista = []

for i in range(1, 201):
    eventos_lista.append(generar_evento(i))

eventos_seguridad = pd.DataFrame(eventos_lista)

print("\nEventos de seguridad:")
print(eventos_seguridad.head())

# =========================================
# GENERAR REPORTE DE CALIDAD
# =========================================

def generar_reporte_calidad():

    datos = [

        {
            "tabla": "clientes",
            "columna": "pais",
            "metrica": "completitud",
            "valor_actual": calcular_completitud(clientes),
            "umbral": 95,
        },

        {
            "tabla": "clientes",
            "columna": "criticidad",
            "metrica": "exactitud",
            "valor_actual": validar_exactitud_clientes(clientes),
            "umbral": 95,
        },

        {
            "tabla": "versiones_software",
            "columna": "contiene_sunburst",
            "metrica": "exactitud",
            "valor_actual": validar_exactitud_versiones(versiones_software),
            "umbral": 95,
        },

        {
            "tabla": "versiones_software",
            "columna": "fechas",
            "metrica": "consistencia",
            "valor_actual": validar_consistencia_fechas(versiones_software),
            "umbral": 95,
        }

    ]

    df = pd.DataFrame(datos)

    # Evaluar estado
    df["estado"] = df.apply(
        lambda row: "OK" if row["valor_actual"] >= row["umbral"] else "ALERTA",
        axis=1
    )

    return df
reporte_calidad = generar_reporte_calidad()

print("\nReporte de calidad:")
print(reporte_calidad)

# =========================================
# EXPORTACIÓN CSV
# =========================================

eventos_seguridad.to_csv("eventos_seguridad.csv", index=False)
reporte_calidad.to_csv("reporte_calidad.csv", index=False)

print("\nCSV generados correctamente.")

# =========================================
# 8. VISUALIZACIONES
# =========================================

import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set(style="whitegrid")

# Crear carpeta para gráficos
os.makedirs("graficos", exist_ok=True)

print("Generando gráficos...")

# =========================================
# GRÁFICO 1: SEVERIDAD DE EVENTOS
# =========================================
plt.figure()
sns.countplot(data=eventos_seguridad, x="severidad")
plt.title("Distribución de Severidad de Eventos")
plt.xlabel("Severidad")
plt.ylabel("Cantidad")
plt.savefig("graficos/grafico_severidad.png")
plt.close()

# =========================================
# GRÁFICO 2: ANOMALÍAS
# =========================================
plt.figure()
sns.countplot(data=eventos_seguridad, x="es_anomalo")
plt.title("Eventos Anómalos vs Normales")
plt.xlabel("Es anómalo")
plt.ylabel("Cantidad")
plt.savefig("graficos/grafico_anomalias.png")
plt.close()

# =========================================
# GRÁFICO 3: TIPOS DE EVENTO
# =========================================
plt.figure()
sns.countplot(data=eventos_seguridad, x="tipo_evento")
plt.xticks(rotation=45)
plt.title("Distribución de Tipos de Evento")
plt.xlabel("Tipo de evento")
plt.ylabel("Cantidad")
plt.savefig("graficos/grafico_tipos_evento.png")
plt.close()

# =========================================
# GRÁFICO 4: INSTALACIONES POR CLIENTE
# =========================================
conteo = instalaciones.groupby("cliente_id").size()

plt.figure()
sns.histplot(conteo, bins=10)
plt.title("Distribución de Instalaciones por Cliente")
plt.xlabel("Cantidad de instalaciones")
plt.ylabel("Frecuencia")
plt.savefig("graficos/grafico_instalaciones_cliente.png")
plt.close()

# =========================================
# GRÁFICO 5: ESTADO DE SEGURIDAD
# =========================================
plt.figure()
sns.countplot(data=instalaciones, x="estado_seguridad")
plt.title("Estado de Seguridad de Instalaciones")
plt.xlabel("Estado")
plt.ylabel("Cantidad")
plt.savefig("graficos/grafico_estado_seguridad.png")
plt.close()

# =========================================
# GRÁFICO 6: EVENTOS EN EL TIEMPO
# =========================================
eventos_seguridad["timestamp"] = pd.to_datetime(eventos_seguridad["timestamp"])

eventos_por_fecha = eventos_seguridad.groupby(
    eventos_seguridad["timestamp"].dt.date
).size()

plt.figure()
eventos_por_fecha.plot()
plt.title("Eventos de Seguridad en el Tiempo")
plt.xlabel("Fecha")
plt.ylabel("Cantidad")
plt.savefig("graficos/grafico_eventos_tiempo.png")
plt.close()

print("Gráficos generados correctamente.")