import pandas as pd
import os

ruta_actual = os.path.dirname(os.path.abspath(__file__))

# Rutas a otros roles
ruta_rol1 = os.path.join(ruta_actual, "..", "ENTREGABLES ROL 1")
ruta_rol2 = os.path.join(ruta_actual, "..", "ENTREGABLES ROL 2")

# =========================================
# CARGA DE DATOS (ROL 1)
# =========================================

clientes = pd.read_csv(os.path.join(ruta_rol1, "clientes.csv"))
versiones_software = pd.read_csv(os.path.join(ruta_rol1, "versiones_software.csv"))
instalaciones = pd.read_csv(os.path.join(ruta_rol1, "instalaciones.csv"))

# =========================================
# CARGA DE DATOS (ROL 2)
# =========================================

eventos_seguridad = pd.read_csv(os.path.join(ruta_rol2, "eventos_seguridad.csv"))
reporte_calidad = pd.read_csv(os.path.join(ruta_rol2, "reporte_calidad.csv"))

print("Datos cargados correctamente")
print(clientes.shape)
print(eventos_seguridad.shape)

#USAR MERGE PARA RELACIONAR DATAFRAME
#Unir instalaciones con clientes
inst_clientes = instalaciones.merge(
    clientes,
    on="cliente_id",
    how="left"
)

print(inst_clientes.head())
#Unir instalaciones con version de software
inst_clientes_versiones = inst_clientes.merge(
    versiones_software,
    on="version_id",
    how="left"
)

print(inst_clientes_versiones.head())

#Unir con eventos de seguridad
df_integrado = eventos_seguridad.merge(
    inst_clientes_versiones,
    on="instalacion_id",
    how="left"
)

print(df_integrado.head())

print("\nDimensiones del DataFrame integrado:")
print(df_integrado.shape)

#CREAR DATAFRAME CONSOLIDADO
#Seleccionar columnas importantes
df_consolidado = df_integrado[[
    "evento_id",
    "timestamp",
    "tipo_evento",
    "severidad",
    "es_anomalo",
    
    "instalacion_id",
    "fecha_instalacion",
    "nivel_datos_sensibles",
    
    "cliente_id",
    "nombre_organizacion",
    "sector",
    "criticidad",
    
    "version_id",
    "nombre_version",
    "contiene_sunburst"
]]
#Convertir fechas 
df_consolidado["timestamp"] = pd.to_datetime(df_consolidado["timestamp"])
df_consolidado["fecha_instalacion"] = pd.to_datetime(df_consolidado["fecha_instalacion"]) 
#Ordenar datos 
df_consolidado = df_consolidado.sort_values(by="timestamp")
#Verificar resultado
print(df_consolidado.head())
print("\nDimensiones:", df_consolidado.shape)

#MAPEAR EVENTOS AL CICLO DE VIDA DE LOS DATOS 
#Función de mapeo
def mapear_ciclo_vida(tipo_evento):
    if tipo_evento in ["login", "acceso"]:
        return "Uso", "Data Security"
    elif tipo_evento == "actualizacion":
        return "Mantenimiento", "Data Maintenance"
    elif tipo_evento == "instalacion":
        return "Creacion", "Data Integration"
    elif tipo_evento == "eliminacion":
        return "Eliminacion", "Data Governance"
    elif tipo_evento == "alerta":
        return "Uso", "Data Security"
    else:
        return "Uso", "Data Management"
    
#Aplicar al dataset
df_ciclo = eventos_seguridad.copy()

df_ciclo[["fase_ciclo_vida", "area_dama"]] = df_ciclo["tipo_evento"].apply(
    lambda x: pd.Series(mapear_ciclo_vida(x))
)
#Crear columnas finales 
df_ciclo["fecha"] = pd.to_datetime(df_ciclo["timestamp"])

df_ciclo["descripcion"] = "Evento de tipo " + df_ciclo["tipo_evento"] 

#Crear dataframe final
eventos_ciclo_vida = df_ciclo[[
    "evento_id",
    "fase_ciclo_vida",
    "fecha",
    "descripcion",
    "area_dama"
]]

#Verificar
print(eventos_ciclo_vida.head())
print("\nDimensiones:", eventos_ciclo_vida.shape)

#Exportar CSV 
eventos_ciclo_vida.to_csv("eventos_ciclo_vida.csv", index=False)

ruta_salida = os.path.join(ruta_actual, "eventos_ciclo_vida.csv")

eventos_ciclo_vida.to_csv(ruta_salida, index=False)

print("\nArchivo eventos_ciclo_vida.csv generado correctamente")

# =========================================
# AGREGAR FASE AL DATAFRAME CONSOLIDADO
# =========================================

df_consolidado = df_consolidado.merge(
    eventos_ciclo_vida[["evento_id", "fase_ciclo_vida"]],
    on="evento_id",
    how="left"
)

#CALCULAR MÉTRICAS POR FASE DEL CICLO DE VIDA
#Eventos por fase
metricas_fase = eventos_ciclo_vida.groupby("fase_ciclo_vida").size().reset_index(name="total_eventos")

print(metricas_fase)

#Eventos anómalos por fase
anomalias_fase = df_consolidado.groupby("fase_ciclo_vida")["es_anomalo"].sum().reset_index()

anomalias_fase.rename(columns={"es_anomalo": "eventos_anomalos"}, inplace=True)

print(anomalias_fase)
#Eventos por severidad y fase 
severidad_fase = df_consolidado.groupby(
    ["fase_ciclo_vida", "severidad"]
).size().reset_index(name="cantidad")

print(severidad_fase)
#Unir métricas 
metricas_finales = metricas_fase.merge(
    anomalias_fase,
    on="fase_ciclo_vida",
    how="left"
)

print(metricas_finales)
#Exportar 
metricas_finales.to_csv("metricas_ciclo_vida.csv", index=False)

#VISUALIZACIONES
#Importaciones
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set(style="whitegrid")

os.makedirs("graficos_rol3", exist_ok=True)

#Timeline del ataque
# Convertir fecha
df_consolidado["timestamp"] = pd.to_datetime(df_consolidado["timestamp"])

eventos_tiempo = df_consolidado.groupby(
    df_consolidado["timestamp"].dt.date
).size()

plt.figure()
eventos_tiempo.plot()

plt.title("Timeline del ataque")
plt.xlabel("Fecha")
plt.ylabel("Cantidad de eventos")

plt.savefig("graficos_rol3/timeline_ataque.png")
plt.close()

#Gráfico de cascada 
import matplotlib.pyplot as plt

etapas = ["Total clientes", "Expuestos", "Comprometidos"]
valores = [18000, 200, 80]

plt.figure()
plt.bar(etapas, valores)

plt.title("Impacto del ataque SUNBURST")
plt.ylabel("Cantidad")

plt.savefig("graficos_rol3/cascada_impacto.png")
plt.close()

#DASHBOARD
#Gráfico 1 - Eventos por fase 
sns.countplot(data=df_consolidado, x="fase_ciclo_vida")
plt.title("Eventos por fase del ciclo de vida")
plt.savefig("graficos_rol3/eventos_fase.png")
plt.close()

#Gráfico 2 - Anomalías por fase
sns.barplot(
    data=df_consolidado,
    x="fase_ciclo_vida",
    y="es_anomalo"
)
plt.title("Anomalías por fase")
plt.savefig("graficos_rol3/anomalias_fase.png")
plt.close()

#Gráfico 3 - Severidad
sns.countplot(data=df_consolidado, x="severidad")
plt.title("Distribución de severidad")
plt.savefig("graficos_rol3/severidad.png")
plt.close()

#Grafico 4 - Versiones comprometidas
sns.countplot(data=df_consolidado, x="contiene_sunburst")
plt.title("Versiones comprometidas")
plt.savefig("graficos_rol3/versiones_comprometidas.png")
plt.close()

#Gráfico 5 - Sector afectado
sns.countplot(data=df_consolidado, x="sector")
plt.xticks(rotation=45)
plt.title("Sectores afectados")
plt.savefig("graficos_rol3/sectores.png")
plt.close()

#IDENTIFICAR CLIENTES COMPROMETIDOS VS EXPUESTOS
resumen_impacto = df_consolidado.groupby("version_id").agg(
    total_instalaciones=("instalacion_id", "count")
).reset_index()

# Expuestos
expuestos = df_consolidado[df_consolidado["contiene_sunburst"] == True]
expuestos = expuestos.groupby("version_id")["cliente_id"].nunique().reset_index()
expuestos.rename(columns={"cliente_id": "clientes_expuestos"}, inplace=True)

# Comprometidos
comprometidos = df_consolidado[
    (df_consolidado["contiene_sunburst"] == True) &
    (df_consolidado["es_anomalo"] == True)
]
comprometidos = comprometidos.groupby("version_id")["cliente_id"].nunique().reset_index()
comprometidos.rename(columns={"cliente_id": "clientes_comprometidos"}, inplace=True)

# Unir todo
resumen_impacto = resumen_impacto.merge(expuestos, on="version_id", how="left")
resumen_impacto = resumen_impacto.merge(comprometidos, on="version_id", how="left")

# Reemplazar NaN por 0
resumen_impacto.fillna(0, inplace=True)

print(resumen_impacto)

#Exportar CSV
resumen_impacto.to_csv("resumen_impacto.csv", index=False)

print("\nArchivo resumen_impacto.csv generado correctamente")