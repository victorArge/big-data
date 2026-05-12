from fpdf import FPDF
from pathlib import Path
import pandas as pd
import numpy as np

DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent

MAPEO_INGENIOS = {
    'ingenio el refugio s.a. de c.v.': 'el refugio',
    'el refugio s.a. de c.v.': 'el refugio',
    'el refugio': 'el refugio',
    'ingenio adolfo lopez mateos s.a. de c.v.': 'adolfo lopez mateos',
    'adolfo lopez mateos': 'adolfo lopez mateos',
    'adolfo l\xf3pez mateos': 'adolfo lopez mateos',
    'ingenio alianza popular s.a. de c.v.': 'alianza popular',
    'alianza popular': 'alianza popular',
    'fideicomiso ingenio atencingo': 'atencingo',
    'atencingo': 'atencingo',
    'cia azucarera ingenio bellavista s.a de c.v.': 'bellavista',
    'cia. azucarera ingenio bellavista s.a de c.v.': 'bellavista',
    'bellavista': 'bellavista',
    'central casasano': 'central casasano',
    'Central Casasano': 'central casasano',
    'fideicomiso ingenio casasano': 'central casasano',
    'central el potrero': 'central el potrero',
    'Central El Potrero': 'central el potrero',
    'central la providencia': 'central la providencia',
    'Central La Providencia': 'central la providencia',
    'central motzorongo s.a. de c.v.': 'central motzorongo',
    'central motzorongo': 'central motzorongo',
    'Central Motzorongo': 'central motzorongo',
    'central progreso s.a. de c.v.': 'central progreso',
    'central progreso': 'central progreso',
    'Central Progreso': 'central progreso',
    'central san miguelito': 'central san miguelito',
    'Central San Miguelito': 'central san miguelito',
    'cia azucarera la fe s.a. de c.v.': 'la fe',
    'cia. azucarera la fe s.a. de c.v.': 'la fe',
    'cia. la fe (pujiltic)': 'la fe',
    'C\u00eda. La Fe (Pujiltic)': 'la fe',
    'azsuremex': 'azsuremex',
    'azsuremex - tenosique': 'azsuremex',
    'cia. azucarera del rio guayalejo s.a. de c.v.': 'rio guayalejo',
    'calipam': 'calipam',
    'el modelo': 'el modelo',
    'El Modelo': 'el modelo',
    'el molino': 'el molino',
    'El Molino': 'el molino',
    'el higo': 'el higo',
    'El Higo': 'el higo',
    'el mante': 'el mante',
    'El Mante': 'el mante',
    'emiliano zapata': 'emiliano zapata',
    'Emiliano Zapata': 'emiliano zapata',
    'constancia': 'constancia',
    'Constancia': 'constancia',
    'cia. industrial azucarera s.a de c.v.': 'cia industrial azucarera',
    'huixtla': 'huixtla',
    'Huixtla': 'huixtla',
    'josé maría morelos': 'jose maria morelos',
    'Jos\u00e9 Mar\u00eda Morelos': 'jose maria morelos',
    'la gloria': 'la gloria',
    'La Gloria': 'la gloria',
    'la joya': 'la joya',
    'La Joya': 'la joya',
    'la margarita': 'la margarita',
    'La Margarita': 'la margarita',
    'lazaro cardenas - siembra': 'lazaro cardenas',
    'L\u00e1zaro C\u00e1rdenas - Siembra': 'lazaro cardenas',
    'mahuixtlán': 'mahuixtlan',
    'Mahuixtl\u00e1n': 'mahuixtlan',
    'melchor ocampo': 'melchor ocampo',
    'Melchor Ocampo': 'melchor ocampo',
    'pedernales': 'pedernales',
    'Pedernales': 'pedernales',
    'plan de ayala': 'plan de ayala',
    'Plan de Ayala': 'plan de ayala',
    'plan de san luis': 'plan de san luis',
    'Plan de San Luis': 'plan de san luis',
    'puga': 'puga',
    'Puga': 'puga',
    'pánuco': 'panuco',
    'P\u00e1nuco': 'panuco',
    'quesería': 'queseria',
    'Queser\u00eda': 'queseria',
    'san cristóbal': 'san cristobal',
    'San Crist\u00f3bal': 'san cristobal',
    'san francisco ameca': 'san francisco ameca',
    'San Francisco Ameca': 'san francisco ameca',
    'san josé de abajo': 'san jose de abajo',
    'San Jos\u00e9 de Abajo': 'san jose de abajo',
    'san miguel del naranjo': 'san miguel del naranjo',
    'San Miguel del Naranjo': 'san miguel del naranjo',
    'san nicolás': 'san nicolas',
    'San Nicol\u00e1s': 'san nicolas',
    'san pedro': 'san pedro',
    'San Pedro': 'san pedro',
    'santa clara': 'santa clara',
    'Santa Clara': 'santa clara',
    'santa rosalía': 'santa rosalia',
    'Santa Rosal\u00eda': 'san roselia',
    'tala - siembra': 'tala',
    'Tala - Siembra': 'tala',
    'tres valles': 'tres valles',
    'Tres Valles': 'tres valles',
    'aaron saenz garza': 'aaron saenz garza',
    'avance regional agroindustrial s.a. de c.v.': 'avance regional',
    'ciasa (cuatotolapam)': 'ciasa',
    'comercializadora san gabriel a en p': 'comercializadora san gabriel',
}

def normalizar_ingenio(nombre):
    nombre = nombre.strip().lower()
    if nombre in MAPEO_INGENIOS:
        return MAPEO_INGENIOS[nombre]
    for key, value in MAPEO_INGENIOS.items():
        if key in nombre or nombre in key:
            return value
    nombre = nombre.replace('s.a. de c.v.', '').replace('s.a.', '').replace('ingenio ', '').strip()
    return nombre.title()

def load_all_data():
    csv_files = sorted(DATA_DIR.glob("infocana_*_resumen*.csv"))
    dfs = []
    for f in csv_files:
        df = pd.read_csv(f)
        df['archivo'] = f.stem
        dfs.append(df)
    combined = pd.concat(dfs, ignore_index=True)
    combined['ingenio_normalizado'] = combined['ingenio'].apply(normalizar_ingenio)
    combined['semana_num'] = pd.to_numeric(
        combined['no_s_zafra'] if 'no_s_zafra' in combined.columns else combined.get('semana', 1),
        errors='coerce'
    ).fillna(1)
    combined['azucar_producida_total'] = combined['azucar_producida_total'].fillna(combined['azucar_total'])
    return combined

class PDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(29, 53, 87)
        self.cell(0, 10, 'INFOCANA - Analisis Predictivo de Produccion Azucarera', 0, new_x='LMARGIN', new_y='NEXT', align='C')
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Pagina {self.page_no()}/{{nb}}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(230, 57, 70)
        self.cell(0, 10, title, 0, new_x='LMARGIN', new_y='NEXT', align='L')
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(0)
        self.multi_cell(0, 6, body)
        self.ln(4)

    def sub_title(self, title):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(69, 123, 157)
        self.cell(0, 8, title, 0, new_x='LMARGIN', new_y='NEXT', align='L')

    def table_header(self, headers, widths):
        self.set_fill_color(29, 53, 87)
        self.set_text_color(255)
        self.set_font('Helvetica', 'B', 9)
        for i, h in enumerate(headers):
            self.cell(widths[i], 8, h, 1, 0, 'C', True)
        self.ln()

    def table_row(self, data, widths, fill=False):
        self.set_font('Helvetica', '', 8)
        if fill:
            self.set_fill_color(241, 250, 238)
        else:
            self.set_fill_color(255, 255, 255)
        self.set_text_color(0)
        for i, d in enumerate(data):
            self.cell(widths[i], 7, str(d), 1, 0, 'C', fill)
        self.ln()

def generar_reporte():
    print("Generando reporte PDF...")

    df = load_all_data()

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.chapter_title("1. RESUMEN EJECUTIVO")
    resumen = ("El presente documento describe el analisis predictivo de la produccion de "
               "azucar en Mexico utilizando datos abiertos del sistema INFOCANA. El proyecto "
               "aplica tecnicas de ETL (Extract, Transform, Load), regresion lineal y series "
               "de tiempo para predecir la produccion de azucar basada en variables como "
               "la cana molida y la superficie cosechada.\n\n"
               "El dashboard desarrollado permite visualizar datos historicos, comparar ingenios "
               "y zafras, y generar predicciones para la proxima zafra.")
    pdf.chapter_body(resumen)

    pdf.chapter_title("2. FUENTE DE DATOS")
    pdf.sub_title("2.1 Descripcion del Dataset")
    stats = (f"Los datos fueron obtenidos de INFOCANA (datos.gob.mx), conteniendo informacion "
             f"de produccion azucarera de Mexico desde la zafra 2012-2013 hasta 2025-2026.\n\n"
             f"Estadisticas del Dataset:\n"
             f" - Total de registros: {len(df):,}\n"
             f" - Numero de ingenios: {df['ingenio_normalizado'].nunique()}\n"
             f" - Numero de zafras: {df['zafra'].nunique()}\n"
             f" - Columnas disponibles: {len(df.columns)}\n"
             f" - Semanas por zafra: {df['semana_num'].min():.0f} a {df['semana_num'].max():.0f}")
    pdf.chapter_body(stats)

    pdf.sub_title("2.2 Variables Principales")
    variables_data = [
        ["azucar_producida_total", "Toneladas de azucar total", "toneladas"],
        ["cana_molida_bruta", "Cana molida total", "toneladas"],
        ["cana_molida_neta", "Cana molida neta", "toneladas"],
        ["superficie_cosechada", "Superficie cosechada", "hectareas"],
        ["rendimiento_campo", "Rendimiento por hectarea", "ton/ha"],
        ["rendimiento_fabrica", "Eficiencia en fabrica", "%"],
    ]
    pdf.table_header(["Variable", "Descripcion", "Unidad"], [55, 90, 40])
    for i, row in enumerate(variables_data):
        pdf.table_row(row, [55, 90, 40], i % 2 == 0)

    pdf.add_page()
    pdf.chapter_title("3. PROCESO ETL")
    etl_text = ("El proceso de ETL (Extract, Transform, Load) se implemento para preparar "
                 "los datos crudos para el analisis:\n\n"
                 "EXTRACCION:\n"
                 "- Se leyeron archivos CSV del directorio 'data/'\n"
                 "- Archivos con formato: infocana_XX_XX_resumen*.csv\n\n"
                 "TRANSFORMACION:\n"
                 "- Normalizacion de nombres de ingenios\n"
                 "- Estandarizacion de formatos de numeros\n"
                 "- Generacion de variable 'ingenio_normalizado'\n"
                 "- Imputacion de azucar_producida_total con azucar_total\n\n"
                 "CARGA:\n"
                 "- Combinacion de todos los archivos en un solo DataFrame\n"
                 "- Filtrado y limpieza de datos inconsistentes")
    pdf.chapter_body(etl_text)

    pdf.chapter_title("4. MODELO DE REGRESION LINEAL")
    pdf.chapter_body(("Se implemento un modelo de regresion lineal simple para predecir "
                     "la produccion total de azucar (Y) basandose en la cantidad de cana "
                     "molida neta (X).\n\n"
                     "Parametros del Modelo:\n"
                     "- Algoritmo: LinearRegression de scikit-learn\n"
                     "- Division de datos: 80% entrenamiento, 20% prueba\n"
                     "- Metricas evaluadas: R2 Score, RMSE, MAE\n\n"
                     "Resultados del Modelo (ejemplo con ingenio 'el refugio', zafra 2019-2020):"))

    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

    df_model = df[(df['ingenio_normalizado'] == 'el refugio') & (df['zafra'] == '2019-2020')].copy()
    df_model = df_model[['azucar_producida_total', 'cana_molida_neta']].dropna()

    if len(df_model) >= 5:
        X = df_model[['cana_molida_neta']].values
        y = df_model['azucar_producida_total'].values
        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        resultados = [
            ["R2 Score", f"{r2:.4f}"],
            ["RMSE", f"{rmse:,.2f} ton"],
            ["MAE", f"{mae:,.2f} ton"],
            ["Pendiente (coef)", f"{model.coef_[0]:.4f}"],
            ["Intercepto", f"{model.intercept_:,.2f}"],
        ]
        pdf.table_header(["Metrica", "Valor"], [60, 60])
        for i, row in enumerate(resultados):
            pdf.table_row(row, [60, 60], i % 2 == 0)

    pdf.add_page()
    pdf.chapter_title("5. MODELO DE SERIES DE TIEMPO")
    pdf.chapter_body(("Se implemento un modelo de series de tiempo para forecasting.\n\n"
                     "Metodologia:\n"
                     "- Modelo: ExponentialSmoothing con tendencia aditiva y estacionalidad\n"
                     "- Periodo estacional: 4 (semanas)\n"
                     "- El modelo captura patrones estacionales en la produccion\n\n"
                     "Interpretacion:\n"
                     "- La grafica muestra los datos historicos de produccion\n"
                     "- La linea punteada indica el inicio de las predicciones\n"
                     "- Las predicciones se generan para 1 a 24 semanas futuras"))

    pdf.chapter_title("6. DASHBOARD SHINY")
    pdf.chapter_body(("Se desarrollo un dashboard interactivo utilizando Shiny para Python.\n\n"
                     "FUNCIONALIDADES:\n"
                     "- Seleccion de ingenio y zafra para analisis detallado\n"
                     "- Visualizacion de tendencias de produccion\n"
                     "- Mapas de calor (heatmaps) para comparacion\n"
                     "- Analisis de regresion lineal con metricas\n"
                     "- Pronosticos de series de tiempo\n"
                     "- Tablas de datos con informacion detallada\n\n"
                     "TECNOLOGIAS UTILIZADAS:\n"
                     "- Python 3.11+\n"
                     "- Shiny for Python\n"
                     "- Plotly para visualizaciones\n"
                     "- Pandas para manipulacion de datos\n"
                     "- scikit-learn para machine learning\n"
                     "- statsmodels para series de tiempo"))

    pdf.add_page()
    pdf.chapter_title("7. RESULTADOS PRINCIPALES")
    pdf.sub_title("7.1 Top 10 Ingenios por Produccion")

    top_ingenios = df.groupby('ingenio_normalizado')['azucar_producida_total'].sum().sort_values(ascending=False).head(10)
    pdf.table_header(["Ingenio", "Produccion Total (ton)"], [80, 60])
    for i, (ing, val) in enumerate(top_ingenios.items()):
        pdf.table_row([ing.title(), f"{val:,.0f}"], [80, 60], i % 2 == 0)

    pdf.ln(5)
    pdf.sub_title("7.2 Produccion por Zafra")
    produccion_zafra = df.groupby('zafra')['azucar_producida_total'].sum().sort_index()
    pdf.table_header(["Zafra", "Produccion Total (ton)"], [80, 60])
    for i, (zafra, val) in enumerate(produccion_zafra.items()):
        pdf.table_row([zafra, f"{val:,.0f}"], [80, 60], i % 2 == 0)

    pdf.add_page()
    pdf.chapter_title("8. CONCLUSIONES")
    pdf.chapter_body(("1. El modelo de regresion lineal muestra una fuerte correlacion entre "
                     "la cantidad de cana molida y la produccion de azucar.\n\n"
                     "2. Los modelos de series de tiempo capturan efectivamente los patrones "
                     "estacionales de la produccion azucarera.\n\n"
                     "3. El dashboard proporciona una herramienta accesible para explorar "
                     "los datos y generar insights.\n\n"
                     "4. Los datos de INFOCANA son una fuente valiosa para el analisis de "
                     "la industria azucarera mexicana.\n\n"
                     "5. Se recomienda actualizar periodicamente los datos para mantener "
                     "la relevancia de las predicciones."))

    pdf.chapter_title("9. RECOMENDACIONES")
    pdf.chapter_body(("1. Implementar un pipeline automatizado para la actualizacion de datos.\n"
                     "2. Considerar modelos de machine learning mas avanzados (Random Forest, XGBoost).\n"
                     "3. Agregar validacion cruzada para mejorar la robustez de las metricas.\n"
                     "4. Expandir el dashboard con mas visualizaciones y comparativas.\n"
                     "5. Desplegar el dashboard en GitHub Pages para acceso publico.\n"
                     "6. Generar reportes automaticos periodicos con los pronosticos."))

    pdf.add_page()
    pdf.chapter_title("10. REFERENCIAS")
    pdf.chapter_body(("- INFOCANA: Sistema de Informacion de la Cana de Azucar\n"
                     "  https://datos.gob.mx/busca/dataset?tags=infocana\n\n"
                     "- Documentacion Shiny for Python:\n"
                     "  https://shiny.posit.co/\n\n"
                     "- scikit-learn:\n"
                     "  https://scikit-learn.org/\n\n"
                     "- statsmodels:\n"
                     "  https://www.statsmodels.org/\n\n"
                     "- Plotly Python:\n"
                     "  https://plotly.com/python/"))

    filename = OUTPUT_DIR / "Reporte_INFOCANA.pdf"
    pdf.output(str(filename))
    print(f"Reporte generado: {filename}")
    return str(filename)

if __name__ == "__main__":
    generar_reporte()