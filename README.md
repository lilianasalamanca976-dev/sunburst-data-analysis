# SUNBURST DATA ANALYSIS

## Integrantes y roles

Karol Liliana Salamanca Herrera 

---
## Descripción del Proyecto

Este proyecto analiza el incidente cibernético SUNBURST (SolarWinds) mediante la generación de datos sintéticos, validación de calidad de datos e integración de información, siguiendo los principios del marco DAMA-DMBOK.

El objetivo principal es simular un entorno real de análisis de datos para identificar clientes afectados, detectar anomalías y comprender el ciclo de vida de los datos durante un incidente de seguridad.
---
## Tecnologías utilizadas
- Python  
- pandas  
- numpy  
- faker  
- matplotlib  
- seaborn  
- Jupyter Notebook  
---
## Estructura del proyecto 
```
sunburst-data-analysis/
├── data/
├── notebooks/
├── scripts/
├── visualizations/
├── docs/
├── requirements.txt
└── README.md
```
---
## Instalación y ejecución

### 1. Clonar repositorio

```bash
git clone https://github.com/lilianasalamanca976-dev/sunburst-data-analysis.git
cd sunburst-data-analysis
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```
### 3. Ejecutar script 
```bash
python scripts/rol1_generacion_datos.py
python scripts/rol2_calidad_datos.py
python scripts/rol3_integracion.py
```
---
## Descripción de los datos

El proyecto genera y analiza los siguientes datasets:

- clientes
- versiones_software
- instalaciones
- eventos_seguridad
- reporte_calidad
- eventos_ciclo_vida
- resumen_impacto
---

## Principales Hallazgos
- Diferencia significativa entre clientes expuestos y comprometidos
- Mayor concentración de eventos en la fase de uso
- Presencia de anomalías en eventos de seguridad
- La calidad de los datos impacta directamente el análisis

---
## Notas
- Datos generados sintéticamente con Python
- Aplicación de métricas DAMA-DMBOK
- Simulación de un caso real de ciberseguridad
