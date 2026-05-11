# Proyecto Infocana - Dashboard de Predicciones Azucareras

## Estructura del proyecto
```
proyecto_infocana/
├── app.py              # Aplicación Shiny principal
├── requirements.txt    # Dependencias de Python
├── data/               # Archivos CSV de Infocana (13 zafras)
│   ├── infocana_12_13_resumen_ok.csv
│   ├── infocana_14_15_resumen_ok.csv
│   └── ... (13 archivos en total)
└── README.md
```

## Instalación

1. Crear entorno virtual (recomendado):
```powershell
cd proyecto_infocana
python -m venv venv
.\venv\Scripts\activate
```

2. Instalar dependencias:
```powershell
pip install -r requirements.txt
```

3. Ejecutar la aplicación:
```powershell
shiny run
```

La aplicación se abrirá en http://127.0.0.1:8000

## Funcionalidades
- Selector de ingenio azucarero
- Selector de zafra (temporada)
- Selector de variable a visualizar
- Dashboard con gráficos de tendencias
- Tabla de datos filtrados
- Módulo de predicciones (en desarrollo)

## Datos
Los 13 archivos CSV contienen datos de producción de azúcar de ingenios mexicanos desde 2012-2013 hasta 2025-2026.