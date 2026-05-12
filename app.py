from shiny import App, ui, render
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import tempfile

DATA_DIR = Path(__file__).parent / "data"

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

df_combined = load_all_data()

ingenios = sorted(df_combined['ingenio_normalizado'].unique(), key=str.lower)
zafras = sorted(df_combined['zafra'].unique(), reverse=True)

default_ingenio = ingenios[0]
default_zafra = zafras[0]

for ing in ingenios:
    for zafra in zafras:
        if len(df_combined[(df_combined['ingenio_normalizado'] == ing) & (df_combined['zafra'] == zafra)]) > 0:
            default_ingenio = ing
            default_zafra = zafra
            break
    else:
        continue
    break

VARIABLES = {
    "Producci\u00f3n Total de Az\u00facar": "azucar_producida_total",
    "Ca\u00f1a Molida Bruta": "cana_molida_bruta",
    "Rendimiento Campo": "rendimiento_campo",
    "Rendimiento F\u00e1brica": "rendimiento_fabrica",
    "Rendimiento Agroindustrial": "rendimiento_agroindustrial",
    "Superficie Cosechada": "superficie_cosechada",
}

ACCENT_COLOR = "#e63946"
SECONDARY_COLOR = "#457b9d"
DARK_BG = "#1d3557"
LIGHT_BG = "#f1faee"
CARD_BG = "#ffffff"

def plot_to_image(fig, width=600, height=400):
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        img_bytes = fig.to_image(format="png", scale=2, width=width, height=height)
        f.write(img_bytes)
        f.flush()
        return {"src": f.name}

custom_theme = """
<style>
  :root {
    --accent: #e63946;
    --secondary: #457b9d;
    --dark-bg: #1d3557;
    --light-bg: #f1faee;
    --card-bg: #ffffff;
    --text-primary: #1d3557;
    --text-secondary: #457b9d;
    --border-radius: 12px;
    --shadow: 0 4px 20px rgba(0,0,0,0.08);
  }
  body { background-color: var(--light-bg); font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
  .card { background: var(--card-bg); border-radius: var(--border-radius); box-shadow: var(--shadow); border: none; }
  .card-header { background: var(--dark-bg); color: white; border-radius: var(--border-radius) var(--border-radius) 0 0; font-weight: 600; }
  .sidebar { background: var(--dark-bg) !important; color: white; }
  .sidebar h2, .sidebar h4 { color: white; }
  .sidebar .card { background: rgba(255,255,255,0.1); border-radius: 10px; }
  .sidebar .card-header { background: transparent; padding: 0.5rem; }
  .sidebar .card-body { padding: 0.5rem; color: rgba(255,255,255,0.85); font-size: 0.9rem; }
  .nav-tabs { border-bottom: 2px solid var(--light-bg); }
  .nav-tabs .nav-link { color: var(--text-secondary); border: none; border-bottom: 3px solid transparent; padding: 12px 20px; font-weight: 500; transition: all 0.3s; }
  .nav-tabs .nav-link:hover { color: var(--accent); border-color: transparent; }
  .nav-tabs .nav-link.active { color: var(--accent); background: transparent; border: none; border-bottom: 3px solid var(--accent); }
  .kpi-card { text-align: center; padding: 20px; border-left: 4px solid var(--accent); }
  .kpi-value { font-size: 2.2rem; font-weight: 700; color: var(--dark-bg); line-height: 1; }
  .kpi-label { font-size: 0.85rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px; margin-top: 8px; }
  .kpi-trend { font-size: 0.8rem; margin-top: 8px; }
  .kpi-trend.up { color: #2ecc71; }
  .kpi-trend.down { color: var(--accent); }
  .form-select, .form-control { border-radius: 8px; border: 1px solid #dee2e6; padding: 10px 14px; }
  .form-select:focus, .form-control:focus { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(230, 57, 70, 0.15); }
  .btn-accent { background: var(--accent); color: white; border: none; border-radius: 8px; padding: 10px 24px; font-weight: 500; }
  .btn-accent:hover { background: #c92a35; color: white; }
  .shiny-input-container { margin-bottom: 15px; }
  .nav-item { font-size: 0.95rem; }
  .table { font-size: 0.9rem; }
  .table thead th { background: var(--dark-bg); color: white; border: none; padding: 12px; }
  .table tbody tr:hover { background-color: rgba(69, 123, 157, 0.08); }
  .value-box { background: linear-gradient(135deg, var(--dark-bg) 0%, var(--secondary) 100%); color: white; border-radius: var(--border-radius); padding: 20px; text-align: center; }
  .value-box .value { font-size: 2rem; font-weight: 700; }
  .value-box .label { font-size: 0.8rem; opacity: 0.85; text-transform: uppercase; }
  .card img, .shiny-image > img { max-width: 100%; max-height: 400px; width: auto; height: auto; object-fit: contain; display: block; margin: 0 auto; }
  .shiny-image { display: flex; justify-content: center; align-items: center; flex-direction: column; }
</style>
"""

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h2("INFOCANA", style="color: white; font-weight: 700; margin-bottom: 5px;"),
        ui.p("An\u00e1lisis de Producci\u00f3n Azucarera", style="color: rgba(255,255,255,0.7); margin: 0;"),
        ui.hr(style="border-color: rgba(255,255,255,0.2);"),
        ui.div(
            ui.h4("Filtros", style="color: white; font-size: 1rem; margin-bottom: 15px;"),
            ui.input_selectize("ingenio", "Ingenio", choices=ingenios, selected=default_ingenio),
            ui.input_selectize("zafra", "Zafra", choices=zafras, selected=default_zafra),
            ui.input_selectize("variable", "Variable", choices=list(VARIABLES.keys()), selected=list(VARIABLES.keys())[0]),
        ),
        ui.hr(style="border-color: rgba(255,255,255,0.2);"),
        ui.div(
            ui.h4("Acerca de", style="color: white; font-size: 1rem;"),
            ui.p("Sistema de an\u00e1lisis y visualizaci\u00f3n de datos de producci\u00f3n azucarera en M\u00e9xico.", style="color: rgba(255,255,255,0.7); font-size: 0.85rem;"),
            ui.p(f"Ingenios registrados: {len(ingenios)}", style="color: rgba(255,255,255,0.7); font-size: 0.85rem;"),
            ui.p(f"Zafras disponibles: {len(zafras)}", style="color: rgba(255,255,255,0.7); font-size: 0.85rem;"),
        ),
        style="padding: 20px;",
    ),
    ui.head_content(ui.HTML(custom_theme)),
    ui.navset_tab(
        ui.nav_panel("Dashboard",
            ui.layout_columns(
                ui.card(
                    ui.card_header("Produccion Total"),
                    ui.div(
                        ui.output_text("total_produccion"),
                        ui.output_text("total_produccion_und"),
                    ),
                    class_="kpi-card",
                ),
                ui.card(
                    ui.card_header("Rendimiento Campo"),
                    ui.div(
                        ui.output_text("rendimiento_campo_val"),
                        ui.output_text("rendimiento_campo_und"),
                    ),
                    class_="kpi-card",
                ),
                ui.card(
                    ui.card_header("Rendimiento Fabrica"),
                    ui.div(
                        ui.output_text("rendimiento_fabrica_val"),
                        ui.output_text("rendimiento_fabrica_und"),
                    ),
                    class_="kpi-card",
                ),
                ui.card(
                    ui.card_header("Superficie"),
                    ui.div(
                        ui.output_text("superficie_val"),
                        ui.output_text("superficie_und"),
                    ),
                    class_="kpi-card",
                ),
            ),
            ui.card(
                ui.card_header("Tendencia de Produccion"),
                ui.output_image("grafico_linea"),
            ),
        ),
        ui.nav_panel("Comparativas",
            ui.card(
                ui.card_header("Top 10 Ingenios - Produccion de Azucar"),
                ui.output_image("grafico_barras_top10"),
            ),
            ui.br(),
            ui.card(
                ui.card_header("Comparacion por Zafra"),
                ui.output_image("grafico_barras_zafra"),
            ),
        ),
        ui.nav_panel("Heatmaps",
            ui.card(
                ui.card_header("Rendimiento por Ingenio y Zafra"),
                ui.output_image("heatmap_rendimiento"),
            ),
            ui.br(),
            ui.card(
                ui.card_header("Produccion por Ingenio y Zafra"),
                ui.output_image("heatmap_produccion"),
            ),
        ),
        ui.nav_panel("Datos",
            ui.card(
                ui.card_header("Detalle de Datos"),
                ui.output_table("tabla_datos"),
            ),
        ),
        ui.nav_panel("Predicciones",
            ui.card(
                ui.card_header("Panel de Prediccion"),
                ui.layout_columns(
                    ui.div(
                        ui.h5("Configuracion"),
                        ui.input_selectize("pred_ingenio", "Ingenio", choices=ingenios, selected=default_ingenio),
                        ui.input_selectize("pred_variable", "Variable", choices=list(VARIABLES.keys()), selected=list(VARIABLES.keys())[0]),
                        ui.input_slider("pred_meses", "Meses:", min=1, max=24, value=3, step=1),
                    ),
                    ui.div(
                        ui.h5("Grafico"),
                        ui.output_image("grafico_prediccion"),
                    ),
                    ui.div(
                        ui.h5("Resultados"),
                        ui.output_table("tabla_prediccion"),
                    ),
                    col_widths=[2, 7, 3],
                ),
            ),
        ),
        ui.nav_panel("Modelos ML",
            ui.layout_columns(
                ui.card(
                    ui.card_header("Regresion Lineal - Configuracion"),
                    ui.input_selectize("ml_ingenio", "Ingenio", choices=ingenios, selected=default_ingenio),
                    ui.input_selectize("ml_variable_x", "Variable X (predictor)",
                                       choices=["cana_molida_neta", "superficie_cosechada", "cana_molida_bruta"],
                                       selected="cana_molida_neta"),
                    ui.input_selectize("ml_zafra", "Zafra", choices=zafras, selected=zafras[0]),
                    ui.input_numeric("ml_train_size", "Train size (%):", value=80, min=50, max=95),
                    ui.input_action_button("btn_entrenar", "Entrenar Modelo", class_="btn-accent"),
                ),
                ui.card(
                    ui.card_header("Resultados del Modelo"),
                    ui.output_table("ml_resultados"),
                ),
            ),
            ui.layout_columns(
                ui.card(
                    ui.card_header("Regresion Lineal - Grafico"),
                    ui.output_image("grafico_regresion"),
                ),
                ui.card(
                    ui.card_header("Serie de Tiempo - SARIMAX"),
                    ui.output_image("grafico_sarimax"),
                ),
            ),
            ui.card(
                ui.card_header("Prediccion Global - Todos los Ingenios"),
                ui.output_table("ml_prediccion_global"),
            ),
        ),
    ),
    title="INFOCANA - Dashboard Azucarero",
)

def server(input, output, session):
    def get_filtro():
        return df_combined[
            (df_combined['ingenio_normalizado'] == input.ingenio()) &
            (df_combined['zafra'] == input.zafra())
        ]

    def get_col():
        return VARIABLES.get(input.variable(), "azucar_producida_total")

    @output
    @render.text
    def total_produccion():
        filt = get_filtro()
        if filt.empty:
            return "N/A"
        col = get_col()
        if col in filt.columns:
            val = filt[col].sum()
            if val > 1000000:
                return f"{val/1000:.1f}"
        return "N/A"

    @output
    @render.text
    def total_produccion_und():
        filt = get_filtro()
        if filt.empty:
            return ""
        col = get_col()
        if col in filt.columns:
            val = filt[col].sum()
            if val > 1000000:
                return "miles de toneladas"
        return "toneladas"

    @output
    @render.text
    def rendimiento_campo_val():
        filt = get_filtro()
        if filt.empty:
            return "N/A"
        if 'rendimiento_campo' in filt.columns:
            val = filt['rendimiento_campo'].mean()
            return f"{val:.1f}"
        return "N/A"

    @output
    @render.text
    def rendimiento_campo_und():
        return "ton/ha promedio"

    @output
    @render.text
    def rendimiento_fabrica_val():
        filt = get_filtro()
        if filt.empty:
            return "N/A"
        if 'rendimiento_fabrica' in filt.columns:
            val = filt['rendimiento_fabrica'].mean()
            return f"{val:.1f}"
        return "N/A"

    @output
    @render.text
    def rendimiento_fabrica_und():
        return "% eficiencia"

    @output
    @render.text
    def superficie_val():
        filt = get_filtro()
        if filt.empty:
            return "N/A"
        if 'superficie_cosechada' in filt.columns:
            val = filt['superficie_cosechada'].sum()
            if val > 1000:
                return f"{val/1000:.1f}K"
            return f"{val:,.0f}"
        return "N/A"

    @output
    @render.text
    def superficie_und():
        return "hect\u00e1reas"

    @output
    @render.image
    def grafico_linea():
        filt = get_filtro()
        if filt.empty:
            fig = go.Figure()
            fig.add_annotation(text="Sin datos disponibles", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font_size=20)
            return plot_to_image(fig)
        col = get_col()
        if col not in filt.columns:
            fig = go.Figure()
            fig.add_annotation(text="Variable no disponible", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            return plot_to_image(fig)
        fig = px.line(filt, x='semana_num', y=col, markers=True,
                      title=f"{input.ingenio().title()} - Zafra {input.zafra()}")
        fig.update_layout(
            plot_bgcolor='rgba(241,250,238,0.9)',
            paper_bgcolor='white',
            title_font_size=16,
            title_font=dict(color='#1d3557'),
            font=dict(color='#1d3557'),
            margin=dict(l=40, r=40, t=60, b=40),
            height=400,
            width=600
        )
        fig.update_traces(line=dict(color='#e63946', width=3), marker=dict(color='#457b9d', size=8))
        return plot_to_image(fig)

    @output
    @render.image
    def grafico_barras_top10():
        agg = df_combined.groupby('ingenio_normalizado')['azucar_producida_total'].sum().sort_values(ascending=False).head(10).reset_index()
        fig = px.bar(agg, x='ingenio_normalizado', y='azucar_producida_total',
                     title="Top 10 Ingenios - Producci\u00f3n Total de Az\u00facar",
                     color='azucar_producida_total', color_continuous_scale='RdYlGn')
        fig.update_layout(
            xaxis_title="Ingenio",
            yaxis_title="Toneladas de Az\u00facar",
            plot_bgcolor='rgba(241,250,238,0.9)',
            paper_bgcolor='white',
            title_font_size=16,
            title_font=dict(color='#1d3557'),
            font=dict(color='#1d3557'),
            margin=dict(l=40, r=40, t=60, b=80),
            xaxis_tickangle=-45,
            height=400,
            width=600
        )
        return plot_to_image(fig)

    @output
    @render.image
    def grafico_barras_zafra():
        agg = df_combined.groupby('zafra')['azucar_producida_total'].sum().reset_index().sort_values('zafra')
        fig = px.bar(agg, x='zafra', y='azucar_producida_total',
                     title="Producci\u00f3n de Az\u00facar por Zafra",
                     color='azucar_producida_total', color_continuous_scale='Blues')
        fig.update_layout(
            xaxis_title="Zafra",
            yaxis_title="Toneladas de Az\u00facar",
            plot_bgcolor='rgba(241,250,238,0.9)',
            paper_bgcolor='white',
            title_font_size=16,
            title_font=dict(color='#1d3557'),
            font=dict(color='#1d3557'),
            margin=dict(l=40, r=40, t=60, b=80),
            xaxis_tickangle=-45,
            height=400,
            width=600
        )
        return plot_to_image(fig)

    @output
    @render.image
    def heatmap_rendimiento():
        agg = df_combined.groupby(['ingenio_normalizado', 'zafra'])['rendimiento_campo'].mean().reset_index()
        pivot = agg.pivot(index='ingenio_normalizado', columns='zafra', values='rendimiento_campo')
        pivot = pivot.sort_values(pivot.columns[-1], ascending=False).head(20)
        fig = px.imshow(pivot, title="Rendimiento Campo (ton/ha)", color_continuous_scale='RdYlGn', aspect='auto')
        fig.update_layout(
            title_font_size=16,
            title_font=dict(color='#1d3557'),
            font=dict(color='#1d3557'),
            margin=dict(l=40, r=40, t=60, b=40),
            height=400,
            width=600
        )
        return plot_to_image(fig)

    @output
    @render.image
    def heatmap_produccion():
        agg = df_combined.groupby(['ingenio_normalizado', 'zafra'])['azucar_producida_total'].sum().reset_index()
        pivot = agg.pivot(index='ingenio_normalizado', columns='zafra', values='azucar_producida_total')
        pivot = pivot.sort_values(pivot.columns[-1], ascending=False).head(20)
        fig = px.imshow(pivot, title="Producci\u00f3n Total de Az\u00facar (toneladas)", color_continuous_scale='Blues', aspect='auto')
        fig.update_layout(
            title_font_size=16,
            title_font=dict(color='#1d3557'),
            font=dict(color='#1d3557'),
            margin=dict(l=40, r=40, t=60, b=40),
            height=400,
            width=500
        )
        return plot_to_image(fig)

    @output
    @render.table
    def tabla_datos():
        filt = get_filtro()
        if filt.empty:
            return pd.DataFrame({"Mensaje": ["Sin datos disponibles"]})
        cols = [c for c in ['ingenio_normalizado', 'zafra', 'semana_num', 'no_s_zafra',
                             'azucar_producida_total', 'cana_molida_bruta',
                             'rendimiento_campo', 'rendimiento_fabrica'] if c in filt.columns]
        if not cols:
            cols = filt.columns[:8].tolist()
        resultado = filt[cols].head(20).copy()
        if 'semana_num' in resultado.columns:
            resultado.rename(columns={'semana_num': 'Semana'}, inplace=True)
        if 'azucar_producida_total' in resultado.columns:
            resultado.rename(columns={'azucar_producida_total': 'Az\u00facar (ton)'}, inplace=True)
        if 'cana_molida_bruta' in resultado.columns:
            resultado.rename(columns={'cana_molida_bruta': 'Ca\u00f1a (ton)'}, inplace=True)
        if 'rendimiento_campo' in resultado.columns:
            resultado.rename(columns={'rendimiento_campo': 'Rend. Campo'}, inplace=True)
        if 'rendimiento_fabrica' in resultado.columns:
            resultado.rename(columns={'rendimiento_fabrica': 'Rend. Fab.'}, inplace=True)
        return resultado

    @output
    @render.table
    def tabla_prediccion():
        try:
            from statsmodels.tsa.holtwinters import ExponentialSmoothing
            ing = input.pred_ingenio()
            var_col = VARIABLES.get(input.pred_variable(), 'azucar_producida_total')
            meses = int(input.pred_meses())

            datos = df_combined[df_combined['ingenio_normalizado'] == ing].copy()
            datos = datos.sort_values('semana_num')

            if len(datos) < 5:
                return pd.DataFrame({"Mensaje": ["Datos insuficientes para predecir"]})

            serie = datos[var_col].dropna().values
            if len(serie) < 5:
                return pd.DataFrame({"Mensaje": ["La serie no tiene suficientes datos"]})

            model = ExponentialSmoothing(serie, trend='add', seasonal='add', seasonal_periods=4)
            fitted = model.fit()
            forecast = fitted.forecast(meses)

            result = pd.DataFrame({
                'Mes': range(1, meses + 1),
                'Predicci\u00f3n': forecast.round(2)
            })
            return result
        except Exception as e:
            return pd.DataFrame({"Error": [str(e)]})

    @output
    @render.image
    def grafico_prediccion():
        try:
            from statsmodels.tsa.holtwinters import ExponentialSmoothing
            ing = input.pred_ingenio()
            var_col = VARIABLES.get(input.pred_variable(), 'azucar_producida_total')
            meses = int(input.pred_meses())

            datos = df_combined[df_combined['ingenio_normalizado'] == ing].copy()
            datos = datos.sort_values('semana_num')

            if len(datos) < 5:
                fig = go.Figure()
                fig.add_annotation(text="Datos insuficientes", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
                return plot_to_image(fig)

            serie = datos[var_col].dropna().values
            if len(serie) < 5:
                fig = go.Figure()
                fig.add_annotation(text="Serie con datos insuficientes", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
                return plot_to_image(fig)

            model = ExponentialSmoothing(serie, trend='add', seasonal='add', seasonal_periods=4)
            fitted = model.fit()
            forecast = fitted.forecast(meses)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=list(range(len(serie))), y=serie, mode='lines+markers', name='Datos Hist\u00f3ricos',
                                     line=dict(color='#1d3557', width=2)))
            fig.add_trace(go.Scatter(x=list(range(len(serie), len(serie) + meses)), y=forecast, mode='lines+markers', name='Predicci\u00f3n',
                                     line=dict(color='#e63946', width=2, dash='dash')))
            fig.add_vline(x=len(serie)-1, line_dash="dot", line_color="#457b9d", annotation_text="Inicio Predicci\u00f3n")
            fig.update_layout(
                title=f"Predicci\u00f3n: {ing.title()}",
                xaxis_title="Per\u00edodo",
                yaxis_title=var_col.replace('_', ' ').title(),
                plot_bgcolor='rgba(241,250,238,0.9)',
                paper_bgcolor='white',
                title_font=dict(color='#1d3557'),
                font=dict(color='#1d3557'),
                margin=dict(l=40, r=40, t=60, b=40),
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
            )
            return plot_to_image(fig)
        except Exception as e:
            fig = go.Figure()
            fig.add_annotation(text=f"Error: {str(e)}", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            return plot_to_image(fig)

    @output
    @render.table
    def ml_resultados():
        try:
            from sklearn.linear_model import LinearRegression
            from sklearn.model_selection import train_test_split
            from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

            ing = input.ml_ingenio()
            x_col = input.ml_variable_x()
            zafra_sel = input.ml_zafra()
            train_size = input.ml_train_size() / 100

            datos = df_combined[
                (df_combined['ingenio_normalizado'] == ing) &
                (df_combined['zafra'] == zafra_sel)
            ].copy()

            datos = datos[['azucar_producida_total', x_col]].dropna()

            if len(datos) < 5:
                return pd.DataFrame({"Error": ["Datos insuficientes"]})

            X = datos[[x_col]].values
            y = datos['azucar_producida_total'].values

            X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=train_size, random_state=42)

            model = LinearRegression()
            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)

            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            pendiente = model.coef_[0]
            intercepto = model.intercept_
            prediccion_ejemplo = model.predict([[datos[x_col].mean()]])[0]

            return pd.DataFrame({
                "Metrica": ["R2 Score", "RMSE", "MAE", "Pendiente (coef)", "Intercepto", "R2 Entrenamiento", "Prediccion (ejemplo)"],
                "Valor": [
                    f"{r2:.4f}",
                    f"{rmse:,.2f} ton",
                    f"{mae:,.2f} ton",
                    f"{pendiente:.4f}",
                    f"{intercepto:,.2f}",
                    f"{model.score(X_train, y_train):.4f}",
                    f"{prediccion_ejemplo:,.2f} ton"
                ]
            })
        except Exception as e:
            return pd.DataFrame({"Error": [str(e)]})

    @output
    @render.image
    def grafico_regresion():
        try:
            from sklearn.linear_model import LinearRegression
            from sklearn.model_selection import train_test_split

            ing = input.ml_ingenio()
            x_col = input.ml_variable_x()
            zafra_sel = input.ml_zafra()
            train_size = input.ml_train_size() / 100

            datos = df_combined[
                (df_combined['ingenio_normalizado'] == ing) &
                (df_combined['zafra'] == zafra_sel)
            ].copy()

            datos = datos[['azucar_producida_total', x_col]].dropna()

            if len(datos) < 10:
                fig = go.Figure()
                fig.add_annotation(text="Datos insuficientes", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
                return plot_to_image(fig)

            X = datos[[x_col]].values
            y = datos['azucar_producida_total'].values

            X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=train_size, random_state=42)

            model = LinearRegression()
            model.fit(X_train, y_train)

            X_range = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
            y_range = model.predict(X_range)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=X_train.flatten(), y=y_train, mode='markers', name='Entrenamiento',
                                     marker=dict(color='#1d3557', size=8)))
            fig.add_trace(go.Scatter(x=X_test.flatten(), y=y_test, mode='markers', name='Prueba',
                                     marker=dict(color='#e63946', size=8)))
            fig.add_trace(go.Scatter(x=X_range.flatten(), y=y_range, mode='lines', name='Regresion',
                                     line=dict(color='#457b9d', width=3)))

            fig.update_layout(
                title=f"Regresion Lineal: {ing.title()}",
                xaxis_title=x_col.replace('_', ' ').title(),
                yaxis_title="Azucar Producida (ton)",
                plot_bgcolor='rgba(241,250,238,0.9)',
                paper_bgcolor='white',
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                height=400,
                width=500,
                margin=dict(l=50, r=30, t=60, b=60)
            )
            return plot_to_image(fig)
        except Exception as e:
            fig = go.Figure()
            fig.add_annotation(text=f"Error: {str(e)}", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            fig.update_layout(height=400, width=500)
            return plot_to_image(fig)

    @output
    @render.image
    def grafico_sarimax():
        try:
            from statsmodels.tsa.statespace.sarimax import SARIMAX

            zafra_sel = input.ml_zafra()
            meses = int(input.ml_train_size()) // 10

            datos_global = df_combined[df_combined['zafra'] == zafra_sel].copy()
            datos_global = datos_global.sort_values('semana_num')

            serie_global = datos_global.groupby('semana_num')['azucar_producida_total'].sum().reset_index()
            serie_global.columns = ['periodo', 'produccion']
            serie_global = serie_global.set_index('periodo')['produccion']

            if len(serie_global) < 12:
                fig = go.Figure()
                fig.add_annotation(text="Datos insuficientes para SARIMAX", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
                fig.update_layout(height=400, width=500)
                return plot_to_image(fig)

            try:
                model = SARIMAX(serie_global, order=(1, 1, 1), seasonal_order=(1, 1, 1, 4), enforce_stationarity=False, enforce_invertibility=False)
                fitted = model.fit(disp=False)
                forecast = fitted.forecast(steps=meses)
            except:
                from statsmodels.tsa.holtwinters import ExponentialSmoothing
                model_h = ExponentialSmoothing(serie_global.values, trend='add', seasonal='add', seasonal_periods=4)
                fitted_h = model_h.fit()
                forecast = fitted_h.forecast(meses)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=list(range(len(serie_global))), y=serie_global.values, mode='lines+markers', name='Historico',
                                     line=dict(color='#1d3557', width=2)))
            fig.add_trace(go.Scatter(x=list(range(len(serie_global), len(serie_global) + len(forecast))), y=forecast, mode='lines+markers', name='Pronostico SARIMAX',
                                     line=dict(color='#e63946', width=2, dash='dash')))
            fig.add_vline(x=len(serie_global)-1, line_dash="dot", line_color="#457b9d", annotation_text="Zafra Actual")

            fig.update_layout(
                title=f"Serie de Tiempo - Zafra {zafra_sel}",
                xaxis_title="Semana",
                yaxis_title="Produccion Total (ton)",
                plot_bgcolor='rgba(241,250,238,0.9)',
                paper_bgcolor='white',
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                height=400,
                width=500,
                margin=dict(l=50, r=30, t=60, b=60)
            )
            return plot_to_image(fig)
        except Exception as e:
            fig = go.Figure()
            fig.add_annotation(text=f"Error: {str(e)}", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
            fig.update_layout(height=400, width=500)
            return plot_to_image(fig)

    @output
    @render.table
    def ml_prediccion_global():
        try:
            from sklearn.linear_model import LinearRegression

            zafra_sel = input.ml_zafra()

            datos_global = df_combined[df_combined['zafra'] == zafra_sel].copy()

            resultados = []
            for ing in datos_global['ingenio_normalizado'].unique():
                datos_ing = datos_global[datos_global['ingenio_normalizado'] == ing]

                X = datos_ing[['cana_molida_neta']].dropna()
                y = datos_ing.loc[X.index, 'azucar_producida_total']

                if len(X) >= 10:
                    model = LinearRegression()
                    model.fit(X, y)

                    prediccion = model.predict(X.mean().values.reshape(1, -1))[0]
                    r2 = model.score(X, y)

                    resultados.append({
                        'Ingenio': ing.title(),
                        'R2': f"{r2:.3f}",
                        'Prediccion Prox Zafra (ton)': f"{prediccion:,.0f}",
                        'Cana Promedio (ton)': f"{X.mean().values[0]:,.0f}"
                    })

            if not resultados:
                return pd.DataFrame({"Mensaje": ["Sin datos para predecir"]})

            df_result = pd.DataFrame(resultados)
            df_result = df_result.sort_values('Prediccion Prox Zafra (ton)', ascending=False).head(20)
            return df_result
        except Exception as e:
            return pd.DataFrame({"Error": [str(e)]})

app = App(app_ui, server)