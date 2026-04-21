"""
K-Moda · Marketing Mix Modeling Dashboard
==========================================
Streamlit dashboard for K-Moda MMM project.
Run: streamlit run app.py
Requires: conda activate UAX-IA
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from pathlib import Path

# ─── CONFIGURACIÓN ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="K-Moda · Marketing Mix Modeling",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── PALETA K-MODA ───────────────────────────────────────────────────────────
KM_GOLD      = "#C8A96E"
KM_GOLD_DARK = "#8B6914"
KM_CHARCOAL  = "#2D2D2D"
KM_CREAM     = "#F7F4EF"
KM_GRAY      = "#9E9893"
KM_IVORY     = "#EDE8DC"
KM_CHANNELS  = ["#C8A96E","#8B6914","#2D2D2D","#9E9893",
                 "#D4C4A8","#6B5B3E","#B8A88A","#5C4A2A"]
KM_ACCENT    = "#D4A55A"
KM_DANGER    = "#C0392B"
KM_SUCCESS   = "#27AE60"

GROUP_LABELS = {
    "performance":        "Performance",
    "branding_digital":   "Branding Digital",
    "offline_medios":     "Offline Medios",
    "propios_y_exterior": "Propios y Exterior",
}
GROUP_COLORS = {
    "performance":        KM_CHANNELS[0],
    "branding_digital":   KM_CHANNELS[1],
    "offline_medios":     KM_CHANNELS[2],
    "propios_y_exterior": KM_CHANNELS[3],
}
CH8_LABELS = {
    "inv_paid_search":  "Paid Search",
    "inv_social_paid":  "Social Paid",
    "inv_video_online": "Video Online",
    "inv_display":      "Display",
    "inv_email_crm":    "Email / CRM",
    "inv_radio_local":  "Radio Local",
    "inv_exterior":     "Exterior",
    "inv_prensa":       "Prensa",
}

# ─── CSS PERSONALIZADO ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700;800&display=swap');

/* Global */
html, body, [class*="st-"] {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background: linear-gradient(160deg, #141414 0%, #0a0a0a 60%, #111008 100%);
    color: #E8E0D4;
}
header[data-testid="stHeader"] {
    background: rgba(10,10,10,0.95);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(200,169,110,0.1);
}

/* Sidebar collapsed */
section[data-testid="stSidebar"] {
    background: #0d0d0d;
    border-right: 1px solid rgba(200,169,110,0.12);
}

/* Top brand bar */
.brand-bar {
    display: flex;
    align-items: baseline;
    gap: 16px;
    padding: 8px 0 24px;
    border-bottom: 1px solid rgba(200,169,110,0.12);
    margin-bottom: 28px;
}
.brand-name {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-weight: 700;
    color: #C8A96E;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.brand-sub {
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #9E9893;
}

/* KPI Card */
.kpi-card {
    background: linear-gradient(145deg, rgba(200,169,110,0.06) 0%, rgba(20,20,20,0.8) 100%);
    border: 1px solid rgba(200,169,110,0.18);
    border-radius: 2px;
    padding: 24px 20px 20px;
    text-align: center;
    transition: all 0.4s ease;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #C8A96E, transparent);
    opacity: 0.6;
}
.kpi-card:hover {
    border-color: rgba(200,169,110,0.4);
    background: linear-gradient(145deg, rgba(200,169,110,0.1) 0%, rgba(25,25,15,0.9) 100%);
}
.kpi-label {
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #9E9893;
    margin-bottom: 10px;
}
.kpi-value {
    font-family: 'Playfair Display', serif;
    font-size: 34px;
    font-weight: 600;
    color: #C8A96E;
    line-height: 1.1;
}
.kpi-sub {
    font-size: 11px;
    color: #6B6560;
    margin-top: 6px;
    letter-spacing: 0.5px;
}

/* Insight card */
.insight-card {
    background: linear-gradient(135deg, rgba(139,105,20,0.08) 0%, rgba(15,15,10,0.6) 100%);
    border: 1px solid rgba(200,169,110,0.15);
    border-left: 3px solid #C8A96E;
    border-radius: 2px;
    padding: 28px 32px;
    margin: 20px 0;
}
.insight-card h3 {
    font-family: 'Playfair Display', serif !important;
    color: #C8A96E !important;
    font-size: 18px !important;
    font-weight: 600 !important;
    margin-bottom: 10px !important;
    letter-spacing: 0.5px;
}
.insight-card p {
    color: #A89880;
    font-size: 14px;
    line-height: 1.8;
}

/* Scenario card */
.scenario-card {
    background: linear-gradient(145deg, rgba(25,25,20,0.9) 0%, rgba(15,15,10,0.95) 100%);
    border: 1px solid rgba(200,169,110,0.12);
    border-radius: 2px;
    padding: 28px 24px;
    text-align: center;
    transition: all 0.4s ease;
}
.scenario-card:hover {
    border-color: rgba(200,169,110,0.35);
}
.scenario-card.highlight {
    border-color: rgba(200,169,110,0.4);
    border-top: 2px solid #C8A96E;
    background: linear-gradient(145deg, rgba(139,105,20,0.1) 0%, rgba(15,15,10,0.95) 100%);
}
.scenario-title {
    font-size: 9px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 14px;
    color: #9E9893;
}
.scenario-value {
    font-family: 'Playfair Display', serif;
    font-size: 30px;
    font-weight: 600;
    color: #C8A96E;
}
.scenario-delta {
    font-size: 12px;
    margin-top: 8px;
    letter-spacing: 0.3px;
}

/* Section headers */
.section-header {
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #C8A96E;
    border-bottom: 1px solid rgba(200,169,110,0.12);
    padding-bottom: 10px;
    margin: 40px 0 24px;
}

/* Memo */
.memo-block {
    background: linear-gradient(135deg, rgba(200,169,110,0.04) 0%, rgba(20,20,15,0.7) 100%);
    border-left: 2px solid rgba(200,169,110,0.5);
    border-radius: 0 2px 2px 0;
    padding: 28px 32px;
    margin: 20px 0;
    font-size: 14px;
    line-height: 1.9;
    color: #C0B090;
}

/* Streamlit metric */
[data-testid="stMetric"] {
    background: rgba(200,169,110,0.04);
    border: 1px solid rgba(200,169,110,0.12);
    border-radius: 2px;
    padding: 16px;
}

/* Tabs — luxury minimal */
button[data-baseweb="tab"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 2.5px !important;
    text-transform: uppercase !important;
    color: #6B6560 !important;
    padding: 12px 20px !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #C8A96E !important;
}
div[data-baseweb="tab-highlight"] {
    background-color: #C8A96E !important;
    height: 1px !important;
}
div[data-baseweb="tab-border"] {
    background-color: rgba(200,169,110,0.12) !important;
}

/* Slider */
.stSlider > div > div > div > div {
    background-color: #C8A96E !important;
}

/* Radio buttons */
.stRadio > div {
    gap: 8px;
}
.stRadio > div > label {
    font-size: 11px !important;
    letter-spacing: 1px !important;
}

/* Expander */
details {
    border: 1px solid rgba(200,169,110,0.12) !important;
    border-radius: 2px !important;
    background: rgba(15,15,10,0.6) !important;
}

/* Select box */
.stSelectbox > div > div {
    border-color: rgba(200,169,110,0.2) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: rgba(0,0,0,0.2); }
::-webkit-scrollbar-thumb { background: rgba(200,169,110,0.3); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ─── CARGA DE DATOS ──────────────────────────────────────────────────────────
DATA_DIR = Path("data/warehouse/version211")

@st.cache_data
def load_data():
    etl = pd.read_csv(DATA_DIR / "etl.csv", parse_dates=["semana_inicio"])
    dp  = pd.read_csv(DATA_DIR / "data_preparation.csv", parse_dates=["semana_inicio"])
    return etl, dp

@st.cache_resource
def load_models():
    model_data   = pickle.load(open(DATA_DIR / "elastic_net.pkl",  "rb"))
    adstock_data = pickle.load(open(DATA_DIR / "adstock_params.pkl","rb"))
    scaler_data  = pickle.load(open(DATA_DIR / "scalers.pkl",      "rb"))
    return model_data, adstock_data, scaler_data

etl, dp = load_data()
model_data, adstock_data, scaler_data = load_models()

model        = model_data["model"]
feature_cols = model_data["feature_cols"]
logadstock_cols = model_data["logadstock_cols"]
boot_coefs   = model_data["boot_coefs"]
boot_lo      = model_data["boot_lo"]
boot_hi      = model_data["boot_hi"]
contribs_eur = model_data["contribs_eur"]
pct_mkt      = model_data["pct_mkt_total"]
metrics      = model_data["metrics"]

best_params    = adstock_data["best_params"]
channel_groups = adstock_data["channel_groups"]
saturation_k   = adstock_data["saturation_k"]
inv_group_cols = adstock_data["inv_group_cols"]

scaler      = scaler_data["scaler"]
cols_scaled = scaler_data["cols_scaled"]

INV_INDIV = [c for cols in channel_groups.values() for c in cols]

# ─── FUNCIONES DE SIMULACIÓN ──────────────────────────────────────────────────
def _adstock(series, alpha, lag=0):
    x = pd.Series(series).shift(lag).fillna(0).to_numpy(dtype=float)
    out = np.zeros_like(x)
    for t in range(len(x)):
        out[t] = x[t] + (alpha * out[t-1] if t > 0 else 0.0)
    return out

def _build_X_sim(inv_nueva, n_semanas=52):
    logads_raw = np.zeros((n_semanas, len(logadstock_cols)))
    for group_col, p in best_params.items():
        logcol = f"logadstock_{group_col.replace('inv_', '')}"
        j = logadstock_cols.index(logcol)
        k = saturation_k[group_col]
        A = _adstock(np.ones(n_semanas) * inv_nueva.get(group_col, 0.0), p["alpha"], p["lag"])
        logads_raw[:, j] = np.log1p(A / k)
    rest_means = scaler.mean_[len(logadstock_cols):]
    to_scale = np.hstack([logads_raw, np.tile(rest_means, (n_semanas, 1))])
    scaled = scaler.transform(to_scale)
    X_sim = np.tile(dp[feature_cols].mean().values, (n_semanas, 1))
    for i, col in enumerate(logadstock_cols):
        X_sim[:, feature_cols.index(col)] = scaled[:, i]
    return X_sim

def simular(inv_nueva, n_semanas=52):
    X_sim = _build_X_sim(inv_nueva, n_semanas)
    ventas_anual = model.predict(X_sim).sum()
    inv_hist = {g: dp[g].mean() for g in inv_group_cols}
    ventas_hist = model.predict(_build_X_sim(inv_hist, n_semanas)).sum()
    lift_eur = ventas_anual - ventas_hist
    inv_total = sum(inv_nueva.values()) * n_semanas
    return {
        "ventas_anual_eur": ventas_anual,
        "lift_eur": lift_eur,
        "lift_pct": lift_eur / ventas_hist * 100 if ventas_hist else 0,
        "roi": lift_eur / inv_total if inv_total > 0 else 0,
        "inv_total_eur": inv_total,
    }

def simular_ic(inv_nueva, n_semanas=52):
    X_sim = _build_X_sim(inv_nueva, n_semanas)
    resultado = simular(inv_nueva, n_semanas)
    ventas_boot = [
        np.maximum(model.intercept_ + X_sim @ coefs, 0).sum()
        for coefs in boot_coefs
    ]
    resultado["ic_lo_eur"]  = np.percentile(ventas_boot, 2.5)
    resultado["ic_hi_eur"]  = np.percentile(ventas_boot, 97.5)
    resultado["riesgo_eur"] = resultado["ic_hi_eur"] - resultado["ic_lo_eur"]
    resultado["ventas_boot"] = ventas_boot
    return resultado

# ─── DATOS PRECALCULADOS ─────────────────────────────────────────────────────
inv_hist_media = {g: dp[g].mean() for g in inv_group_cols}

roi_por_grupo = {}
for grp, channels in channel_groups.items():
    inv_t = etl[channels].sum().sum()
    contrib_t = contribs_eur[f"logadstock_{grp}"].sum()
    roi_por_grupo[grp] = contrib_t / inv_t if inv_t > 0 else 0

contrib_total_grupo = {grp: contribs_eur[f"logadstock_{grp}"].sum() for grp in channel_groups}
contrib_total_marketing = sum(contrib_total_grupo.values())
ventas_totales = etl["venta_neta_total_eur"].sum()
base_total = ventas_totales - contrib_total_marketing

best_grp  = max(roi_por_grupo, key=roi_por_grupo.get)
worst_grp = min(roi_por_grupo, key=roi_por_grupo.get)
mroi_global = contrib_total_marketing / etl["inversion_total_eur"].sum()

X_full = dp[feature_cols].values
y_pred_full = model.predict(X_full)
y_actual = etl["venta_neta_total_eur"].values

n_train = int(len(etl) * 0.8)
y_train_real, y_test_real = y_actual[:n_train], y_actual[n_train:]
y_train_pred, y_test_pred = y_pred_full[:n_train], y_pred_full[n_train:]
residuos = y_actual - y_pred_full

# ─── PLOTLY LAYOUT DEFAULTS ──────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#C0B090", size=11),
    title_font=dict(color=KM_GOLD, size=14, family="Playfair Display, serif"),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(size=10, color="#9E9893"),
    ),
    xaxis=dict(gridcolor="rgba(200,169,110,0.06)", zerolinecolor="rgba(200,169,110,0.1)"),
    yaxis=dict(gridcolor="rgba(200,169,110,0.06)", zerolinecolor="rgba(200,169,110,0.1)"),
    margin=dict(t=64, b=40, l=60, r=30),
    hoverlabel=dict(bgcolor="#1a1a12", font=dict(color=KM_CREAM, size=12), bordercolor=KM_GOLD),
)

def apply_layout(fig, **kwargs):
    layout = {**PLOTLY_LAYOUT, **kwargs}
    fig.update_layout(**layout)
    return fig

def fmt_eur(v):
    if abs(v) >= 1e6:
        return f"€{v/1e6:.1f}M"
    elif abs(v) >= 1e3:
        return f"€{v/1e3:.0f}k"
    return f"€{v:.0f}"

def kpi_card(label, value, sub=""):
    sub_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    return f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {sub_html}
    </div>
    """

# ─── BRAND BAR ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="brand-bar">
    <span class="brand-name">K·Moda</span>
    <span class="brand-sub">Marketing Mix Modeling · 2020–2024</span>
</div>
""", unsafe_allow_html=True)

# ─── NAVEGACIÓN POR TABS ─────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "Resumen Ejecutivo",
    "Transparencia del Modelo",
    "Atribución por Canal",
    "Simulador Estratégico",
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — RESUMEN EJECUTIVO
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:

    # ── Filtro anual como radio horizontal ──
    years = sorted(etl["anio"].unique())
    year_opts = ["Todo el periodo"] + [str(y) for y in years]
    year_sel = st.radio(
        "Periodo de análisis",
        year_opts,
        index=0,
        horizontal=True,
        key="year_radio",
    )

    if year_sel == "Todo el periodo":
        mask = pd.Series(True, index=etl.index)
        n_weeks = len(etl)
    else:
        mask = etl["anio"] == int(year_sel)
        n_weeks = mask.sum()

    v_sel   = etl.loc[mask, "venta_neta_total_eur"].sum()
    inv_sel = etl.loc[mask, "inversion_total_eur"].sum()
    contrib_sel = sum(contribs_eur[f"logadstock_{g}"][mask.values].sum() for g in channel_groups)
    attr_pct = contrib_sel / v_sel * 100 if v_sel > 0 else 0
    mroi_sel = contrib_sel / inv_sel if inv_sel > 0 else 0

    # ── KPI Cards ──
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(kpi_card("Ventas Totales", fmt_eur(v_sel), f"{n_weeks} semanas"), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card("Inversión Medios", fmt_eur(inv_sel), f"{inv_sel/v_sel*100:.1f}% de ventas"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card("Atribuido a Marketing", f"{attr_pct:.0f}%", f"{fmt_eur(contrib_sel)} atribuidos"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_card("mROI Global", f"{mroi_sel:.1f}x", "€ ventas / € invertido"), unsafe_allow_html=True)
    with c5:
        st.markdown(kpi_card("Precisión del Modelo", f"{metrics['test_mape']:.1f}%", f"MAPE · R² = {metrics['test_r2']:.3f}"), unsafe_allow_html=True)

    st.markdown("")

    # ── mROI por canal ──
    st.markdown('<p class="section-header">Rendimiento por Canal</p>', unsafe_allow_html=True)

    mroi_data = []
    for yr in years:
        m = etl["anio"] == yr
        for grp, channels in channel_groups.items():
            inv = etl.loc[m, channels].sum().sum()
            contrib = contribs_eur[f"logadstock_{grp}"][m.values].sum()
            mroi_data.append({"Año": str(yr), "Canal": GROUP_LABELS[grp], "mROI": contrib / inv if inv > 0 else 0, "Inversión": inv, "Contribución": contrib})
    mroi_df = pd.DataFrame(mroi_data)

    col_a, col_b = st.columns(2)

    with col_a:
        fig_mroi = px.bar(
            mroi_df, x="Canal", y="mROI", color="Canal",
            animation_frame="Año",
            color_discrete_map={GROUP_LABELS[g]: GROUP_COLORS[g] for g in channel_groups},
            text_auto=".1f",
        )
        apply_layout(fig_mroi, title="mROI por canal · animado por año", yaxis_title="mROI (x)", showlegend=False, height=420)
        fig_mroi.update_traces(textposition="outside", textfont=dict(size=13, color=KM_GOLD))
        st.plotly_chart(fig_mroi, use_container_width=True)

    with col_b:
        inv_mix = []
        for yr in years:
            m = etl["anio"] == yr
            total_yr = etl.loc[m, "inversion_total_eur"].sum()
            for grp, channels in channel_groups.items():
                v = etl.loc[m, channels].sum().sum()
                inv_mix.append({"Año": str(yr), "Canal": GROUP_LABELS[grp], "Inversión €": v, "% Mix": v / total_yr * 100 if total_yr > 0 else 0})
        inv_mix_df = pd.DataFrame(inv_mix)
        fig_inv = px.bar(
            inv_mix_df, x="Canal", y="Inversión €", color="Canal",
            animation_frame="Año",
            color_discrete_map={GROUP_LABELS[g]: GROUP_COLORS[g] for g in channel_groups},
            text_auto=".2s",
        )
        apply_layout(fig_inv, title="Inversión por canal · animado por año", yaxis_title="Inversión (€)", showlegend=False, height=420)
        fig_inv.update_traces(textposition="outside", textfont=dict(size=11, color=KM_CREAM))
        st.plotly_chart(fig_inv, use_container_width=True)

    # ── Validación del Modelo ──
    st.markdown('<p class="section-header">Validación del Modelo</p>', unsafe_allow_html=True)

    tab_fit, tab_res, tab_ape = st.tabs(["Real vs Predicción", "Residuos", "Error porcentual"])

    with tab_fit:
        fig_fit = go.Figure()
        dates_all = etl["semana_inicio"]
        fig_fit.add_trace(go.Scatter(
            x=dates_all[:n_train], y=y_actual[:n_train] / 1e6,
            name="Real (Train)", mode="lines",
            line=dict(color=KM_GOLD, width=2),
        ))
        fig_fit.add_trace(go.Scatter(
            x=dates_all[n_train:], y=y_actual[n_train:] / 1e6,
            name="Real (Test)", mode="lines",
            line=dict(color=KM_GOLD, width=2, dash="dot"),
        ))
        fig_fit.add_trace(go.Scatter(
            x=dates_all[:n_train], y=y_pred_full[:n_train] / 1e6,
            name="Predicción (Train)", mode="lines",
            line=dict(color=KM_ACCENT, width=2),
        ))
        fig_fit.add_trace(go.Scatter(
            x=dates_all[n_train:], y=y_pred_full[n_train:] / 1e6,
            name="Predicción (Test)", mode="lines",
            line=dict(color=KM_SUCCESS, width=2),
        ))
        fig_fit.add_vline(x=dates_all.iloc[n_train], line=dict(color=KM_GRAY, dash="dash", width=1))
        split_y = max(y_actual) / 1e6
        fig_fit.add_annotation(
            x=dates_all.iloc[n_train], y=split_y,
            text="TRAIN", font=dict(size=9, color=KM_GRAY, family="Inter"),
            showarrow=False, xanchor="right", xshift=-8, yshift=15,
        )
        fig_fit.add_annotation(
            x=dates_all.iloc[n_train], y=split_y,
            text="TEST", font=dict(size=9, color=KM_GRAY, family="Inter"),
            showarrow=False, xanchor="left", xshift=8, yshift=15,
        )
        apply_layout(fig_fit, title="Ventas Reales vs Predicciones del Modelo", yaxis_title="Ventas (M€)", height=440)
        st.plotly_chart(fig_fit, use_container_width=True)

    with tab_res:
        colors_res = [KM_SUCCESS if r >= 0 else KM_DANGER for r in residuos]
        fig_res = go.Figure(go.Bar(
            x=dates_all, y=residuos / 1e6,
            marker_color=colors_res,
            marker_line_width=0,
            hovertemplate="Semana: %{x}<br>Residuo: €%{y:.2f}M<extra></extra>",
        ))
        apply_layout(fig_res, title="Residuos semanales (Real - Prediccion)", yaxis_title="Residuo (M€)", height=400)
        st.plotly_chart(fig_res, use_container_width=True)

    with tab_ape:
        ape = np.abs(residuos / y_actual) * 100
        fig_ape = go.Figure()
        fig_ape.add_trace(go.Scatter(
            x=dates_all, y=ape,
            mode="lines", line=dict(color=KM_GOLD, width=1.5),
            fill="tozeroy", fillcolor="rgba(200,169,110,0.08)",
            name="APE %",
        ))
        fig_ape.add_hline(y=metrics["test_mape"], line=dict(color=KM_DANGER, dash="dash", width=2),
                          annotation_text=f"MAPE test = {metrics['test_mape']:.1f}%",
                          annotation_font=dict(color=KM_DANGER, size=11))
        apply_layout(fig_ape, title="Error Porcentual Absoluto (APE) por Semana", yaxis_title="APE (%)", height=400)
        st.plotly_chart(fig_ape, use_container_width=True)

    # ── Escenarios ──
    st.markdown('<p class="section-header">Escenarios Estratégicos</p>', unsafe_allow_html=True)

    inv_baseline = {g: dp[g].mean() for g in inv_group_cols}
    inv_zero     = {g: 0.0 for g in inv_group_cols}

    canal_alto = max(roi_por_grupo, key=roi_por_grupo.get)
    canal_bajo = min(roi_por_grupo, key=roi_por_grupo.get)
    transfer = inv_baseline[f"inv_{canal_bajo}"] * 0.30
    inv_optimo = inv_baseline.copy()
    inv_optimo[f"inv_{canal_alto}"] += transfer
    inv_optimo[f"inv_{canal_bajo}"] -= transfer

    r_base = simular(inv_baseline)
    r_zero = simular(inv_zero)
    r_opt  = simular(inv_optimo)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="scenario-card">
            <div class="scenario-title">Baseline · Situacion actual</div>
            <div class="scenario-value">{fmt_eur(r_base['ventas_anual_eur'])}</div>
            <div class="scenario-delta" style="color:{KM_GRAY};">Reparto historico</div>
            <div class="scenario-delta" style="color:{KM_GRAY};">Inversion: {fmt_eur(r_base['inv_total_eur'])}/ano</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="scenario-card">
            <div class="scenario-title" style="color:{KM_DANGER};">Recorte · Sin inversion</div>
            <div class="scenario-value" style="color:{KM_DANGER};">{fmt_eur(r_zero['ventas_anual_eur'])}</div>
            <div class="scenario-delta" style="color:{KM_DANGER};">{r_zero['lift_pct']:+.0f}% vs baseline</div>
            <div class="scenario-delta" style="color:{KM_GRAY};">Sin inversion en marketing</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="scenario-card highlight">
            <div class="scenario-title" style="color:{KM_GOLD};">Optimo · Redistribucion</div>
            <div class="scenario-value">{fmt_eur(r_opt['ventas_anual_eur'])}</div>
            <div class="scenario-delta" style="color:{KM_SUCCESS};">{r_opt['lift_pct']:+.1f}% · {fmt_eur(r_opt['lift_eur'])}</div>
            <div class="scenario-delta" style="color:{KM_GRAY};">30% de {GROUP_LABELS[canal_bajo]} a {GROUP_LABELS[canal_alto]}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")

    col_esc1, col_esc2 = st.columns(2)
    with col_esc1:
        esc_names  = ["Baseline", "Sin inversion", "Optimo"]
        esc_vals   = [r_base["ventas_anual_eur"]/1e6, r_zero["ventas_anual_eur"]/1e6, r_opt["ventas_anual_eur"]/1e6]
        esc_colors = [KM_GRAY, KM_DANGER, KM_GOLD]
        fig_esc = go.Figure(go.Bar(
            x=esc_names, y=esc_vals,
            marker_color=esc_colors,
            text=[f"€{v:.0f}M" for v in esc_vals],
            textposition="outside",
            textfont=dict(color=KM_CREAM, size=14, family="Inter"),
        ))
        apply_layout(fig_esc, title="Ventas anuales por escenario (M€)", yaxis_title="Ventas (M€)", height=400, showlegend=False)
        st.plotly_chart(fig_esc, use_container_width=True)

    with col_esc2:
        inv_esc_vals = [r_base["inv_total_eur"]/1e6, 0, sum(inv_optimo.values())*52/1e6]
        mroi_esc = [
            r_base["ventas_anual_eur"] / r_base["inv_total_eur"] if r_base["inv_total_eur"] > 0 else 0,
            0,
            r_opt["ventas_anual_eur"] / (sum(inv_optimo.values())*52) if sum(inv_optimo.values()) > 0 else 0,
        ]
        fig_esc2 = make_subplots(specs=[[{"secondary_y": True}]])
        fig_esc2.add_trace(go.Bar(
            x=esc_names, y=inv_esc_vals,
            marker_color=[KM_GRAY, KM_DANGER, KM_GOLD],
            name="Inversion (M€)",
            text=[f"€{v:.1f}M" for v in inv_esc_vals],
            textposition="outside",
            textfont=dict(size=11),
        ), secondary_y=False)
        fig_esc2.add_trace(go.Scatter(
            x=esc_names, y=mroi_esc,
            mode="lines+markers+text",
            line=dict(color=KM_CREAM, width=2),
            marker=dict(size=10, color=KM_GOLD_DARK),
            name="mROI (x)",
            text=[f"{v:.1f}x" for v in mroi_esc],
            textposition="top center",
            textfont=dict(color=KM_CREAM, size=12),
        ), secondary_y=True)
        apply_layout(fig_esc2, title="Inversion vs mROI por escenario", height=400)
        fig_esc2.update_yaxes(title_text="Inversion (M€)", secondary_y=False, gridcolor="rgba(200,169,110,0.06)")
        fig_esc2.update_yaxes(title_text="mROI (x)", secondary_y=True, gridcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_esc2, use_container_width=True)

    # ── Contexto estratégico (al final, no al principio) ──
    with st.expander("Contexto estrategico — Por que Marketing Mix Modeling"):
        st.markdown("""
        <div class="insight-card">
            <h3>El problema de visibilidad</h3>
            <p>
                La desaparicion de las cookies de terceros, las restricciones de iOS 14+ y el GDPR han destruido
                la precision del modelo de atribucion por ultimo clic. K-Moda necesita un enfoque estadistico
                robusto — Marketing Mix Modeling — para medir que parte de cada euro de ventas es atribuible
                a cada canal, sin depender del rastreo individual.
            </p>
        </div>
        """, unsafe_allow_html=True)

        events = [
            ("2018-05-25", "GDPR", 95),
            ("2020-01-01", "CCPA", 85),
            ("2021-04-26", "iOS 14.5 ATT", 55),
            ("2022-06-01", "Google anuncia fin cookies", 40),
            ("2023-01-01", "DSA/DMA UE", 30),
            ("2024-01-04", "Chrome elimina 1% cookies", 20),
            ("2024-07-22", "Google pospone Privacy Sandbox", 15),
        ]
        fig_timeline = go.Figure()
        dates = [e[0] for e in events]
        labels = [e[1] for e in events]
        precisions = [e[2] for e in events]

        fig_timeline.add_trace(go.Scatter(
            x=dates, y=precisions,
            mode="lines+markers",
            line=dict(color=KM_GOLD, width=3, shape="spline"),
            marker=dict(size=10, color=KM_GOLD_DARK, line=dict(color=KM_GOLD, width=2)),
            fill="tozeroy",
            fillcolor="rgba(200,169,110,0.06)",
            hovertemplate="<b>%{text}</b><br>Precision tracking: %{y}%<extra></extra>",
            text=labels,
        ))
        for d, lbl, pr in events:
            fig_timeline.add_annotation(
                x=d, y=pr + 6, text=lbl,
                showarrow=True, arrowhead=2, arrowcolor=KM_GRAY,
                font=dict(size=9, color=KM_CREAM), bgcolor="rgba(20,20,12,0.9)",
                bordercolor=KM_GOLD, borderwidth=1, borderpad=4,
            )
        apply_layout(fig_timeline, title="Caida de la precision del tracking digital", yaxis_title="Precision estimada (%)", xaxis_title="", height=380)
        fig_timeline.update_yaxes(range=[0, 110])
        st.plotly_chart(fig_timeline, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — MODELO FINAL
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:

    st.markdown('<p class="section-header">Metricas de Calidad</p>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card("R² Train", f"{metrics['train_r2']:.3f}", "Ajuste interno"), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card("R² Test", f"{metrics['test_r2']:.3f}", "Fuera de muestra"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card("MAPE Test", f"{metrics['test_mape']:.1f}%", "Rango valido: 8-20%"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_card("Delta R² Placebo", f"+{metrics['delta_r2_placebo']:.3f}", "Señal real confirmada"), unsafe_allow_html=True)

    st.markdown("")

    # ── Especificaciones ──
    st.markdown("""
    <div class="insight-card">
        <h3>Especificaciones del Modelo</h3>
        <p>
            Algoritmo: <strong>ElasticNet</strong> con restriccion <code>positive=True</code> &mdash;
            garantiza que todos los canales tengan contribucion no negativa.<br>
            500 bootstraps por bloques · 19 features (4 logadstock + 4 Fourier + 8 calendario + 3 climaticas).
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Coeficientes ──
    st.markdown('<p class="section-header">Coeficientes del Modelo</p>', unsafe_allow_html=True)

    coef_data = []
    for feat, coef in zip(feature_cols, model.coef_):
        if coef > 0:
            is_media = feat.startswith("logadstock")
            label = feat.replace("logadstock_", "").replace("_", " ").title()
            coef_data.append({
                "Feature": label,
                "Coeficiente": coef,
                "Tipo": "Canal de Medios" if is_media else "Variable Exogena",
                "Color": KM_GOLD if is_media else KM_GRAY,
            })
    coef_df = pd.DataFrame(coef_data).sort_values("Coeficiente", ascending=True)

    fig_coef = go.Figure(go.Bar(
        y=coef_df["Feature"],
        x=coef_df["Coeficiente"],
        orientation="h",
        marker_color=coef_df["Color"],
        text=[f"€{v:,.0f}" for v in coef_df["Coeficiente"]],
        textposition="outside",
        textfont=dict(size=11, color=KM_CREAM),
        hovertemplate="<b>%{y}</b><br>b = €%{x:,.0f}/unidad<extra></extra>",
    ))
    apply_layout(fig_coef, title="Coeficientes activos del modelo (b > 0)", xaxis_title="Coeficiente (€/unidad escalada)", height=max(350, len(coef_df)*45+100))
    st.plotly_chart(fig_coef, use_container_width=True)
    st.caption("Dorado = Canales de Marketing   ·   Gris = Variables Exogenas (temperatura, festivos, etc.)")

    # ── Contribución por año animada ──
    st.markdown('<p class="section-header">Contribucion Acumulada por Año</p>', unsafe_allow_html=True)

    contrib_year = []
    for yr in sorted(etl["anio"].unique()):
        m = etl["anio"] == yr
        for grp in channel_groups:
            c = contribs_eur[f"logadstock_{grp}"][m.values].sum()
            contrib_year.append({"Año": str(yr), "Canal": GROUP_LABELS[grp], "Contribucion €": c})
    contrib_year_df = pd.DataFrame(contrib_year)

    fig_cy = px.bar(
        contrib_year_df, x="Canal", y="Contribucion €", color="Canal",
        animation_frame="Año",
        color_discrete_map={GROUP_LABELS[g]: GROUP_COLORS[g] for g in channel_groups},
        text_auto=".2s",
    )
    apply_layout(fig_cy, title="Contribucion acumulada por canal · animado por año", yaxis_title="Contribucion (€)", showlegend=False, height=420)
    fig_cy.update_traces(textposition="outside", textfont=dict(size=12, color=KM_CREAM))
    st.plotly_chart(fig_cy, use_container_width=True)

    # ── Simulador Adstock ──
    st.markdown('<p class="section-header">Simulador de Adstock · Memoria de Marca</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-card">
        <h3>¿Que es el Adstock?</h3>
        <p>
            La publicidad no desaparece al dia siguiente. El consumidor <em>recuerda</em> el anuncio
            durante varias semanas. El parametro <strong>Alpha</strong> controla cuanto dura ese recuerdo,
            y el <strong>Lag</strong> cuantas semanas tarda en hacer efecto.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_sl1, col_sl2 = st.columns(2)
    with col_sl1:
        alpha_sim = st.slider("Alpha · Decaimiento semanal", 0.05, 0.95, 0.50, 0.05, key="alpha_adstock")
    with col_sl2:
        lag_sim = st.slider("Lag · Semanas de retardo", 0, 4, 1, key="lag_adstock")

    n_weeks_sim = 20
    decay = np.array([alpha_sim**t for t in range(n_weeks_sim)])
    half_life = -np.log(2) / np.log(alpha_sim) if alpha_sim > 0 else 0

    investment_constant = 1.0
    accum = np.zeros(n_weeks_sim)
    for t in range(n_weeks_sim):
        accum[t] = investment_constant + (alpha_sim * accum[t-1] if t > 0 else 0)
    steady_state = investment_constant / (1 - alpha_sim) if alpha_sim < 1 else np.inf

    col_d, col_a = st.columns(2)
    with col_d:
        fig_decay = go.Figure()
        fig_decay.add_trace(go.Scatter(
            x=list(range(n_weeks_sim)), y=decay,
            fill="tozeroy", fillcolor="rgba(200,169,110,0.1)",
            line=dict(color=KM_GOLD, width=2.5),
            mode="lines",
            hovertemplate="Semana %{x}: %{y:.1%} del efecto<extra></extra>",
        ))
        fig_decay.add_vline(x=half_life, line=dict(color=KM_DANGER, dash="dash", width=1.5))
        fig_decay.add_annotation(x=half_life, y=0.5, text=f"Vida media: {half_life:.1f} sem",
                                 font=dict(size=10, color=KM_DANGER), showarrow=True, arrowcolor=KM_DANGER)
        apply_layout(fig_decay, title="Curva de Decaimiento", xaxis_title="Semanas despues del anuncio", yaxis_title="Efecto residual (%)", height=380)
        fig_decay.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig_decay, use_container_width=True)

    with col_a:
        fig_accum = go.Figure()
        fig_accum.add_trace(go.Scatter(
            x=list(range(n_weeks_sim)), y=accum,
            fill="tozeroy", fillcolor="rgba(139,105,20,0.12)",
            line=dict(color=KM_GOLD_DARK, width=2.5),
            mode="lines",
            hovertemplate="Semana %{x}: Adstock acum. = %{y:.2f}<extra></extra>",
        ))
        if steady_state < 50:
            fig_accum.add_hline(y=steady_state, line=dict(color=KM_CREAM, dash="dash", width=1.5))
            fig_accum.add_annotation(x=n_weeks_sim-1, y=steady_state,
                                     text=f"Estado estacionario: {steady_state:.2f}",
                                     font=dict(size=10, color=KM_CREAM), showarrow=True, arrowcolor=KM_CREAM)
        apply_layout(fig_accum, title="Curva de Acumulacion (inversion constante)", xaxis_title="Semanas de inversion constante", yaxis_title="Adstock acumulado", height=380)
        st.plotly_chart(fig_accum, use_container_width=True)

    if alpha_sim < 0.30:
        mem_desc = "**corta** — El efecto se disipa rapidamente. Ideal para promociones puntuales (Paid Search, Social Paid)."
    elif alpha_sim < 0.60:
        mem_desc = "**media** — El recuerdo dura semanas. Tipico de branding digital (Display, Video)."
    else:
        mem_desc = "**larga** — El impacto persiste mucho tiempo. Tipico de canales offline (Radio, Exterior)."

    st.info(f"Con Alpha = {alpha_sim:.2f}, la memoria de marca es {mem_desc} Vida media aprox. **{half_life:.1f} semanas**.")

    with st.expander("Formulas matematicas"):
        st.latex(r"Adstock_t = x_t + \alpha \cdot Adstock_{t-1}")
        st.latex(r"Saturacion(Adstock) = \log\!\left(1 + \frac{Adstock}{k}\right)")
        st.latex(r"\hat{y}_t = \beta_0 + \sum_{j} \beta_j \cdot Saturacion(Adstock_j)_t + \sum_{k} \gamma_k \cdot Z_{k,t}")
        st.markdown("""
        - **Alpha** = factor de decaimiento (0 = sin memoria, 1 = memoria infinita)
        - **k** = punto de saturacion (percentil 60 del adstock positivo)
        - **Beta** = coeficientes de medios (restringidos >= 0)
        - **Gamma** = coeficientes de variables de control
        """)

    # ── Inversión vs adstock por canal ──
    st.markdown('<p class="section-header">Inversion Bruta vs Señal Adstock Transformada</p>', unsafe_allow_html=True)

    canal_opts = list(GROUP_LABELS.values())
    canal_sel = st.radio(
        "Grupo de canales",
        canal_opts,
        index=0,
        horizontal=True,
        key="canal_adstock_radio",
    )
    grp_key = [k for k, v in GROUP_LABELS.items() if v == canal_sel][0]
    inv_col = f"inv_{grp_key}"
    logads_col = f"logadstock_{grp_key}"

    fig_vs = make_subplots(specs=[[{"secondary_y": True}]])
    fig_vs.add_trace(go.Bar(
        x=dp["semana_inicio"], y=dp[inv_col],
        name="Inversion bruta (€)", marker_color=KM_GRAY, opacity=0.4,
    ), secondary_y=False)
    fig_vs.add_trace(go.Scatter(
        x=dp["semana_inicio"], y=dp[logads_col],
        name="Logadstock (transformado)", line=dict(color=KM_GOLD, width=2),
    ), secondary_y=True)
    apply_layout(fig_vs, title=f"{canal_sel} · Inversion Bruta vs Señal Transformada", height=380)
    fig_vs.update_yaxes(title_text="Inversion (€)", secondary_y=False, gridcolor="rgba(200,169,110,0.06)")
    fig_vs.update_yaxes(title_text="Logadstock", secondary_y=True, gridcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_vs, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — VARIABLES Y ATRIBUCIÓN
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:

    st.markdown('<p class="section-header">Rendimiento por Canal</p>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card("Canal mas eficiente", GROUP_LABELS[best_grp], f"ROI = {roi_por_grupo[best_grp]:.1f}x"), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card("Canal menos eficiente", GROUP_LABELS[worst_grp], f"ROI = {roi_por_grupo[worst_grp]:.1f}x"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card("Contribucion total Mkt", fmt_eur(contrib_total_marketing), f"{pct_mkt:.0f}% de las ventas"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_card("mROI Global", f"{mroi_global:.1f}x", "€ contrib / € invertido"), unsafe_allow_html=True)

    st.markdown("")

    # ── Áreas apiladas ──
    st.markdown('<p class="section-header">Contribucion Semanal por Canal</p>', unsafe_allow_html=True)

    fig_stacked = go.Figure()
    for grp in channel_groups:
        fig_stacked.add_trace(go.Scatter(
            x=etl["semana_inicio"],
            y=contribs_eur[f"logadstock_{grp}"] / 1e6,
            name=GROUP_LABELS[grp],
            stackgroup="one",
            line=dict(width=0.5, color=GROUP_COLORS[grp]),
            fillcolor=GROUP_COLORS[grp],
            hovertemplate=f"{GROUP_LABELS[grp]}: €%{{y:.2f}}M<extra></extra>",
        ))
    base_weekly = model.intercept_ / 1e6
    fig_stacked.add_trace(go.Scatter(
        x=etl["semana_inicio"],
        y=[base_weekly] * len(etl),
        name="Base Organica",
        stackgroup="one",
        line=dict(width=0.5, color=KM_IVORY),
        fillcolor=KM_IVORY,
    ))
    apply_layout(fig_stacked, title="Descomposicion Semanal de Ventas", yaxis_title="Ventas (M€)", height=450)
    st.plotly_chart(fig_stacked, use_container_width=True)

    # ── Waterfall ──
    st.markdown('<p class="section-header">Cascada de Atribucion</p>', unsafe_allow_html=True)

    waterfall_items = [("Base Organica", base_total)]
    for grp in sorted(contrib_total_grupo, key=lambda g: contrib_total_grupo[g], reverse=True):
        waterfall_items.append((GROUP_LABELS[grp], contrib_total_grupo[grp]))

    wf_names = [w[0] for w in waterfall_items] + ["Total Ventas"]
    wf_values = [w[1] for w in waterfall_items] + [ventas_totales]
    wf_measures = ["absolute"] + ["relative"] * len(contrib_total_grupo) + ["total"]

    fig_wf = go.Figure(go.Waterfall(
        x=wf_names,
        y=[v / 1e6 for v in wf_values],
        measure=wf_measures,
        connector_line_color=KM_GRAY,
        connector_line_dash="dot",
        increasing_marker_color=KM_GOLD,
        decreasing_marker_color=KM_DANGER,
        totals_marker_color=KM_GOLD_DARK,
        text=[f"€{v/1e6:.0f}M" for v in wf_values],
        textposition="outside",
        textfont=dict(size=11, color=KM_CREAM),
    ))
    apply_layout(fig_wf, title="De la Base Organica al Total de Ventas", yaxis_title="M€", height=450, showlegend=False)
    st.plotly_chart(fig_wf, use_container_width=True)

    # ── ROI Ranking + Scatter ──
    st.markdown('<p class="section-header">Panel de Rendimiento</p>', unsafe_allow_html=True)

    col_roi, col_scatter = st.columns(2)

    with col_roi:
        roi_sorted = dict(sorted(roi_por_grupo.items(), key=lambda x: x[1]))
        fig_roi = go.Figure(go.Bar(
            y=[GROUP_LABELS[g] for g in roi_sorted],
            x=list(roi_sorted.values()),
            orientation="h",
            marker_color=[GROUP_COLORS[g] for g in roi_sorted],
            text=[f"{v:.1f}x" for v in roi_sorted.values()],
            textposition="outside",
            textfont=dict(size=13, color=KM_GOLD),
        ))
        apply_layout(fig_roi, title="Ranking mROI por Canal", xaxis_title="mROI (x)", height=350, showlegend=False)
        st.plotly_chart(fig_roi, use_container_width=True)

    with col_scatter:
        scatter_data = []
        for grp, channels in channel_groups.items():
            inv = etl[channels].sum().sum()
            contrib = contrib_total_grupo[grp]
            roi_v = roi_por_grupo[grp]
            scatter_data.append({
                "Canal": GROUP_LABELS[grp],
                "Inversion": inv,
                "Contribucion": contrib,
                "mROI": roi_v,
                "Color": GROUP_COLORS[grp],
            })
        sc_df = pd.DataFrame(scatter_data)
        fig_sc = go.Figure()
        for _, row in sc_df.iterrows():
            fig_sc.add_trace(go.Scatter(
                x=[row["Inversion"] / 1e6],
                y=[row["Contribucion"] / 1e6],
                mode="markers+text",
                marker=dict(size=row["mROI"] * 4 + 10, color=row["Color"], opacity=0.8,
                            line=dict(color=KM_CREAM, width=1)),
                text=[row["Canal"]],
                textposition="top center",
                textfont=dict(size=11, color=KM_CREAM),
                name=row["Canal"],
                hovertemplate=f"<b>{row['Canal']}</b><br>Inv: €{row['Inversion']/1e6:.1f}M<br>Contrib: €{row['Contribucion']/1e6:.1f}M<br>mROI: {row['mROI']:.1f}x<extra></extra>",
            ))
        apply_layout(fig_sc, title="Inversion vs Contribucion (tamano = mROI)", xaxis_title="Inversion (M€)", yaxis_title="Contribucion (M€)", height=350, showlegend=False)
        st.plotly_chart(fig_sc, use_container_width=True)

    # ── Tabla de atribución ──
    st.markdown('<p class="section-header">Tabla Completa de Atribucion</p>', unsafe_allow_html=True)

    attr_table = []
    for grp, channels in channel_groups.items():
        inv = etl[channels].sum().sum()
        contrib = contrib_total_grupo[grp]
        coef_idx = feature_cols.index(f"logadstock_{grp}")
        beta = model.coef_[coef_idx]
        boot_med = np.median(boot_coefs[:, coef_idx])
        attr_table.append({
            "Canal": GROUP_LABELS[grp],
            "Inversion (€)": f"€{inv:,.0f}",
            "Contribucion (€)": f"€{contrib:,.0f}",
            "% Atribucion": f"{contrib/ventas_totales*100:.1f}%",
            "mROI": f"{roi_por_grupo[grp]:.1f}x",
            "Beta (coef)": f"{beta:,.0f}",
            "Beta IC 95%": f"[{boot_lo[coef_idx]:,.0f} – {boot_hi[coef_idx]:,.0f}]",
        })
    attr_table.append({
        "Canal": "Base Organica",
        "Inversion (€)": "—",
        "Contribucion (€)": f"€{base_total:,.0f}",
        "% Atribucion": f"{base_total/ventas_totales*100:.1f}%",
        "mROI": "—",
        "Beta (coef)": f"{model.intercept_:,.0f}",
        "Beta IC 95%": "—",
    })
    st.dataframe(pd.DataFrame(attr_table), use_container_width=True, hide_index=True)

    # ── Donut + Barras apiladas ──
    st.markdown('<p class="section-header">Composicion de las Ventas</p>', unsafe_allow_html=True)

    col_dn, col_stk = st.columns(2)

    with col_dn:
        donut_labels = ["Base Organica"] + [GROUP_LABELS[g] for g in channel_groups]
        donut_values = [base_total] + [contrib_total_grupo[g] for g in channel_groups]
        donut_colors = [KM_IVORY] + [GROUP_COLORS[g] for g in channel_groups]
        fig_donut = go.Figure(go.Pie(
            labels=donut_labels,
            values=donut_values,
            marker=dict(colors=donut_colors, line=dict(color="rgba(0,0,0,0.3)", width=2)),
            hole=0.58,
            textinfo="label+percent",
            textfont=dict(size=11, color=KM_CHARCOAL),
            hovertemplate="<b>%{label}</b><br>%{value:,.0f} €<br>%{percent}<extra></extra>",
        ))
        fig_donut.add_annotation(text=f"<b>€{ventas_totales/1e6:.0f}M</b><br>Total",
                                 font=dict(size=16, color=KM_GOLD, family="Playfair Display, serif"),
                                 showarrow=False, x=0.5, y=0.5)
        apply_layout(fig_donut, title="Composicion: Base vs Marketing", height=420, showlegend=False)
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_stk:
        inv_year_data = []
        for yr in sorted(etl["anio"].unique()):
            m = etl["anio"] == yr
            for grp, channels in channel_groups.items():
                v = etl.loc[m, channels].sum().sum()
                inv_year_data.append({"Año": str(yr), "Canal": GROUP_LABELS[grp], "Inversion": v})
        inv_yr_df = pd.DataFrame(inv_year_data)
        fig_inv_stk = px.bar(
            inv_yr_df, x="Año", y="Inversion", color="Canal",
            color_discrete_map={GROUP_LABELS[g]: GROUP_COLORS[g] for g in channel_groups},
            barmode="stack",
            text_auto=".2s",
        )
        apply_layout(fig_inv_stk, title="Evolucion de la Inversion Anual (Apilada)", yaxis_title="Inversion (€)", height=420)
        fig_inv_stk.update_traces(textfont=dict(size=10, color=KM_CREAM))
        st.plotly_chart(fig_inv_stk, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — SIMULADOR FINAL
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:

    st.markdown('<p class="section-header">Planificador de Presupuesto What-If</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-card">
        <h3>Simulador de Escenarios</h3>
        <p>
            Redistribuye la inversion semanal entre los 4 grupos de canales y observa en tiempo real
            como cambian las ventas proyectadas, el mROI y el riesgo. El modelo calcula bootstrap con IC 95%.
        </p>
    </div>
    """, unsafe_allow_html=True)

    inv_base_ref = {g: dp[g].mean() for g in inv_group_cols}
    total_weekly_hist = sum(inv_base_ref.values())

    # ── Slider maestro ──
    st.markdown('<p class="section-header">Presupuesto Semanal</p>', unsafe_allow_html=True)

    budget_total = st.slider(
        "Presupuesto semanal total (€)",
        min_value=0,
        max_value=int(total_weekly_hist * 3),
        value=int(total_weekly_hist),
        step=1000,
        format="€%d",
        key="budget_total",
    )

    st.markdown("")
    st.markdown("**Distribucion porcentual por canal:**")

    col_s1, col_s2, col_s3, col_s4 = st.columns(4)

    pct_hist = {g: inv_base_ref[g] / total_weekly_hist * 100 for g in inv_group_cols}

    with col_s1:
        pct_perf = st.slider(f"Performance", 0, 100, int(pct_hist["inv_performance"]), key="pct_perf")
    with col_s2:
        pct_brand = st.slider(f"Branding Digital", 0, 100, int(pct_hist["inv_branding_digital"]), key="pct_brand")
    with col_s3:
        pct_off = st.slider(f"Offline Medios", 0, 100, int(pct_hist["inv_offline_medios"]), key="pct_off")
    with col_s4:
        pct_prop = st.slider(f"Propios y Exterior", 0, 100, int(pct_hist["inv_propios_y_exterior"]), key="pct_prop")

    pct_total = pct_perf + pct_brand + pct_off + pct_prop

    if pct_total == 0:
        st.warning("La suma de los porcentajes es 0%. Ajusta los sliders.")
        st.stop()

    inv_sim = {
        "inv_performance":        budget_total * (pct_perf / pct_total),
        "inv_branding_digital":   budget_total * (pct_brand / pct_total),
        "inv_offline_medios":     budget_total * (pct_off / pct_total),
        "inv_propios_y_exterior": budget_total * (pct_prop / pct_total),
    }

    if pct_total != 100:
        st.info(f"La suma de los porcentajes es **{pct_total}%**. Normalizado automaticamente a 100%.")

    # ── Simulación ──
    r_sim = simular_ic(inv_sim)
    r_ref = simular(inv_base_ref)

    lift_eur = r_sim["ventas_anual_eur"] - r_ref["ventas_anual_eur"]
    lift_pct = lift_eur / r_ref["ventas_anual_eur"] * 100 if r_ref["ventas_anual_eur"] else 0

    # ── KPIs Dinámicos ──
    st.markdown('<p class="section-header">Resultados de la Simulacion</p>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card("Ventas Proyectadas", fmt_eur(r_sim["ventas_anual_eur"]), f"IC: [{fmt_eur(r_sim['ic_lo_eur'])} – {fmt_eur(r_sim['ic_hi_eur'])}]"), unsafe_allow_html=True)
    with c2:
        delta_color = KM_SUCCESS if lift_eur >= 0 else KM_DANGER
        st.markdown(kpi_card("Lift vs Baseline", f'<span style="color:{delta_color}">{lift_pct:+.1f}%</span>', f"{fmt_eur(lift_eur)}"), unsafe_allow_html=True)
    with c3:
        mroi_sim = r_sim["ventas_anual_eur"] / r_sim["inv_total_eur"] if r_sim["inv_total_eur"] > 0 else 0
        st.markdown(kpi_card("mROI Proyectado", f"{mroi_sim:.1f}x", f"Inversion: {fmt_eur(r_sim['inv_total_eur'])}/ano"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_card("Riesgo (IC 95%)", fmt_eur(r_sim["riesgo_eur"]), "Amplitud del intervalo"), unsafe_allow_html=True)

    st.markdown("")

    # ── Panel Combinado ──
    col_sim1, col_sim2 = st.columns(2)

    with col_sim1:
        grps = list(channel_groups.keys())
        inv_vals = [inv_sim[f"inv_{g}"] * 52 / 1e6 for g in grps]
        contrib_labels = [GROUP_LABELS[g] for g in grps]

        contrib_sim_vals = []
        for g in grps:
            old_inv = inv_base_ref[f"inv_{g}"]
            new_inv = inv_sim[f"inv_{g}"]
            ratio = new_inv / old_inv if old_inv > 0 else 0
            contrib_sim_vals.append(contrib_total_grupo[g] * ratio / len(etl["anio"].unique()) / 1e6)

        mroi_per_ch = [c / i if i > 0 else 0 for c, i in zip(contrib_sim_vals, inv_vals)]

        fig_sim = make_subplots(specs=[[{"secondary_y": True}]])
        fig_sim.add_trace(go.Bar(
            x=contrib_labels, y=inv_vals, name="Inversion (M€/ano)",
            marker_color=KM_GRAY, opacity=0.6,
        ), secondary_y=False)
        fig_sim.add_trace(go.Bar(
            x=contrib_labels, y=contrib_sim_vals, name="Contribucion est. (M€/ano)",
            marker_color=KM_GOLD, opacity=0.8,
        ), secondary_y=False)
        fig_sim.add_trace(go.Scatter(
            x=contrib_labels, y=mroi_per_ch,
            mode="lines+markers+text",
            name="mROI proyectado",
            line=dict(color=KM_CREAM, width=2),
            marker=dict(size=8, color=KM_GOLD_DARK),
            text=[f"{v:.1f}x" for v in mroi_per_ch],
            textposition="top center",
            textfont=dict(size=11, color=KM_CREAM),
        ), secondary_y=True)
        apply_layout(fig_sim, title="Inversion vs Contribucion Esperada", height=420, barmode="group")
        fig_sim.update_yaxes(title_text="M€/ano", secondary_y=False, gridcolor="rgba(200,169,110,0.06)")
        fig_sim.update_yaxes(title_text="mROI (x)", secondary_y=True, gridcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_sim, use_container_width=True)

    with col_sim2:
        tm_data = []
        for g in grps:
            inv_v = inv_sim[f"inv_{g}"] * 52
            roi_v = roi_por_grupo[g]
            tm_data.append({
                "Canal": GROUP_LABELS[g],
                "Inversion": inv_v,
                "mROI": roi_v,
            })
        tm_df = pd.DataFrame(tm_data)
        fig_tm = px.treemap(
            tm_df, path=["Canal"], values="Inversion",
            color="mROI",
            color_continuous_scale=[[0, KM_CHARCOAL], [0.5, KM_GOLD_DARK], [1, KM_GOLD]],
            hover_data={"mROI": ":.1f", "Inversion": ":,.0f"},
        )
        fig_tm.update_traces(
            textinfo="label+value+percent root",
            textfont=dict(size=13, color=KM_CHARCOAL),
            marker=dict(line=dict(color="rgba(0,0,0,0.3)", width=2)),
        )
        apply_layout(fig_tm, title="Mapa de Presupuesto (tamano = inversion, color = mROI)", height=420, coloraxis_colorbar=dict(title="mROI"))
        st.plotly_chart(fig_tm, use_container_width=True)

    # ── Sensibilidad Creativa ──
    with st.expander("Laboratorio de Sensibilidad Creativa"):
        st.markdown("""
        <div class="memo-block">
            ¿Y si mejoramos la <strong>calidad creativa</strong> del anuncio? Simula un aumento del coeficiente Beta
            para estimar el impacto de una mejor agencia, mejor copy, o mejor produccion.
        </div>
        """, unsafe_allow_html=True)

        sens_canal = st.radio(
            "Canal a modificar",
            list(GROUP_LABELS.values()),
            horizontal=True,
            key="sens_canal_radio",
        )
        sens_key = [k for k, v in GROUP_LABELS.items() if v == sens_canal][0]
        sens_pct = st.slider("Mejora del rendimiento creativo (%)", -30, 50, 10, 5, key="sens_pct")

        coef_idx = feature_cols.index(f"logadstock_{sens_key}")
        beta_base = model.coef_[coef_idx]
        beta_new = beta_base * (1 + sens_pct / 100)
        contrib_canal = contrib_total_grupo[sens_key]
        delta_year = contrib_canal * (sens_pct / 100) / len(etl["anio"].unique())

        if sens_pct > 0:
            st.success(f"Una mejora creativa del +{sens_pct}% en **{sens_canal}** podria generar **+{fmt_eur(delta_year)}** adicionales por ano (estimacion lineal).")
        elif sens_pct < 0:
            st.error(f"Una caida creativa del {sens_pct}% en **{sens_canal}** costaria **{fmt_eur(delta_year)}** por ano.")
        else:
            st.info("Sin cambio en el rendimiento creativo.")

    # ── Escenarios predefinidos ──
    st.markdown('<p class="section-header">Escenarios Estrategicos Predefinidos</p>', unsafe_allow_html=True)

    inv_base_esc = {g: dp[g].mean() for g in inv_group_cols}

    inv_conservador = inv_base_esc.copy()
    inv_conservador[f"inv_{best_grp}"]  *= 1.10
    inv_conservador[f"inv_{worst_grp}"] *= 0.90

    inv_optimo_esc = inv_base_esc.copy()
    transfer_opt = inv_base_esc[f"inv_{worst_grp}"] * 0.30
    inv_optimo_esc[f"inv_{best_grp}"]  += transfer_opt
    inv_optimo_esc[f"inv_{worst_grp}"] -= transfer_opt

    inv_recorte = {g: v * 0.50 for g, v in inv_base_esc.items()}

    escenarios = {
        "Baseline":      (inv_base_esc,   "Reparto historico sin cambios"),
        "Recorte -50%":  (inv_recorte,    "Reduccion del 50% en todos los canales"),
        "Conservador":   (inv_conservador, f"+10% {GROUP_LABELS[best_grp]}, -10% {GROUP_LABELS[worst_grp]}"),
        "Optimo":        (inv_optimo_esc,  f"30% de {GROUP_LABELS[worst_grp]} hacia {GROUP_LABELS[best_grp]}"),
    }

    esc_results = {}
    for name, (inv, desc) in escenarios.items():
        esc_results[name] = simular(inv)
        esc_results[name]["desc"] = desc
        esc_results[name]["inv"] = inv

    cols_esc = st.columns(4)
    esc_colors_card = [KM_GRAY, KM_DANGER, KM_GOLD_DARK, KM_GOLD]
    esc_highlight = ["", "", "", "highlight"]

    for i, (name, esc_r) in enumerate(esc_results.items()):
        lift = esc_r["ventas_anual_eur"] - esc_results["Baseline"]["ventas_anual_eur"]
        lift_p = lift / esc_results["Baseline"]["ventas_anual_eur"] * 100 if esc_results["Baseline"]["ventas_anual_eur"] else 0
        delta_color = KM_SUCCESS if lift >= 0 else KM_DANGER

        with cols_esc[i]:
            st.markdown(f"""
            <div class="scenario-card {esc_highlight[i]}">
                <div class="scenario-title" style="color:{esc_colors_card[i]};">{name}</div>
                <div class="scenario-value">{fmt_eur(esc_r['ventas_anual_eur'])}</div>
                <div class="scenario-delta" style="color:{delta_color};">{lift_p:+.1f}% · {fmt_eur(lift)}</div>
                <div class="scenario-delta" style="color:{KM_GRAY}; font-size:11px; margin-top:8px;">{esc_r['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")

    # ── Donuts ──
    st.markdown('<p class="section-header">Distribucion del Presupuesto por Escenario</p>', unsafe_allow_html=True)

    donut_escs = ["Baseline", "Conservador", "Optimo"]
    cols_donut = st.columns(3)

    for i, esc_name in enumerate(donut_escs):
        inv_e = esc_results[esc_name]["inv"]
        labels = [GROUP_LABELS[g.replace("inv_", "")] for g in inv_e]
        values = list(inv_e.values())
        colors = [GROUP_COLORS[g.replace("inv_", "")] for g in inv_e]

        fig_dn = go.Figure(go.Pie(
            labels=labels, values=values,
            marker=dict(colors=colors, line=dict(color="rgba(0,0,0,0.3)", width=2)),
            hole=0.52,
            textinfo="percent",
            textfont=dict(size=11, color=KM_CHARCOAL),
        ))
        total_wk = sum(values)
        fig_dn.add_annotation(
            text=f"€{total_wk:,.0f}<br>/semana",
            font=dict(size=11, color=KM_GOLD, family="Playfair Display, serif"),
            showarrow=False,
        )
        apply_layout(fig_dn, title=esc_name, height=340, showlegend=(i == 0))
        with cols_donut[i]:
            st.plotly_chart(fig_dn, use_container_width=True)

    # ── Tabla de distribución ──
    st.markdown('<p class="section-header">Tabla Comparativa de Distribucion</p>', unsafe_allow_html=True)

    dist_table = []
    for g in inv_group_cols:
        row = {"Canal": GROUP_LABELS[g.replace("inv_", "")]}
        for esc_name in escenarios:
            inv_e = esc_results[esc_name]["inv"]
            total_e = sum(inv_e.values())
            row[f"{esc_name} (€/sem)"] = f"€{inv_e[g]:,.0f}"
            row[f"{esc_name} (%)"] = f"{inv_e[g]/total_e*100:.0f}%" if total_e > 0 else "—"
        dist_table.append(row)
    st.dataframe(pd.DataFrame(dist_table), use_container_width=True, hide_index=True)

    # ── Informe Ejecutivo ──
    st.markdown('<p class="section-header">Informe Ejecutivo Generado</p>', unsafe_allow_html=True)

    best_esc_name = max(esc_results, key=lambda k: esc_results[k]["ventas_anual_eur"])
    best_esc = esc_results[best_esc_name]
    baseline_ventas = esc_results["Baseline"]["ventas_anual_eur"]
    best_lift = best_esc["ventas_anual_eur"] - baseline_ventas
    best_lift_pct = best_lift / baseline_ventas * 100

    st.markdown(f"""
    <div class="memo-block">
        <p style="font-weight:700; color:{KM_GOLD}; font-size:15px; letter-spacing:1px; margin-bottom:16px; text-transform:uppercase;">
            Memorandum — Comite de Direccion K-Moda
        </p>
        <p><strong>Asunto:</strong> Recomendacion de redistribucion presupuestaria basada en Marketing Mix Modeling</p>
        <p><strong>Datos:</strong> 2020–2024 · 258 semanas de actividad comercial</p>
        <hr style="border-color:rgba(200,169,110,0.15); margin:16px 0;">
        <p>
            El modelo MMM (ElasticNet, R² test = {metrics['test_r2']:.3f}, MAPE = {metrics['test_mape']:.1f}%)
            confirma que el <strong>{pct_mkt:.0f}% de las ventas</strong> es atribuible al marketing, con un
            retorno global de <strong>{mroi_global:.1f}x</strong>.
        </p>
        <p>
            El canal mas eficiente es <strong>{GROUP_LABELS[best_grp]}</strong> (ROI = {roi_por_grupo[best_grp]:.1f}x),
            mientras que <strong>{GROUP_LABELS[worst_grp]}</strong> presenta el menor retorno ({roi_por_grupo[worst_grp]:.1f}x).
        </p>
        <p>
            La simulacion del escenario <strong>{best_esc_name}</strong> proyecta ventas anuales de
            <strong>{fmt_eur(best_esc['ventas_anual_eur'])}</strong>, lo que supone un incremento de
            <strong>{best_lift_pct:+.1f}% ({fmt_eur(best_lift)})</strong> respecto al reparto actual,
            sin incrementar el presupuesto total.
        </p>
        <p style="margin-top:16px; font-weight:600; color:{KM_GOLD}; letter-spacing:0.5px;">
            Recomendacion: Aprobar la redistribucion presupuestaria del escenario {best_esc_name} para el proximo ejercicio fiscal.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="margin-top:60px; padding-top:24px; border-top:1px solid rgba(200,169,110,0.1);
            display:flex; justify-content:space-between; align-items:center;">
    <span style="font-family:'Playfair Display',serif; color:#C8A96E; font-size:14px; letter-spacing:2px;">K·MODA</span>
    <span style="font-size:10px; color:#6B6560; letter-spacing:1px;">
        258 semanas · 2020–2024 &nbsp;·&nbsp; ElasticNet MMM &nbsp;·&nbsp;
        R² = {metrics['test_r2']:.3f} &nbsp;·&nbsp; MAPE = {metrics['test_mape']:.1f}%
    </span>
</div>
""", unsafe_allow_html=True)
