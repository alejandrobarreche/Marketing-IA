"""
K-Moda · Marketing Mix Modeling Dashboard
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from pathlib import Path

st.set_page_config(
    page_title="K-Moda · MMM",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

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

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, .stApp, .stApp [class*="st-"] { font-family: 'Inter', sans-serif; }
.stApp [data-testid="stIconMaterial"],
.stApp span.material-symbols-rounded,
.stApp span.material-symbols-outlined {
    font-family: 'Material Symbols Rounded', 'Material Symbols Outlined' !important;
}
.stApp {
    background:
        radial-gradient(ellipse 120% 80% at 20% 0%, rgba(200,169,110,0.05) 0%, rgba(0,0,0,0) 55%),
        radial-gradient(ellipse 90% 60% at 85% 100%, rgba(139,105,20,0.04) 0%, rgba(0,0,0,0) 50%),
        linear-gradient(178deg, #17150f 0%, #0d0b08 55%, #0a0907 100%);
    color: #E8E0D4;
}
.stApp::before {
    content: ""; position: fixed; inset: 0; pointer-events: none; z-index: 0;
    background-image:
        linear-gradient(rgba(200,169,110,0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(200,169,110,0.025) 1px, transparent 1px);
    background-size: 48px 48px;
    mask-image: radial-gradient(ellipse 70% 60% at 50% 40%, #000 0%, transparent 80%);
}
header[data-testid="stHeader"] {
    background: rgba(10,10,10,0.95);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(200,169,110,0.1);
}
section[data-testid="stSidebar"] {
    background: #0d0d0d;
    border-right: 1px solid rgba(200,169,110,0.12);
}
.brand-bar {
    display: flex; align-items: baseline; gap: 16px;
    padding: 8px 0 24px;
    border-bottom: 1px solid rgba(200,169,110,0.12);
    margin-bottom: 28px;
}
.brand-name {
    font-family: 'Playfair Display', serif;
    font-size: 28px; font-weight: 700; color: #C8A96E;
    letter-spacing: 2px; text-transform: uppercase;
}
.brand-sub {
    font-size: 11px; font-weight: 500;
    letter-spacing: 3px; text-transform: uppercase; color: #9E9893;
}
.kpi-card {
    background: linear-gradient(145deg, rgba(200,169,110,0.06) 0%, rgba(20,20,20,0.8) 100%);
    border: 1px solid rgba(200,169,110,0.18); border-radius: 2px;
    padding: 24px 20px 20px; text-align: center;
    position: relative; overflow: hidden;
}
.kpi-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, #C8A96E, transparent); opacity: 0.6;
}
.kpi-label { font-size: 9px; font-weight: 700; letter-spacing: 2.5px; text-transform: uppercase; color: #9E9893; margin-bottom: 10px; }
.kpi-value { font-family: 'Playfair Display', serif; font-size: 34px; font-weight: 600; color: #C8A96E; line-height: 1.1; }
.kpi-sub { font-size: 11px; color: #6B6560; margin-top: 6px; letter-spacing: 0.5px; }
.insight-card {
    background: linear-gradient(135deg, rgba(139,105,20,0.08) 0%, rgba(15,15,10,0.6) 100%);
    border: 1px solid rgba(200,169,110,0.15); border-left: 3px solid #C8A96E;
    border-radius: 2px; padding: 20px 24px; margin: 12px 0;
}
.insight-card h3 { font-family: 'Playfair Display', serif !important; color: #C8A96E !important; font-size: 16px !important; font-weight: 600 !important; margin-bottom: 8px !important; }
.insight-card p { color: #A89880; font-size: 13px; line-height: 1.7; margin: 0; }
.chart-caption { font-size: 12px; color: #7A7268; padding: 4px 0 20px; line-height: 1.6; }
.section-header {
    font-size: 9px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase;
    color: #C8A96E; border-bottom: 1px solid rgba(200,169,110,0.12);
    padding-bottom: 10px; margin: 40px 0 24px;
}
@keyframes pulseBadge {
    0%   { box-shadow: 0 0 0 0 rgba(200,169,110,0.55); transform: translateY(-1px) scale(1); }
    70%  { box-shadow: 0 0 0 10px rgba(200,169,110,0);   transform: translateY(-1px) scale(1.04); }
    100% { box-shadow: 0 0 0 0 rgba(200,169,110,0);      transform: translateY(-1px) scale(1); }
}
.play-badge {
    display: inline-block; margin-left: 14px;
    padding: 3px 10px; border-radius: 12px;
    background: linear-gradient(90deg, #C8A96E 0%, #8B6914 100%);
    color: #0a0907 !important;
    font-size: 9px; font-weight: 800; letter-spacing: 1.8px;
    animation: pulseBadge 1.8s infinite;
    vertical-align: middle;
}
.scenario-card {
    background: linear-gradient(145deg, rgba(25,25,20,0.9) 0%, rgba(15,15,10,0.95) 100%);
    border: 1px solid rgba(200,169,110,0.12); border-radius: 2px;
    padding: 22px 18px; text-align: center;
}
.scenario-card.highlight {
    border-color: rgba(200,169,110,0.4); border-top: 2px solid #C8A96E;
    background: linear-gradient(145deg, rgba(139,105,20,0.1) 0%, rgba(15,15,10,0.95) 100%);
}
.scenario-title { font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 12px; color: #9E9893; }
.scenario-value { font-family: 'Playfair Display', serif; font-size: 26px; font-weight: 600; color: #C8A96E; }
.scenario-delta { font-size: 12px; margin-top: 6px; letter-spacing: 0.3px; }
.memo-block {
    background: linear-gradient(135deg, rgba(200,169,110,0.04) 0%, rgba(20,20,15,0.7) 100%);
    border-left: 2px solid rgba(200,169,110,0.5); border-radius: 0 2px 2px 0;
    padding: 24px 28px; margin: 16px 0; font-size: 14px; line-height: 1.9; color: #C0B090;
}
[data-testid="stMetric"] { background: rgba(200,169,110,0.04); border: 1px solid rgba(200,169,110,0.12); border-radius: 2px; padding: 16px; }
button[data-baseweb="tab"] { font-family: 'Inter', sans-serif !important; font-size: 10px !important; font-weight: 700 !important; letter-spacing: 2.5px !important; text-transform: uppercase !important; color: #6B6560 !important; padding: 12px 20px !important; }
button[data-baseweb="tab"][aria-selected="true"] { color: #C8A96E !important; }
div[data-baseweb="tab-highlight"] { background-color: #C8A96E !important; height: 1px !important; }
div[data-baseweb="tab-border"] { background-color: rgba(200,169,110,0.12) !important; }
.stSlider > div > div > div > div { background-color: #C8A96E !important; }
details { border: 1px solid rgba(200,169,110,0.12) !important; border-radius: 2px !important; background: rgba(15,15,10,0.6) !important; }
.stSelectbox > div > div { border-color: rgba(200,169,110,0.2) !important; }
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: rgba(0,0,0,0.2); }
::-webkit-scrollbar-thumb { background: rgba(200,169,110,0.3); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ─── CARGA DE DATOS ──────────────────────────────────────────────────────────
DATA_DIR = Path("data/warehouse/version1")

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

model           = model_data["model"]
feature_cols    = model_data["feature_cols"]
logadstock_cols = model_data["logadstock_cols"]
boot_coefs      = model_data["boot_coefs"]
boot_lo         = model_data["boot_lo"]
boot_hi         = model_data["boot_hi"]
contribs_eur    = model_data["contribs_eur"]
pct_mkt         = model_data["pct_mkt_total"]
metrics         = model_data["metrics"]

best_params    = adstock_data["best_params"]
channel_groups = adstock_data["channel_groups"]
saturation_k   = adstock_data["saturation_k"]
inv_group_cols = adstock_data["inv_group_cols"]

scaler      = scaler_data["scaler"]
cols_scaled = scaler_data["cols_scaled"]

# ─── SIMULACIÓN ──────────────────────────────────────────────────────────────
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
    resultado["ic_lo_eur"]   = np.percentile(ventas_boot, 2.5)
    resultado["ic_hi_eur"]   = np.percentile(ventas_boot, 97.5)
    resultado["riesgo_eur"]  = resultado["ic_hi_eur"] - resultado["ic_lo_eur"]
    resultado["ventas_boot"] = ventas_boot
    return resultado

# ─── PRECÓMPUTOS BÁSICOS ─────────────────────────────────────────────────────
inv_hist_media = {g: dp[g].mean() for g in inv_group_cols}

roi_por_grupo = {}
for grp, channels in channel_groups.items():
    inv_t     = etl[channels].sum().sum()
    contrib_t = contribs_eur[f"logadstock_{grp}"].sum()
    roi_por_grupo[grp] = contrib_t / inv_t if inv_t > 0 else 0

contrib_total_grupo     = {grp: contribs_eur[f"logadstock_{grp}"].sum() for grp in channel_groups}
contrib_total_marketing = sum(contrib_total_grupo.values())
ventas_totales          = etl["venta_neta_total_eur"].sum()
base_total              = ventas_totales - contrib_total_marketing

best_grp    = max(roi_por_grupo, key=roi_por_grupo.get)
worst_grp   = min(roi_por_grupo, key=roi_por_grupo.get)
mroi_global = contrib_total_marketing / etl["inversion_total_eur"].sum()

X_full      = dp[feature_cols].values
y_pred_full = model.predict(X_full)
y_actual    = etl["venta_neta_total_eur"].values
n_train     = int(len(etl) * 0.8)
residuos    = y_actual - y_pred_full
years       = sorted(etl["anio"].unique())

# Base orgánica semanal (coherente con notebook 5): predicción − Σ contribuciones de medios
mkt_weekly  = np.zeros(len(etl))
for grp in channel_groups:
    mkt_weekly += np.asarray(contribs_eur[f"logadstock_{grp}"])
base_weekly = np.maximum(y_pred_full - mkt_weekly, 0)

# ─── PRECÓMPUTOS NUEVOS (cached) ─────────────────────────────────────────────

@st.cache_data
def _compute_landscape(n=350):
    np.random.seed(42)
    n_ch     = len(inv_group_cols)
    base_wk  = sum(inv_hist_media.values())
    factors  = np.concatenate([np.linspace(0.25, 2.8, n // 2),
                               np.random.uniform(0.25, 2.8, n - n // 2)])
    np.random.shuffle(factors)
    allocs   = np.random.dirichlet(np.ones(n_ch) * 0.6, n)
    rows = []
    for bf, alloc in zip(factors, allocs):
        total_wk = base_wk * bf
        inv = {g: total_wk * a for g, a in zip(inv_group_cols, alloc)}
        r = simular(inv)
        dom_idx = int(np.argmax(alloc))
        dom_key = inv_group_cols[dom_idx].replace("inv_", "")
        rows.append({
            "inv_anual": r["inv_total_eur"],
            "ventas":    r["ventas_anual_eur"],
            "canal_dom": GROUP_LABELS.get(dom_key, dom_key),
        })
    return pd.DataFrame(rows)

@st.cache_data
def _compute_saturation(n_pts=55):
    curves = {}
    for grp in inv_group_cols:
        hist_val  = inv_hist_media[grp]
        max_val   = max(hist_val * 5, 2000)
        inv_range = np.linspace(0, max_val, n_pts)
        revenues  = []
        for v in inv_range:
            inv_t = {g: inv_hist_media[g] for g in inv_group_cols}
            inv_t[grp] = v
            revenues.append(simular(inv_t)["ventas_anual_eur"])
        curves[grp] = (inv_range, np.array(revenues))
    return curves

def _compute_tornado(delta_pct=10):
    r_base = simular(inv_hist_media)["ventas_anual_eur"]
    up, dn = {}, {}
    for g in inv_group_cols:
        inv_up = {k: v for k, v in inv_hist_media.items()}
        inv_dn = {k: v for k, v in inv_hist_media.items()}
        inv_up[g] *= 1 + delta_pct / 100
        inv_dn[g] *= 1 - delta_pct / 100
        up[g] = simular(inv_up)["ventas_anual_eur"] - r_base
        dn[g] = simular(inv_dn)["ventas_anual_eur"] - r_base
    return up, dn

landscape_df      = _compute_landscape()
saturation_curves = _compute_saturation()
tornado_up, tornado_dn = _compute_tornado()

# ─── UTILS ───────────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#C0B090", size=11),
    title_font=dict(color=KM_GOLD, size=14, family="Playfair Display, serif"),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10, color="#9E9893")),
    xaxis=dict(gridcolor="rgba(200,169,110,0.06)", zerolinecolor="rgba(200,169,110,0.1)"),
    yaxis=dict(gridcolor="rgba(200,169,110,0.06)", zerolinecolor="rgba(200,169,110,0.1)"),
    margin=dict(t=64, b=40, l=60, r=30),
    hoverlabel=dict(bgcolor="#1a1a12", font=dict(color=KM_CREAM, size=12), bordercolor=KM_GOLD),
)

def apply_layout(fig, **kwargs):
    fig.update_layout(**{**PLOTLY_LAYOUT, **kwargs})
    return fig

def fmt_eur(v):
    if abs(v) >= 1e6: return f"€{v/1e6:.1f}M"
    if abs(v) >= 1e3: return f"€{v/1e3:.0f}k"
    return f"€{v:.0f}"

def kpi_card(label, value, sub=""):
    sub_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    return f'<div class="kpi-card"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div>{sub_html}</div>'

def caption(text):
    return f'<p class="chart-caption">{text}</p>'

def animated_header(title, label="▶ INTERACTIVO · pulsa Play"):
    return (f'<p class="section-header">{title}'
            f'<span class="play-badge">{label}</span></p>')

def play_button(play_label="▶ Play", stop_label="■ Stop", duration=80, **pos):
    """Botón Play/Stop destacado (fondo dorado). pos override: x, y, xanchor, yanchor."""
    defaults = dict(x=0.02, y=0.02, xanchor="left", yanchor="bottom")
    defaults.update(pos)
    return dict(
        type="buttons", showactive=False, direction="left",
        pad=dict(r=6, t=6, b=6, l=6),
        bgcolor=KM_GOLD, bordercolor=KM_CREAM, borderwidth=2,
        font=dict(color="#0a0907", size=13, family="Inter"),
        buttons=[
            dict(label=f"  {play_label}  ", method="animate",
                 args=[None, dict(frame=dict(duration=duration, redraw=True),
                                  fromcurrent=True, transition=dict(duration=0))]),
            dict(label=f"  {stop_label}  ", method="animate",
                 args=[[None], dict(frame=dict(duration=0, redraw=False),
                                    mode="immediate", transition=dict(duration=0))]),
        ],
        **defaults,
    )

def play_hint_annotation(text="⚡ Pulsa ▶ Play para animar", **pos):
    defaults = dict(x=0.5, y=1.08, xref="paper", yref="paper",
                    xanchor="center", yanchor="bottom")
    defaults.update(pos)
    return dict(
        text=f"<b>{text}</b>", showarrow=False,
        font=dict(color=KM_GOLD, size=12),
        bgcolor="rgba(200,169,110,0.08)",
        bordercolor=KM_GOLD, borderwidth=1, borderpad=6,
        **defaults,
    )

# ─── BRAND BAR ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="brand-bar">
    <span class="brand-name">K·Moda</span>
    <span class="brand-sub">Marketing Mix Modeling · 2020–2024</span>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "Visión General",
    "Canales y Atribución",
    "Laboratorio de Inversión",
    "El Modelo",
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — VISIÓN GENERAL
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:

    year_opts = ["Todo el periodo"] + [str(y) for y in years]
    year_sel  = st.radio("Periodo", year_opts, index=0, horizontal=True, key="yr_t1")

    if year_sel == "Todo el periodo":
        mask    = pd.Series(True, index=etl.index)
        n_weeks = len(etl)
    else:
        mask    = etl["anio"] == int(year_sel)
        n_weeks = mask.sum()

    v_sel       = etl.loc[mask, "venta_neta_total_eur"].sum()
    inv_sel     = etl.loc[mask, "inversion_total_eur"].sum()
    contrib_sel = sum(contribs_eur[f"logadstock_{g}"][mask.values].sum() for g in channel_groups)
    attr_pct    = contrib_sel / v_sel * 100 if v_sel > 0 else 0
    mroi_sel    = contrib_sel / inv_sel if inv_sel > 0 else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.markdown(kpi_card("Ventas Totales", fmt_eur(v_sel), f"{n_weeks} semanas"), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("Inversión en Medios", fmt_eur(inv_sel), f"{inv_sel/v_sel*100:.1f}% de ventas"), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("Atribuido a Marketing", f"{attr_pct:.0f}%", fmt_eur(contrib_sel)), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("mROI Global", f"{mroi_sel:.1f}x", "€ ventas / € invertido"), unsafe_allow_html=True)
    with c5: st.markdown(kpi_card("Precisión Modelo", f"{metrics['test_mape']:.1f}%", f"MAPE · R²={metrics['test_r2']:.3f}"), unsafe_allow_html=True)

    st.markdown("")

    # ── HERO: narrativa de ventas con contribución de marketing ──
    st.markdown('<p class="section-header">Ventas, Marketing y Base Orgánica · Una Historia</p>', unsafe_allow_html=True)

    dates_h  = etl["semana_inicio"]
    ventas_h = y_actual / 1e6
    base_h   = base_weekly / 1e6
    mkt_h    = mkt_weekly  / 1e6

    fig_hero = go.Figure()
    fig_hero.add_trace(go.Scatter(
        x=dates_h, y=base_h, mode="lines", name="Base orgánica",
        line=dict(color="rgba(237,232,220,0.35)", width=0.6), stackgroup="one",
        fillcolor="rgba(237,232,220,0.10)",
        hovertemplate="Base: €%{y:.2f}M<extra></extra>",
    ))
    fig_hero.add_trace(go.Scatter(
        x=dates_h, y=mkt_h, mode="lines", name="Marketing (atribuido)",
        line=dict(color=KM_GOLD, width=0.6), stackgroup="one",
        fillcolor="rgba(200,169,110,0.28)",
        hovertemplate="Marketing: €%{y:.2f}M<extra></extra>",
    ))
    fig_hero.add_trace(go.Scatter(
        x=dates_h, y=ventas_h, mode="lines", name="Ventas reales",
        line=dict(color=KM_CREAM, width=1.8),
        hovertemplate="Ventas: €%{y:.2f}M<extra></extra>",
    ))
    # Anotación de lectura rápida
    peak_idx = int(np.argmax(ventas_h))
    fig_hero.add_annotation(
        x=dates_h.iloc[peak_idx], y=ventas_h[peak_idx],
        text=f"pico · €{ventas_h[peak_idx]:.1f}M",
        font=dict(color=KM_GOLD, size=10), showarrow=False,
        yshift=14, bgcolor="rgba(10,10,10,0.6)", bordercolor=KM_GOLD, borderwidth=1, borderpad=4,
    )
    apply_layout(fig_hero,
                 title="Ventas semanales · capa dorada = marketing atribuido",
                 yaxis_title="Ventas (M€ / semana)", height=420,
                 hovermode="x unified",
                 legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                             bgcolor="rgba(0,0,0,0)", font=dict(size=10, color="#9E9893")))
    st.plotly_chart(fig_hero, width="stretch")

    st.markdown(caption(
        f"Cada semana, la capa <b style='color:{KM_GOLD}'>dorada</b> representa cuánto de las ventas "
        f"se explica por inversión publicitaria. El resto ({base_total/ventas_totales*100:.0f}%) "
        f"es base orgánica: SEO, recurrencia y fuerza de marca. "
        f"Sobre 2020-2024 el marketing explica el <b>{pct_mkt:.0f}%</b> de las ventas con mROI <b>{mroi_global:.1f}x</b>."
    ), unsafe_allow_html=True)

    # ── Hélice cilíndrica: base = año (12 meses), altura = tiempo, deformación radial = ventas ──
    st.markdown(animated_header("Hélice de Ventas · 2020–2024"), unsafe_allow_html=True)

    dates_cyl = pd.to_datetime(etl["semana_inicio"]).reset_index(drop=True)
    ventas_cyl = np.asarray(etl["venta_neta_total_eur"].values, dtype=float)
    n_w = len(dates_cyl)

    iso = dates_cyl.dt.isocalendar()
    week_of_year = iso["week"].to_numpy().astype(float)
    year_arr = iso["year"].to_numpy()
    years_sorted = np.sort(np.unique(year_arr))
    year_idx = np.searchsorted(years_sorted, year_arr).astype(float)

    theta = 2 * np.pi * (week_of_year - 1) / 52.0
    z_line = year_idx + (week_of_year - 1) / 52.0

    v_min, v_max = float(ventas_cyl.min()), float(ventas_cyl.max())
    v_norm = (ventas_cyl - v_min) / (v_max - v_min + 1e-9)
    R_BASE, R_AMP = 0.6, 0.95
    r_line = R_BASE + R_AMP * v_norm

    x_line = r_line * np.cos(theta)
    y_line = r_line * np.sin(theta)

    # Cilindro de referencia (wireframe)
    n_rings = len(years_sorted) + 1
    theta_ring = np.linspace(0, 2 * np.pi, 80)
    ring_x = R_BASE * np.cos(theta_ring)
    ring_y = R_BASE * np.sin(theta_ring)

    fig_cyl = go.Figure()
    for k in range(n_rings):
        fig_cyl.add_trace(go.Scatter3d(
            x=ring_x, y=ring_y, z=np.full_like(ring_x, float(k)),
            mode="lines",
            line=dict(color="rgba(200,169,110,0.18)", width=1),
            hoverinfo="skip", showlegend=False,
        ))
    # Rayos verticales marcando meses
    for m in range(12):
        ang = 2 * np.pi * m / 12
        fig_cyl.add_trace(go.Scatter3d(
            x=[R_BASE * np.cos(ang)] * 2,
            y=[R_BASE * np.sin(ang)] * 2,
            z=[0, float(n_rings - 1)],
            mode="lines",
            line=dict(color="rgba(200,169,110,0.10)", width=1),
            hoverinfo="skip", showlegend=False,
        ))
    # Etiquetas de meses
    meses_lbl = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
    fig_cyl.add_trace(go.Scatter3d(
        x=[(R_BASE + R_AMP + 0.15) * np.cos(2*np.pi*m/12) for m in range(12)],
        y=[(R_BASE + R_AMP + 0.15) * np.sin(2*np.pi*m/12) for m in range(12)],
        z=[float(n_rings - 1) + 0.15] * 12,
        mode="text", text=meses_lbl,
        textfont=dict(color=KM_GRAY, size=10),
        hoverinfo="skip", showlegend=False,
    ))
    # Etiquetas de años
    fig_cyl.add_trace(go.Scatter3d(
        x=[R_BASE + R_AMP + 0.3] * len(years_sorted),
        y=[0.0] * len(years_sorted),
        z=[float(k) for k in range(len(years_sorted))],
        mode="text", text=[str(y) for y in years_sorted],
        textfont=dict(color=KM_GOLD, size=11),
        hoverinfo="skip", showlegend=False,
    ))

    # Traza principal (estado final: la espiral completa)
    hover_txt = [
        f"{d.strftime('%Y-%m-%d')}<br>€{v/1e6:.2f}M"
        for d, v in zip(dates_cyl, ventas_cyl)
    ]
    trace_main_idx = n_rings + 12 + 2  # rings + radios mensuales + labels meses + labels años
    fig_cyl.add_trace(go.Scatter3d(
        x=x_line, y=y_line, z=z_line,
        mode="lines",
        line=dict(
            color=ventas_cyl / 1e6, colorscale=[[0, KM_GOLD_DARK], [1, KM_GOLD]],
            width=5, showscale=False,
        ),
        text=hover_txt, hoverinfo="text",
        name="Ventas semanales",
    ))

    # Frames para animación (crecimiento semana a semana, una por frame)
    frames = []
    for end in range(2, n_w + 1):
        frames.append(go.Frame(
            data=[go.Scatter3d(
                x=x_line[:end], y=y_line[:end], z=z_line[:end],
                mode="lines",
                line=dict(
                    color=ventas_cyl[:end] / 1e6,
                    colorscale=[[0, KM_GOLD_DARK], [1, KM_GOLD]],
                    cmin=v_min/1e6, cmax=v_max/1e6,
                    width=5,
                ),
            )],
            traces=[trace_main_idx],
            name=str(end),
        ))
    fig_cyl.frames = frames

    fig_cyl.update_layout(
        title=dict(text="Cilindro = calendario anual · hélice = ventas semanales (deformación radial)",
                   font=dict(color=KM_CREAM, size=13), x=0.02),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=560, margin=dict(l=0, r=0, t=50, b=20),
        scene=dict(
            xaxis=dict(visible=False), yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            bgcolor="rgba(0,0,0,0)",
            aspectmode="manual", aspectratio=dict(x=1, y=1, z=2.0),
            camera=dict(eye=dict(x=2.2, y=2.2, z=0.35)),
        ),
        updatemenus=[play_button(duration=35, x=0.02, y=0.02)],
        annotations=[play_hint_annotation()],
    )
    st.plotly_chart(fig_cyl, width="stretch")
    st.markdown(caption(
        f"Cada vuelta del cilindro es un año (Ene→Dic). La altura es tiempo cronológico, "
        f"y el radio se despega de la base proporcionalmente a las ventas semanales. "
        f"Pulsa <b>Play</b> para ver cómo se traza la hélice semana a semana."
    ), unsafe_allow_html=True)

    # ── Mini tarjetas por canal ──
    mc_cols = st.columns(4)
    for i, (grp, col_) in enumerate(zip(channel_groups, mc_cols)):
        contrib_g = contrib_total_grupo[grp] / 1e6
        roi_g     = roi_por_grupo[grp]
        pct_g     = contrib_total_grupo[grp] / ventas_totales * 100
        with col_:
            st.markdown(f"""
            <div class="kpi-card" style="text-align:left; border-left: 3px solid {GROUP_COLORS[grp]};">
              <div class="kpi-label" style="color:{GROUP_COLORS[grp]};">{GROUP_LABELS[grp]}</div>
              <div style="display:flex; align-items:baseline; gap:10px; margin-top:6px;">
                <span class="kpi-value" style="font-size:22px;">€{contrib_g:.0f}M</span>
                <span style="color:{KM_GOLD}; font-size:13px;">{roi_g:.1f}x</span>
              </div>
              <div class="kpi-sub">{pct_g:.1f}% de ventas · contribución acumulada</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Eficiencia por canal ──
    st.markdown('<p class="section-header">Eficiencia por Canal · Inversión vs Retorno</p>', unsafe_allow_html=True)

    col_c, col_d = st.columns([1.15, 1])

    with col_c:
        # Barras paralelas: inversión vs contribución en M€, con etiqueta mROI
        grps_sorted = sorted(channel_groups, key=lambda g: roi_por_grupo[g], reverse=True)
        labels_c    = [GROUP_LABELS[g] for g in grps_sorted]
        inv_vals    = [etl[channel_groups[g]].sum().sum() / 1e6 for g in grps_sorted]
        con_vals    = [contrib_total_grupo[g] / 1e6 for g in grps_sorted]
        roi_vals    = [roi_por_grupo[g] for g in grps_sorted]

        fig_ef = go.Figure()
        fig_ef.add_trace(go.Bar(
            y=labels_c, x=inv_vals, orientation="h", name="Inversión",
            marker=dict(color="rgba(158,152,147,0.35)", line=dict(color=KM_GRAY, width=1)),
            text=[f"€{v:.0f}M" for v in inv_vals],
            textposition="inside", textfont=dict(color=KM_CREAM, size=10),
            hovertemplate="Inversión: €%{x:.1f}M<extra></extra>",
        ))
        fig_ef.add_trace(go.Bar(
            y=labels_c, x=con_vals, orientation="h", name="Contribución",
            marker=dict(color=[GROUP_COLORS[g] for g in grps_sorted]),
            text=[f"€{v:.0f}M  ·  {r:.1f}x" for v, r in zip(con_vals, roi_vals)],
            textposition="outside", textfont=dict(color=KM_GOLD, size=11),
            hovertemplate="Contribución: €%{x:.1f}M<extra></extra>",
        ))
        apply_layout(fig_ef,
                     title="Inversión vs Contribución por canal (M€, etiqueta = mROI)",
                     barmode="group", height=340, xaxis_title="M€",
                     legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_ef, width="stretch")

    with col_d:
        hm_rows = []
        for yr in years:
            m = etl["anio"] == yr
            for grp, channels in channel_groups.items():
                inv_yr  = etl.loc[m, channels].sum().sum()
                cont_yr = contribs_eur[f"logadstock_{grp}"][m.values].sum()
                hm_rows.append({"Año": str(yr), "Canal": GROUP_LABELS[grp],
                                "mROI": cont_yr / inv_yr if inv_yr > 0 else 0})
        hm_df  = pd.DataFrame(hm_rows)
        hm_piv = hm_df.pivot(index="Canal", columns="Año", values="mROI").reindex(labels_c)

        fig_hm = go.Figure(go.Heatmap(
            z=hm_piv.values, x=hm_piv.columns.tolist(), y=hm_piv.index.tolist(),
            colorscale=[[0, "#1a0a00"], [0.4, KM_GOLD_DARK], [1, KM_GOLD]],
            text=[[f"{v:.1f}x" for v in row] for row in hm_piv.values],
            texttemplate="%{text}",
            textfont=dict(size=12, color=KM_CREAM),
            hovertemplate="<b>%{y}</b> · %{x}<br>mROI: %{z:.2f}x<extra></extra>",
            colorbar=dict(title=dict(text="mROI", font=dict(color=KM_GRAY, size=10)),
                          thickness=10, len=0.7),
        ))
        apply_layout(fig_hm, title="mROI por canal · año",
                     height=340, margin=dict(t=64, b=40, l=130, r=30))
        st.plotly_chart(fig_hm, width="stretch")

    st.markdown(caption(
        f"<b>{GROUP_LABELS[best_grp]}</b> convierte cada euro en <b>{roi_por_grupo[best_grp]:.1f}×</b> de ventas — "
        f"el ratio más alto del mix. <b>{GROUP_LABELS[worst_grp]}</b> necesita más inversión por euro de venta generado "
        f"({roi_por_grupo[worst_grp]:.1f}×): candidato prioritario a revisión."
    ), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — CANALES Y ATRIBUCIÓN
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(kpi_card("Canal más eficiente", GROUP_LABELS[best_grp], f"ROI = {roi_por_grupo[best_grp]:.1f}x"), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("Canal menos eficiente", GROUP_LABELS[worst_grp], f"ROI = {roi_por_grupo[worst_grp]:.1f}x"), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("Total atribuido Mkt", fmt_eur(contrib_total_marketing), f"{pct_mkt:.0f}% de ventas"), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("mROI Global", f"{mroi_global:.1f}x", "€ contrib / € invertido"), unsafe_allow_html=True)

    st.markdown("")

    # ── Cascada de atribución ──
    st.markdown('<p class="section-header">Cascada de Atribución</p>', unsafe_allow_html=True)

    wf_items  = [("Base Orgánica", base_total)]
    for grp in sorted(contrib_total_grupo, key=lambda g: contrib_total_grupo[g], reverse=True):
        wf_items.append((GROUP_LABELS[grp], contrib_total_grupo[grp]))
    wf_names    = [w[0] for w in wf_items] + ["Total Ventas"]
    wf_values   = [w[1] for w in wf_items] + [ventas_totales]
    wf_measures = ["absolute"] + ["relative"] * len(contrib_total_grupo) + ["total"]

    fig_wf = go.Figure(go.Waterfall(
        x=wf_names, y=[v / 1e6 for v in wf_values],
        measure=wf_measures,
        connector_line_color=KM_GRAY, connector_line_dash="dot",
        increasing_marker_color=KM_GOLD,
        decreasing_marker_color=KM_DANGER,
        totals_marker_color=KM_GOLD_DARK,
        text=[f"€{v/1e6:.0f}M" for v in wf_values],
        textposition="outside",
        textfont=dict(size=11, color=KM_CREAM),
    ))
    apply_layout(fig_wf, title="De la base orgánica al total de ventas",
                 yaxis_title="M€", height=420, showlegend=False)
    st.plotly_chart(fig_wf, width="stretch")
    st.markdown(caption(
        f"La base orgánica ({fmt_eur(base_total)}) es la venta que existiría sin ninguna inversión activa: "
        f"refleja la fuerza de la marca, el SEO y la recurrencia de clientes. "
        f"Cada barra añade la contribución incremental de ese canal hasta alcanzar {fmt_eur(ventas_totales)}."
    ), unsafe_allow_html=True)

    # ── Área apilada semanal ──
    st.markdown('<p class="section-header">Contribución Semanal por Canal</p>', unsafe_allow_html=True)

    # Orden: base abajo, luego canales de mayor a menor contribución media
    grps_stack = sorted(channel_groups, key=lambda g: contrib_total_grupo[g], reverse=True)
    vista = st.radio("Vista", ["Absoluta (M€)", "Porcentual (%)"], horizontal=True, key="vista_area")

    fig_area = go.Figure()
    if vista.startswith("Absoluta"):
        fig_area.add_trace(go.Scatter(
            x=etl["semana_inicio"], y=base_weekly / 1e6,
            name="Base Orgánica", stackgroup="one",
            line=dict(width=0, color="rgba(237,232,220,0.6)"),
            fillcolor="rgba(237,232,220,0.25)",
            hovertemplate="Base: €%{y:.2f}M<extra></extra>",
        ))
        for grp in grps_stack:
            c = GROUP_COLORS[grp]
            fig_area.add_trace(go.Scatter(
                x=etl["semana_inicio"],
                y=contribs_eur[f"logadstock_{grp}"] / 1e6,
                name=GROUP_LABELS[grp], stackgroup="one",
                line=dict(width=0, color=c),
                fillcolor=c, opacity=0.88,
                hovertemplate=f"{GROUP_LABELS[grp]}: €%{{y:.2f}}M<extra></extra>",
            ))
        y_title = "Ventas (M€)"
    else:
        total_w = y_pred_full.copy()
        total_w[total_w == 0] = 1
        fig_area.add_trace(go.Scatter(
            x=etl["semana_inicio"], y=base_weekly / total_w * 100,
            name="Base Orgánica", stackgroup="one",
            line=dict(width=0), fillcolor="rgba(237,232,220,0.25)",
            hovertemplate="Base: %{y:.1f}%<extra></extra>",
        ))
        for grp in grps_stack:
            c = GROUP_COLORS[grp]
            fig_area.add_trace(go.Scatter(
                x=etl["semana_inicio"],
                y=np.asarray(contribs_eur[f"logadstock_{grp}"]) / total_w * 100,
                name=GROUP_LABELS[grp], stackgroup="one",
                line=dict(width=0), fillcolor=c, opacity=0.88,
                hovertemplate=f"{GROUP_LABELS[grp]}: %{{y:.1f}}%<extra></extra>",
            ))
        y_title = "% de ventas"

    apply_layout(fig_area, title="Descomposición semanal de ventas",
                 yaxis_title=y_title, height=440, hovermode="x unified",
                 legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_area, width="stretch")
    st.markdown(caption(
        "La altura total de cada semana es la venta predicha. "
        "La base orgánica ya no es plana: varía con estacionalidad, festivos y clima (variables de control). "
        "Cambia a <i>Porcentual</i> para ver cómo se redistribuye el mix a lo largo del tiempo."
    ), unsafe_allow_html=True)

    # ── Evolución de inversión (líneas, no barras animadas) ──
    st.markdown('<p class="section-header">Evolución de la Inversión Anual</p>', unsafe_allow_html=True)

    inv_evol_rows = []
    for yr in years:
        m = etl["anio"] == yr
        for grp, channels in channel_groups.items():
            inv_evol_rows.append({
                "Año": yr,
                "Canal": GROUP_LABELS[grp],
                "Inversión (M€)": etl.loc[m, channels].sum().sum() / 1e6,
            })
    inv_evol_df = pd.DataFrame(inv_evol_rows)

    fig_evol = go.Figure()
    for grp in channel_groups:
        sub = inv_evol_df[inv_evol_df["Canal"] == GROUP_LABELS[grp]]
        fig_evol.add_trace(go.Scatter(
            x=sub["Año"], y=sub["Inversión (M€)"],
            mode="lines+markers", name=GROUP_LABELS[grp],
            line=dict(color=GROUP_COLORS[grp], width=2.5),
            marker=dict(size=8, color=GROUP_COLORS[grp]),
            hovertemplate=f"<b>{GROUP_LABELS[grp]}</b> %{{x}}: €%{{y:.1f}}M<extra></extra>",
        ))
    apply_layout(fig_evol, title="Inversión anual por canal",
                 xaxis_title="Año", yaxis_title="Inversión (M€)", height=360)
    fig_evol.update_xaxes(tickmode="array", tickvals=years)
    st.plotly_chart(fig_evol, width="stretch")
    st.markdown(caption(
        "Las tendencias de inversión revelan decisiones estratégicas pasadas. "
        "Un canal con inversión creciente pero ROI estancado (ver heatmap en Visión General) "
        "puede estar acercándose a su punto de saturación."
    ), unsafe_allow_html=True)

    # ── Tabla de atribución ──
    st.markdown('<p class="section-header">Tabla de Atribución con Intervalos de Confianza</p>', unsafe_allow_html=True)

    attr_rows = []
    max_contrib = max(contrib_total_grupo.values())
    for grp, channels in channel_groups.items():
        inv     = etl[channels].sum().sum()
        contrib = contrib_total_grupo[grp]
        ci      = feature_cols.index(f"logadstock_{grp}")
        beta    = model.coef_[ci]
        attr_rows.append({
            "Canal":            GROUP_LABELS[grp],
            "Inversión (M€)":   inv / 1e6,
            "Contribución (M€)": contrib / 1e6,
            "% Ventas":         contrib / ventas_totales * 100,
            "mROI":             roi_por_grupo[grp],
            "β":                beta,
            "IC 95%":           f"[{boot_lo[ci]:,.0f} – {boot_hi[ci]:,.0f}]",
        })
    attr_rows.append({
        "Canal": "Base Orgánica", "Inversión (M€)": None,
        "Contribución (M€)": base_total / 1e6,
        "% Ventas": base_total / ventas_totales * 100,
        "mROI": None, "β": model.intercept_, "IC 95%": "—",
    })
    attr_df = pd.DataFrame(attr_rows)
    st.dataframe(
        attr_df, width="stretch", hide_index=True,
        column_config={
            "Inversión (M€)":    st.column_config.NumberColumn(format="€%.1fM"),
            "Contribución (M€)": st.column_config.ProgressColumn(
                format="€%.1fM", min_value=0, max_value=max_contrib / 1e6),
            "% Ventas":          st.column_config.ProgressColumn(
                format="%.1f%%", min_value=0, max_value=100),
            "mROI":              st.column_config.NumberColumn(format="%.1fx"),
            "β":                 st.column_config.NumberColumn(format="%,.0f"),
        },
    )


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — LABORATORIO DE INVERSIÓN
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:

    # ── Mapa de todos los escenarios ──
    st.markdown('<p class="section-header">Mapa de Posibilidades · 350 Escenarios Simulados</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-card">
        <h3>El espacio completo de decisiones</h3>
        <p>Cada punto es una forma diferente de distribuir el presupuesto entre los 4 canales.
        El eje X es la inversión anual; el eje Y, las ventas proyectadas.
        Los puntos <em>más altos para un mismo nivel de inversión</em> son las asignaciones más eficientes.</p>
    </div>
    """, unsafe_allow_html=True)

    r_base_l = simular(inv_hist_media)
    canal_alto = max(roi_por_grupo, key=roi_por_grupo.get)
    canal_bajo = min(roi_por_grupo, key=roi_por_grupo.get)
    transfer_l = inv_hist_media[f"inv_{canal_bajo}"] * 0.30
    inv_opt_l  = inv_hist_media.copy()
    inv_opt_l[f"inv_{canal_alto}"] += transfer_l
    inv_opt_l[f"inv_{canal_bajo}"] -= transfer_l
    r_opt_l = simular(inv_opt_l)

    # mROI por escenario para colorear los puntos
    land_df = landscape_df.copy()
    land_df["mroi"] = land_df["ventas"] / land_df["inv_anual"]

    # Frontera eficiente: para cada bin de inversión, el máximo de ventas
    bins = np.linspace(land_df["inv_anual"].min(), land_df["inv_anual"].max(), 18)
    land_df["_bin"] = pd.cut(land_df["inv_anual"], bins=bins, include_lowest=True)
    frontier = land_df.loc[land_df.groupby("_bin", observed=True)["ventas"].idxmax()].sort_values("inv_anual")

    fig_land = go.Figure()
    # Nube de escenarios coloreada por mROI
    fig_land.add_trace(go.Scatter(
        x=land_df["inv_anual"] / 1e6, y=land_df["ventas"] / 1e6,
        mode="markers", name="Escenarios simulados",
        marker=dict(
            size=7, color=land_df["mroi"], colorscale=[[0, "#3a2510"], [0.5, KM_GOLD_DARK], [1, KM_GOLD]],
            opacity=0.65, line=dict(width=0),
            colorbar=dict(title=dict(text="mROI", font=dict(color=KM_GRAY, size=10)),
                          thickness=10, len=0.5, x=1.02),
        ),
        customdata=np.stack([land_df["canal_dom"], land_df["mroi"]], axis=-1),
        hovertemplate=("Inversión: €%{x:.1f}M<br>"
                       "Ventas: €%{y:.1f}M<br>"
                       "Canal dominante: %{customdata[0]}<br>"
                       "mROI: %{customdata[1]:.1f}x<extra></extra>"),
    ))
    # Frontera eficiente
    fig_land.add_trace(go.Scatter(
        x=frontier["inv_anual"] / 1e6, y=frontier["ventas"] / 1e6,
        mode="lines", name="Frontera eficiente",
        line=dict(color=KM_CREAM, width=2, dash="dash"), opacity=0.75,
        hovertemplate="Máx ventas · €%{x:.1f}M → €%{y:.1f}M<extra></extra>",
    ))

    fig_land.add_trace(go.Scatter(
        x=[r_base_l["inv_total_eur"] / 1e6], y=[r_base_l["ventas_anual_eur"] / 1e6],
        mode="markers+text", name="Baseline",
        marker=dict(size=18, color=KM_CREAM, symbol="diamond", line=dict(color=KM_GOLD, width=2)),
        text=["Baseline"], textposition="bottom right",
        textfont=dict(size=11, color=KM_CREAM),
    ))
    fig_land.add_trace(go.Scatter(
        x=[r_opt_l["inv_total_eur"] / 1e6], y=[r_opt_l["ventas_anual_eur"] / 1e6],
        mode="markers+text", name="Óptimo",
        marker=dict(size=22, color=KM_GOLD, symbol="star", line=dict(color=KM_CREAM, width=1)),
        text=["Óptimo"], textposition="top right",
        textfont=dict(size=12, color=KM_GOLD),
    ))
    apply_layout(fig_land,
                 title="Mapa de posibilidades · color = mROI, línea = frontera eficiente",
                 xaxis_title="Inversión anual (M€)",
                 yaxis_title="Ventas proyectadas (M€)", height=520,
                 legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_land, width="stretch")
    st.markdown(caption(
        "Cada punto es un reparto presupuestario distinto. El <b>color</b> codifica eficiencia (mROI): "
        "puntos más dorados = más ventas por euro invertido. La <b>línea discontinua</b> es la frontera eficiente — "
        f"la combinación que maximiza ventas para cada nivel de inversión. Reasignar 30% de "
        f"<b>{GROUP_LABELS[worst_grp]}</b> → <b>{GROUP_LABELS[best_grp]}</b> mueve el Baseline al Óptimo "
        f"({r_opt_l['lift_pct']:+.1f}% ventas, sin aumentar presupuesto)."
    ), unsafe_allow_html=True)

    # ── Lluvia de escenarios: Riesgo vs. Upside vs. Concentración ──
    st.markdown(animated_header("Lluvia de Escenarios · Riesgo, Upside y Concentración",
                                label="▶ INTERACTIVO · pulsa Llover"), unsafe_allow_html=True)

    @st.cache_data
    def _compute_risk_cloud(n=220, seed=7):
        rng = np.random.default_rng(seed)
        n_ch = len(inv_group_cols)
        base_wk = sum(inv_hist_media.values())
        r_base = simular(inv_hist_media)["ventas_anual_eur"]
        # Factores de presupuesto (½× a 2×) × Dirichlet desbalanceado para cubrir concentración
        factors = rng.uniform(0.5, 2.0, n)
        allocs = rng.dirichlet(np.ones(n_ch) * 0.6, n)
        boot_np = np.asarray(boot_coefs)  # (B, n_feat)
        rows = []
        for bf, alloc in zip(factors, allocs):
            inv = {g: base_wk * bf * a for g, a in zip(inv_group_cols, alloc)}
            X_sim = _build_X_sim(inv)
            ventas_point = float(model.predict(X_sim).sum())
            ventas_boot = np.maximum(model.intercept_ + X_sim @ boot_np.T, 0).sum(axis=0)
            inv_anual = sum(inv.values()) * 52
            hhi = float(np.sum(alloc ** 2))  # Herfindahl 0.25 (uniforme) → 1.0 (mono-canal)
            dom = GROUP_LABELS.get(inv_group_cols[int(np.argmax(alloc))].replace("inv_", ""), "")
            rows.append({
                "hhi":       hhi,
                "d_ventas":  (ventas_point - r_base) / 1e6,     # M€
                "riesgo":    float(ventas_boot.std()) / 1e6,    # M€ (std bootstrap)
                "roi":       (ventas_point - r_base) / inv_anual if inv_anual > 0 else 0,
                "ventas":    ventas_point / 1e6,
                "inv_anual": inv_anual / 1e6,
                "canal_dom": dom,
            })
        df_ = pd.DataFrame(rows)
        # Orden de "lluvia": peores primero, mejores al final (suspense)
        df_ = df_.sort_values("d_ventas").reset_index(drop=True)
        return df_, r_base

    risk_df, r_base_rc = _compute_risk_cloud()
    hhi_base = float(np.sum(np.array([inv_hist_media[g] for g in inv_group_cols]) /
                            sum(inv_hist_media.values())) ** 2 * 0)  # placeholder
    _alloc_base = np.array([inv_hist_media[g] for g in inv_group_cols])
    _alloc_base = _alloc_base / _alloc_base.sum()
    hhi_base = float(np.sum(_alloc_base ** 2))
    # Riesgo del baseline
    _X_base = _build_X_sim(inv_hist_media)
    _boot_np = np.asarray(boot_coefs)
    _vb_base = np.maximum(model.intercept_ + _X_base @ _boot_np.T, 0).sum(axis=0)
    riesgo_base = float(_vb_base.std()) / 1e6

    fig_rain = go.Figure()
    # Punto baseline (referencia fija)
    fig_rain.add_trace(go.Scatter3d(
        x=[hhi_base], y=[0.0], z=[riesgo_base],
        mode="markers+text", text=["baseline"], textposition="top center",
        textfont=dict(color=KM_CREAM, size=11),
        marker=dict(size=9, color=KM_CREAM, symbol="diamond", line=dict(color=KM_GOLD, width=1.5)),
        showlegend=False,
        hovertemplate=f"<b>Baseline</b><br>HHI: %{{x:.2f}}<br>ΔVentas: 0<br>Riesgo σ: €%{{z:.2f}}M<extra></extra>",
    ))
    # Traza-lluvia (se irá revelando en frames). Empieza con un punto invisible.
    trace_rain_idx = 1
    fig_rain.add_trace(go.Scatter3d(
        x=[risk_df["hhi"].iloc[0]], y=[risk_df["d_ventas"].iloc[0]], z=[risk_df["riesgo"].iloc[0]],
        mode="markers",
        marker=dict(
            size=6, color=[risk_df["roi"].iloc[0]],
            colorscale=[[0, "#3a2510"], [0.5, KM_GOLD_DARK], [1, KM_GOLD]],
            cmin=float(risk_df["roi"].min()), cmax=float(risk_df["roi"].max()),
            opacity=0.85, line=dict(width=0),
            colorbar=dict(title=dict(text="mROI", font=dict(color=KM_GRAY, size=10)),
                          thickness=10, len=0.5, x=1.02, tickfont=dict(color=KM_GRAY, size=9)),
        ),
        customdata=np.stack([risk_df["canal_dom"].iloc[:1], risk_df["ventas"].iloc[:1]], axis=-1),
        hovertemplate=("HHI: %{x:.2f}<br>ΔVentas: €%{y:+.2f}M<br>Riesgo σ: €%{z:.2f}M"
                       "<br>Canal dom: %{customdata[0]}<br>Ventas: €%{customdata[1]:.1f}M<extra></extra>"),
        showlegend=False,
    ))

    # Frames: van cayendo los escenarios en lotes (más fluido que 1 a 1)
    BATCH = 4
    frames_rain = []
    for end in range(BATCH, len(risk_df) + 1, BATCH):
        sub = risk_df.iloc[:end]
        frames_rain.append(go.Frame(
            data=[go.Scatter3d(
                x=sub["hhi"], y=sub["d_ventas"], z=sub["riesgo"],
                mode="markers",
                marker=dict(
                    size=6, color=sub["roi"],
                    colorscale=[[0, "#3a2510"], [0.5, KM_GOLD_DARK], [1, KM_GOLD]],
                    cmin=float(risk_df["roi"].min()), cmax=float(risk_df["roi"].max()),
                    opacity=0.85, line=dict(width=0),
                ),
                customdata=np.stack([sub["canal_dom"], sub["ventas"]], axis=-1),
                hovertemplate=("HHI: %{x:.2f}<br>ΔVentas: €%{y:+.2f}M<br>Riesgo σ: €%{z:.2f}M"
                               "<br>Canal dom: %{customdata[0]}<br>Ventas: €%{customdata[1]:.1f}M<extra></extra>"),
            )],
            traces=[trace_rain_idx], name=str(end),
        ))
    fig_rain.frames = frames_rain

    fig_rain.update_layout(
        title=dict(text="Cada gota = un reparto presupuestario · color = ROI marginal",
                   font=dict(color=KM_CREAM, size=13), x=0.02),
        paper_bgcolor="rgba(0,0,0,0)",
        height=600, margin=dict(l=0, r=0, t=50, b=20),
        scene=dict(
            xaxis=dict(title="Concentración (HHI)", color=KM_GRAY,
                       gridcolor="rgba(200,169,110,0.1)", backgroundcolor="rgba(0,0,0,0)"),
            yaxis=dict(title="ΔVentas vs baseline (M€/año)", color=KM_GRAY,
                       gridcolor="rgba(200,169,110,0.1)", backgroundcolor="rgba(0,0,0,0)"),
            zaxis=dict(title="Riesgo σ bootstrap (M€)", color=KM_GRAY,
                       gridcolor="rgba(200,169,110,0.1)", backgroundcolor="rgba(0,0,0,0)"),
            bgcolor="rgba(0,0,0,0)",
            camera=dict(eye=dict(x=1.8, y=-1.8, z=1.1)),
        ),
        updatemenus=[play_button(play_label="▶ Llover", duration=55, x=0.02, y=0.02)],
        annotations=[play_hint_annotation(text="⚡ Pulsa ▶ Llover para ver caer los escenarios")],
    )
    st.plotly_chart(fig_rain, width="stretch")

    # Pareto: máxima ΔVentas por bin de riesgo
    _q_lo = risk_df["d_ventas"].quantile(0.9)
    _top = risk_df[risk_df["d_ventas"] >= _q_lo].sort_values("riesgo").iloc[0]
    st.markdown(caption(
        f"Eje <b>X</b>: concentración del mix (HHI; 0.25 = equireparto, 1.0 = mono-canal). "
        f"Eje <b>Y</b>: ΔVentas vs. baseline. Eje <b>Z</b>: desviación estándar de ventas por bootstrap (riesgo del modelo). "
        f"El óptimo no es el punto más alto en Y — es el que maximiza Y con el menor Z posible. "
        f"Mejor compromiso detectado: ΔVentas <b style='color:{KM_GOLD}'>€{_top['d_ventas']:+.2f}M</b> "
        f"con riesgo σ <b>€{_top['riesgo']:.2f}M</b> (HHI {_top['hhi']:.2f}, canal dominante {_top['canal_dom']})."
    ), unsafe_allow_html=True)

    # ── Tornado de sensibilidad ──
    st.markdown('<p class="section-header">Sensibilidad Marginal por Canal · ±10%</p>', unsafe_allow_html=True)

    col_t1, col_t2 = st.columns([3, 1])

    with col_t1:
        sorted_grps = sorted(tornado_up.keys(), key=lambda g: tornado_up[g])
        labels_t    = [GROUP_LABELS.get(g.replace("inv_", ""), g) for g in sorted_grps]
        vals_up     = [tornado_up[g] / 1e6 for g in sorted_grps]
        vals_dn     = [tornado_dn[g] / 1e6 for g in sorted_grps]

        fig_tor = go.Figure()
        fig_tor.add_trace(go.Bar(
            y=labels_t, x=vals_up, orientation="h", name="+10% inversión",
            marker_color=KM_GOLD,
            text=[f"+{fmt_eur(v*1e6)}" for v in vals_up],
            textposition="outside", textfont=dict(size=11, color=KM_GOLD),
        ))
        fig_tor.add_trace(go.Bar(
            y=labels_t, x=vals_dn, orientation="h", name="−10% inversión",
            marker_color=KM_DANGER,
            text=[f"{fmt_eur(v*1e6)}" for v in vals_dn],
            textposition="outside", textfont=dict(size=11, color=KM_DANGER),
        ))
        apply_layout(fig_tor,
                     title="Δ Ventas anuales al mover un 10% en cada canal",
                     xaxis_title="Δ Ventas anuales (M€)",
                     barmode="overlay", height=320, showlegend=True)
        fig_tor.add_vline(x=0, line=dict(color=KM_GRAY, width=1))
        st.plotly_chart(fig_tor, width="stretch")

    with col_t2:
        best_up_grp = max(tornado_up, key=tornado_up.get)
        best_up_val = tornado_up[best_up_grp]
        best_lab    = GROUP_LABELS.get(best_up_grp.replace("inv_", ""), best_up_grp)
        st.markdown(f"""
        <div class="insight-card" style="margin-top:32px;">
            <h3>Canal con mayor palanca</h3>
            <p>
                +10% en <strong>{best_lab}</strong> genera
                <strong>{fmt_eur(best_up_val)}</strong> adicionales al año.<br><br>
                Es el canal con mayor <em>elasticidad marginal</em>:
                cada euro extra aquí rinde más que en cualquier otro canal.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(caption(
        "Los canales no son intercambiables: reasignar el mismo presupuesto entre ellos produce resultados muy distintos. "
        "El tornado muestra exactamente cuánto se gana o pierde al mover un 10% en cada dirección."
    ), unsafe_allow_html=True)

    # ── Curvas de retorno por canal ──
    st.markdown('<p class="section-header">Curvas de Retorno · Rendimientos Decrecientes</p>', unsafe_allow_html=True)

    # Selector de canales a mostrar
    canal_keys = [g.replace("inv_", "") for g in inv_group_cols]
    canal_labs = [GROUP_LABELS[k] for k in canal_keys]
    sel_canales = st.multiselect("Canales visibles", canal_labs, default=canal_labs, key="sat_sel")

    fig_sat = go.Figure()
    for grp, key, lab in zip(inv_group_cols, canal_keys, canal_labs):
        if lab not in sel_canales:
            continue
        inv_range, revenues = saturation_curves[grp]
        color    = GROUP_COLORS[key]
        hist_val = inv_hist_media[grp]
        hi       = int(np.argmin(np.abs(inv_range - hist_val)))

        # Detectar zona de saturación: derivada < 10% del máximo
        dy = np.gradient(revenues, inv_range)
        if dy.max() > 0:
            sat_mask = dy < 0.10 * dy.max()
            first_sat = np.argmax(sat_mask) if sat_mask.any() else len(inv_range) - 1
        else:
            first_sat = len(inv_range) - 1

        # Tramo crecimiento
        fig_sat.add_trace(go.Scatter(
            x=inv_range[:first_sat + 1] / 1e3, y=revenues[:first_sat + 1] / 1e6,
            name=lab, legendgroup=lab, mode="lines",
            line=dict(color=color, width=2.8),
            hovertemplate=f"<b>{lab}</b><br>€%{{x:.0f}}k/sem → €%{{y:.1f}}M/año<extra></extra>",
        ))
        # Tramo saturado: línea punteada
        if first_sat < len(inv_range) - 1:
            fig_sat.add_trace(go.Scatter(
                x=inv_range[first_sat:] / 1e3, y=revenues[first_sat:] / 1e6,
                name=lab, legendgroup=lab, mode="lines", showlegend=False,
                line=dict(color=color, width=1.8, dash="dot"), opacity=0.6,
                hovertemplate=f"<b>{lab}</b> · saturado<br>€%{{x:.0f}}k/sem → €%{{y:.1f}}M<extra></extra>",
            ))
        # Punto histórico
        fig_sat.add_trace(go.Scatter(
            x=[inv_range[hi] / 1e3], y=[revenues[hi] / 1e6],
            mode="markers+text", showlegend=False, legendgroup=lab,
            marker=dict(size=12, color=color, line=dict(color=KM_CREAM, width=1.5)),
            text=["hoy"], textposition="top center",
            textfont=dict(size=9, color=color),
            hovertemplate=(f"<b>{lab}</b><br>Inversión actual: €{inv_range[hi]/1e3:.0f}k/sem<br>"
                           f"→ €{revenues[hi]/1e6:.1f}M/año<extra></extra>"),
        ))

    apply_layout(fig_sat,
                 title="Curvas de retorno · línea continua = crecimiento, punteada = saturación",
                 xaxis_title="Inversión semanal en el canal (€k)",
                 yaxis_title="Ventas anuales proyectadas (M€)", height=460,
                 legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_sat, width="stretch")
    st.markdown(caption(
        "Los círculos abiertos marcan el nivel histórico de inversión en cada canal. "
        "Donde la curva se aplana, el canal ha alcanzado su punto de saturación: "
        "invertir más apenas mueve las ventas. "
        "Donde la pendiente sigue siendo pronunciada, hay recorrido de crecimiento."
    ), unsafe_allow_html=True)

    # ── Superficie 3D de respuesta: colina de ventas sobre los 2 canales top ──
    st.markdown(animated_header("Colina de Respuesta · Ventas vs. dos canales top",
                                label="▶ INTERACTIVO · pulsa Ascenso"), unsafe_allow_html=True)

    top2 = sorted(contrib_total_grupo, key=lambda g: contrib_total_grupo[g], reverse=True)[:2]
    grp_a, grp_b = top2[0], top2[1]
    col_a, col_b = f"inv_{grp_a}", f"inv_{grp_b}"
    lab_a, lab_b = GROUP_LABELS[grp_a], GROUP_LABELS[grp_b]
    hist_a, hist_b = inv_hist_media[col_a], inv_hist_media[col_b]

    @st.cache_data
    def _compute_response_surface(grp_a, grp_b, n_grid=18):
        col_a = f"inv_{grp_a}"
        col_b = f"inv_{grp_b}"
        xs_ = np.linspace(0, 3 * inv_hist_media[col_a], n_grid)
        ys_ = np.linspace(0, 3 * inv_hist_media[col_b], n_grid)
        Z_ = np.zeros((n_grid, n_grid))
        for i_, xv in enumerate(xs_):
            for j_, yv in enumerate(ys_):
                inv = {g: inv_hist_media[g] for g in inv_group_cols}
                inv[col_a] = xv
                inv[col_b] = yv
                Z_[j_, i_] = simular(inv)["ventas_anual_eur"] / 1e6
        return xs_, ys_, Z_

    xs_s, ys_s, Z_s = _compute_response_surface(grp_a, grp_b)

    i_base = int(np.argmin(np.abs(xs_s - hist_a)))
    j_base = int(np.argmin(np.abs(ys_s - hist_b)))
    j_opt, i_opt = np.unravel_index(int(np.argmax(Z_s)), Z_s.shape)

    # Gradient ascent discreto (8-vecinos) sobre el grid pre-computado
    path_i, path_j = [i_base], [j_base]
    ci, cj = i_base, j_base
    for _ in range(80):
        best_ij, best_z = (ci, cj), Z_s[cj, ci]
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                if di == 0 and dj == 0: continue
                ni, nj = ci + di, cj + dj
                if 0 <= ni < len(xs_s) and 0 <= nj < len(ys_s) and Z_s[nj, ni] > best_z:
                    best_ij, best_z = (ni, nj), Z_s[nj, ni]
        if best_ij == (ci, cj): break
        ci, cj = best_ij
        path_i.append(ci); path_j.append(cj)

    path_x = np.array([xs_s[i] for i in path_i]) / 1e3
    path_y = np.array([ys_s[j] for j in path_j]) / 1e3
    path_z = np.array([Z_s[j, i] for i, j in zip(path_i, path_j)])

    fig_surf = go.Figure()
    fig_surf.add_trace(go.Surface(
        x=xs_s / 1e3, y=ys_s / 1e3, z=Z_s,
        colorscale=[[0, "#1a1a1a"], [0.35, KM_GOLD_DARK], [1, KM_GOLD]],
        opacity=0.92, showscale=False,
        contours=dict(z=dict(show=True, usecolormap=True, highlightcolor=KM_CREAM, project_z=True)),
        hovertemplate=(f"{lab_a}: €%{{x:.0f}}k/sem<br>{lab_b}: €%{{y:.0f}}k/sem"
                       "<br>Ventas: €%{z:.2f}M/año<extra></extra>"),
    ))
    fig_surf.add_trace(go.Scatter3d(
        x=[hist_a/1e3], y=[hist_b/1e3], z=[Z_s[j_base, i_base]],
        mode="markers+text", text=["baseline"], textposition="top center",
        textfont=dict(color=KM_GRAY, size=10),
        marker=dict(size=7, color=KM_GRAY, line=dict(color=KM_CREAM, width=1)),
        showlegend=False,
        hovertemplate="<b>Baseline</b><br>€%{z:.2f}M/año<extra></extra>",
    ))
    fig_surf.add_trace(go.Scatter3d(
        x=[xs_s[i_opt]/1e3], y=[ys_s[j_opt]/1e3], z=[Z_s[j_opt, i_opt]],
        mode="markers+text", text=["óptimo"], textposition="top center",
        textfont=dict(color=KM_GOLD, size=11),
        marker=dict(size=10, color=KM_GOLD, symbol="diamond", line=dict(color=KM_CREAM, width=1.5)),
        showlegend=False,
        hovertemplate="<b>Óptimo</b><br>€%{z:.2f}M/año<extra></extra>",
    ))
    trace_path_idx = 3
    fig_surf.add_trace(go.Scatter3d(
        x=[path_x[0]], y=[path_y[0]], z=[path_z[0]],
        mode="lines+markers",
        line=dict(color=KM_CREAM, width=6),
        marker=dict(size=4, color=KM_CREAM),
        showlegend=False, hoverinfo="skip",
    ))

    frames_surf = []
    for k in range(1, len(path_x) + 1):
        frames_surf.append(go.Frame(
            data=[go.Scatter3d(
                x=path_x[:k], y=path_y[:k], z=path_z[:k],
                mode="lines+markers",
                line=dict(color=KM_CREAM, width=6),
                marker=dict(size=4, color=KM_CREAM),
            )],
            traces=[trace_path_idx], name=str(k),
        ))
    fig_surf.frames = frames_surf

    fig_surf.update_layout(
        title=dict(text=f"Ventas anuales proyectadas según inversión semanal en {lab_a} y {lab_b}",
                   font=dict(color=KM_CREAM, size=13), x=0.02),
        paper_bgcolor="rgba(0,0,0,0)",
        height=620, margin=dict(l=0, r=0, t=50, b=20),
        scene=dict(
            xaxis=dict(title=f"{lab_a} (€k/sem)", color=KM_GRAY,
                       gridcolor="rgba(200,169,110,0.1)", backgroundcolor="rgba(0,0,0,0)"),
            yaxis=dict(title=f"{lab_b} (€k/sem)", color=KM_GRAY,
                       gridcolor="rgba(200,169,110,0.1)", backgroundcolor="rgba(0,0,0,0)"),
            zaxis=dict(title="Ventas (M€/año)", color=KM_GRAY,
                       gridcolor="rgba(200,169,110,0.1)", backgroundcolor="rgba(0,0,0,0)"),
            bgcolor="rgba(0,0,0,0)",
            camera=dict(eye=dict(x=1.7, y=-1.7, z=1.0)),
        ),
        updatemenus=[play_button(play_label="▶ Ascenso", duration=140, x=0.02, y=0.02)],
        annotations=[play_hint_annotation(text="⚡ Pulsa ▶ Ascenso para escalar la colina")],
    )
    st.plotly_chart(fig_surf, width="stretch")

    lift_opt_pct = (Z_s[j_opt, i_opt] - Z_s[j_base, i_base]) / Z_s[j_base, i_base] * 100
    st.markdown(caption(
        f"Fijando el resto de canales en su media histórica, la colina muestra las ventas anuales para cada "
        f"combinación de inversión en <b style='color:{KM_GOLD}'>{lab_a}</b> y <b style='color:{KM_GOLD}'>{lab_b}</b>. "
        f"Donde la superficie se aplana → saturación conjunta. "
        f"Pulsa <b>▶ Ascenso</b> para ver la ruta de gradient ascent desde el baseline al óptimo "
        f"(<b>+{lift_opt_pct:.1f}%</b> vs. mix histórico)."
    ), unsafe_allow_html=True)

    # ── Escenarios predefinidos ──
    st.markdown('<p class="section-header">Escenarios Estratégicos</p>', unsafe_allow_html=True)

    inv_base_d = {g: dp[g].mean() for g in inv_group_cols}

    inv_cons = inv_base_d.copy()
    inv_cons[f"inv_{best_grp}"]  *= 1.10
    inv_cons[f"inv_{worst_grp}"] *= 0.90

    t_opt = inv_base_d[f"inv_{worst_grp}"] * 0.30
    inv_opt_d = inv_base_d.copy()
    inv_opt_d[f"inv_{best_grp}"]  += t_opt
    inv_opt_d[f"inv_{worst_grp}"] -= t_opt

    inv_rec  = {g: v * 0.50 for g, v in inv_base_d.items()}
    inv_agr  = {g: v * 1.30 for g, v in inv_opt_d.items()}

    escenarios = {
        "Baseline":     (inv_base_d, "Reparto histórico sin cambios"),
        "Recorte −50%": (inv_rec,    "Reducción del 50% en todos los canales"),
        "Conservador":  (inv_cons,   f"+10% {GROUP_LABELS[best_grp]}, −10% {GROUP_LABELS[worst_grp]}"),
        "Óptimo":       (inv_opt_d,  f"30% de {GROUP_LABELS[worst_grp]} hacia {GROUP_LABELS[best_grp]}"),
        "Óptimo +30%":  (inv_agr,    "Redistribución óptima con +30% presupuesto"),
    }

    esc_results = {}
    for name, (inv, desc) in escenarios.items():
        r = simular(inv); r["desc"] = desc; r["inv"] = inv
        esc_results[name] = r

    base_v  = esc_results["Baseline"]["ventas_anual_eur"]
    esc_names_l = list(esc_results.keys())
    esc_cols_c  = [
        KM_GRAY if n == "Baseline" else KM_DANGER if "Recorte" in n
        else KM_GOLD_DARK if n == "Conservador" else KM_GOLD if n == "Óptimo"
        else KM_ACCENT for n in esc_names_l
    ]

    fig_esc = make_subplots(rows=1, cols=2,
                            subplot_titles=("Ventas anuales proyectadas (M€)",
                                            "Inversión anual (M€)"))
    fig_esc.add_trace(go.Bar(
        x=esc_names_l,
        y=[esc_results[n]["ventas_anual_eur"] / 1e6 for n in esc_names_l],
        marker_color=esc_cols_c,
        text=[f"€{esc_results[n]['ventas_anual_eur']/1e6:.0f}M  "
              f"{(esc_results[n]['ventas_anual_eur']-base_v)/base_v*100:+.1f}%"
              for n in esc_names_l],
        textposition="outside", textfont=dict(size=10, color=KM_CREAM),
        showlegend=False,
    ), row=1, col=1)
    fig_esc.add_trace(go.Bar(
        x=esc_names_l,
        y=[esc_results[n]["inv_total_eur"] / 1e6 for n in esc_names_l],
        marker_color=esc_cols_c, opacity=0.6,
        text=[f"€{esc_results[n]['inv_total_eur']/1e6:.1f}M" for n in esc_names_l],
        textposition="outside", textfont=dict(size=10, color=KM_CREAM),
        showlegend=False,
    ), row=1, col=2)
    apply_layout(fig_esc, title="", height=400)
    fig_esc.update_annotations(font=dict(color=KM_GRAY, size=11))
    st.plotly_chart(fig_esc, width="stretch")

    cols_esc = st.columns(5)
    highlights = ["", "", "", "highlight", ""]
    for i, (name, er) in enumerate(esc_results.items()):
        lift   = er["ventas_anual_eur"] - base_v
        lift_p = lift / base_v * 100
        dc     = KM_SUCCESS if lift >= 0 else KM_DANGER
        with cols_esc[i]:
            st.markdown(f"""
            <div class="scenario-card {highlights[i]}">
                <div class="scenario-title">{name}</div>
                <div class="scenario-value">{fmt_eur(er['ventas_anual_eur'])}</div>
                <div class="scenario-delta" style="color:{dc};">{lift_p:+.1f}% · {fmt_eur(lift)}</div>
                <div class="scenario-delta" style="color:{KM_GRAY}; font-size:10px; margin-top:6px;">{er['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")

    # ── Simulador interactivo ──
    st.markdown('<p class="section-header">Simulador Interactivo · Presupuesto Propio</p>', unsafe_allow_html=True)

    inv_base_ref  = {g: dp[g].mean() for g in inv_group_cols}
    total_wk_hist = sum(inv_base_ref.values())

    budget_total = st.slider(
        "Presupuesto semanal total (€)",
        min_value=0, max_value=int(total_wk_hist * 3),
        value=int(total_wk_hist), step=1000, format="€%d", key="budget_sim",
    )
    st.markdown("**Distribución porcentual por canal:**")
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    pct_hist = {g: inv_base_ref[g] / total_wk_hist * 100 for g in inv_group_cols}
    with col_s1: pct_perf  = st.slider("Performance",        0, 100, int(pct_hist["inv_performance"]),        key="sp1")
    with col_s2: pct_brand = st.slider("Branding Digital",   0, 100, int(pct_hist["inv_branding_digital"]),   key="sp2")
    with col_s3: pct_off   = st.slider("Offline Medios",     0, 100, int(pct_hist["inv_offline_medios"]),     key="sp3")
    with col_s4: pct_prop  = st.slider("Propios y Exterior", 0, 100, int(pct_hist["inv_propios_y_exterior"]), key="sp4")

    pct_total = pct_perf + pct_brand + pct_off + pct_prop
    if pct_total == 0:
        st.warning("La suma es 0%. Ajusta los sliders.")
        st.stop()

    inv_sim = {
        "inv_performance":        budget_total * (pct_perf  / pct_total),
        "inv_branding_digital":   budget_total * (pct_brand / pct_total),
        "inv_offline_medios":     budget_total * (pct_off   / pct_total),
        "inv_propios_y_exterior": budget_total * (pct_prop  / pct_total),
    }
    if pct_total != 100:
        st.info(f"Suma = {pct_total}% → normalizado automáticamente a 100%.")

    # Donut con la distribución normalizada
    norm_pct = {g: 100 * (v / pct_total) for g, v in
                zip(inv_group_cols, [pct_perf, pct_brand, pct_off, pct_prop])}
    fig_donut = go.Figure(go.Pie(
        labels=[GROUP_LABELS[g.replace("inv_", "")] for g in inv_group_cols],
        values=[norm_pct[g] for g in inv_group_cols],
        hole=0.6,
        marker=dict(colors=[GROUP_COLORS[g.replace("inv_", "")] for g in inv_group_cols],
                    line=dict(color="#0a0907", width=2)),
        textinfo="label+percent", textfont=dict(color=KM_CREAM, size=11),
        hovertemplate="<b>%{label}</b><br>%{percent} · €%{customdata:.0f}k/sem<extra></extra>",
        customdata=[inv_sim[g] / 1e3 for g in inv_group_cols],
        sort=False,
    ))
    fig_donut.add_annotation(
        x=0.5, y=0.5, showarrow=False,
        text=f"<b>€{budget_total/1e3:.0f}k</b><br><span style='font-size:10px;color:#9E9893'>semanal</span>",
        font=dict(size=18, color=KM_GOLD, family="Playfair Display, serif"),
    )
    apply_layout(fig_donut, title="Distribución normalizada del presupuesto", height=340,
                 showlegend=False, margin=dict(t=64, b=20, l=20, r=20))
    st.plotly_chart(fig_donut, width="stretch")

    r_sim  = simular_ic(inv_sim)
    r_ref2 = simular(inv_base_ref)
    lift_e = r_sim["ventas_anual_eur"] - r_ref2["ventas_anual_eur"]
    lift_p = lift_e / r_ref2["ventas_anual_eur"] * 100 if r_ref2["ventas_anual_eur"] else 0
    mroi_s = r_sim["ventas_anual_eur"] / r_sim["inv_total_eur"] if r_sim["inv_total_eur"] > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(kpi_card("Ventas Proyectadas", fmt_eur(r_sim["ventas_anual_eur"]),
                                  f"IC: [{fmt_eur(r_sim['ic_lo_eur'])} – {fmt_eur(r_sim['ic_hi_eur'])}]"), unsafe_allow_html=True)
    with c2:
        dc = KM_SUCCESS if lift_e >= 0 else KM_DANGER
        st.markdown(kpi_card("Lift vs Baseline", f'<span style="color:{dc}">{lift_p:+.1f}%</span>', fmt_eur(lift_e)), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("mROI Proyectado", f"{mroi_s:.1f}x", f"Inversión: {fmt_eur(r_sim['inv_total_eur'])}/año"), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("Riesgo IC 95%", fmt_eur(r_sim["riesgo_eur"]), "Amplitud del intervalo"), unsafe_allow_html=True)

    st.markdown("")
    grps_l = list(channel_groups.keys())
    fig_vs = go.Figure()
    fig_vs.add_trace(go.Bar(
        x=[GROUP_LABELS[g] for g in grps_l],
        y=[inv_base_ref[f"inv_{g}"] * 52 / 1e6 for g in grps_l],
        name="Baseline (M€/año)", marker_color=KM_GRAY, opacity=0.5,
    ))
    fig_vs.add_trace(go.Bar(
        x=[GROUP_LABELS[g] for g in grps_l],
        y=[inv_sim[f"inv_{g}"] * 52 / 1e6 for g in grps_l],
        name="Simulado (M€/año)", marker_color=KM_GOLD,
    ))
    apply_layout(fig_vs, title="Inversión anual: Baseline vs Simulado",
                 yaxis_title="Inversión (M€/año)", height=360, barmode="group")
    st.plotly_chart(fig_vs, width="stretch")

    with st.expander("Informe ejecutivo"):
        best_esc_name = max(esc_results, key=lambda k: esc_results[k]["ventas_anual_eur"])
        best_esc      = esc_results[best_esc_name]
        bl_eur        = best_esc["ventas_anual_eur"] - base_v
        bl_pct        = bl_eur / base_v * 100

        st.markdown(f"""
        <div class="memo-block">
            <p style="font-weight:700; color:{KM_GOLD}; font-size:14px; letter-spacing:1px; margin-bottom:16px; text-transform:uppercase;">
                Memorándum — Comité de Dirección K-Moda
            </p>
            <p><strong>Asunto:</strong> Redistribución presupuestaria basada en Marketing Mix Modeling</p>
            <p><strong>Periodo analizado:</strong> 2020–2024 · 258 semanas · {fmt_eur(ventas_totales)} ventas acumuladas</p>
            <hr style="border-color:rgba(200,169,110,0.15); margin:16px 0;">
            <p>El modelo MMM (R² test = {metrics['test_r2']:.3f}, MAPE = {metrics['test_mape']:.1f}%) confirma que
            el <strong>{pct_mkt:.0f}% de las ventas</strong> es atribuible al marketing, con retorno global
            de <strong>{mroi_global:.1f}x</strong>.
            Canal más eficiente: <strong>{GROUP_LABELS[best_grp]}</strong> ({roi_por_grupo[best_grp]:.1f}x).</p>
            <p>El escenario <strong>{best_esc_name}</strong> proyecta <strong>{fmt_eur(best_esc['ventas_anual_eur'])}</strong>
            en ventas anuales — un incremento de <strong>{bl_pct:+.1f}% ({fmt_eur(bl_eur)})</strong>
            sin aumentar el presupuesto total.</p>
            <p style="margin-top:16px; font-weight:600; color:{KM_GOLD};">
                Recomendación: aprobar la redistribución del escenario {best_esc_name} para el próximo ejercicio fiscal.
            </p>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — EL MODELO
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:

    st.markdown('<p class="section-header">Calidad del Modelo</p>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(kpi_card("R² Train", f"{metrics['train_r2']:.3f}", "Ajuste interno"), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("R² Test",  f"{metrics['test_r2']:.3f}",  "Fuera de muestra"), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("MAPE Test", f"{metrics['test_mape']:.1f}%", "Rango válido: 8–20%"), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("ΔR² Placebo", f"+{metrics['delta_r2_placebo']:.3f}", "Señal real confirmada"), unsafe_allow_html=True)

    st.markdown("")
    st.markdown("""
    <div class="insight-card">
        <h3>Especificaciones técnicas</h3>
        <p>
            <strong>Algoritmo:</strong> ElasticNet con restricción <code>positive=True</code> — contribución ≥ 0 por canal.<br>
            <strong>Features:</strong> 4 logadstock (agrupados) + 4 Fourier + 8 calendario + 3 climáticas = 19 features.<br>
            <strong>Validación:</strong> split estratificado 20% test/año · 500 bootstraps por bloques de 4 semanas.<br>
            <strong>MAPE objetivo:</strong> 8–20%. Por debajo de 8% sería sobreajuste; por encima de 20%, señal no capturada.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Real vs Predicción ──
    st.markdown('<p class="section-header">Ajuste del Modelo · Real vs Predicción</p>', unsafe_allow_html=True)

    dates_all = etl["semana_inicio"]
    fig_fit = go.Figure()
    fig_fit.add_trace(go.Scatter(
        x=dates_all[:n_train], y=y_actual[:n_train] / 1e6,
        name="Real (Train)", mode="lines", line=dict(color=KM_GOLD, width=2),
    ))
    fig_fit.add_trace(go.Scatter(
        x=dates_all[n_train:], y=y_actual[n_train:] / 1e6,
        name="Real (Test)", mode="lines", line=dict(color=KM_GOLD, width=2, dash="dot"),
    ))
    fig_fit.add_trace(go.Scatter(
        x=dates_all[:n_train], y=y_pred_full[:n_train] / 1e6,
        name="Predicción (Train)", mode="lines", line=dict(color=KM_ACCENT, width=2),
    ))
    fig_fit.add_trace(go.Scatter(
        x=dates_all[n_train:], y=y_pred_full[n_train:] / 1e6,
        name="Predicción (Test)", mode="lines", line=dict(color=KM_SUCCESS, width=2),
    ))
    fig_fit.add_vline(x=dates_all.iloc[n_train], line=dict(color=KM_GRAY, dash="dash", width=1))
    split_y = max(y_actual) / 1e6
    for anchor, label in [("right", "TRAIN"), ("left", "TEST")]:
        fig_fit.add_annotation(
            x=dates_all.iloc[n_train], y=split_y, text=label,
            font=dict(size=9, color=KM_GRAY), showarrow=False,
            xanchor=anchor, xshift=-8 if anchor == "right" else 8, yshift=15,
        )
    apply_layout(fig_fit, title="Ventas reales vs predicciones del modelo",
                 yaxis_title="Ventas (M€)", height=440)
    st.plotly_chart(fig_fit, width="stretch")

    with st.expander("Residuos y error porcentual"):
        tr1, tr2 = st.tabs(["Residuos", "APE semanal"])
        with tr1:
            fig_res = go.Figure(go.Bar(
                x=dates_all, y=residuos / 1e6,
                marker_color=[KM_SUCCESS if r >= 0 else KM_DANGER for r in residuos],
                marker_line_width=0,
                hovertemplate="Semana: %{x}<br>Residuo: €%{y:.2f}M<extra></extra>",
            ))
            apply_layout(fig_res, title="Residuos semanales (Real − Predicción)",
                         yaxis_title="Residuo (M€)", height=360)
            st.plotly_chart(fig_res, width="stretch")
        with tr2:
            ape = np.abs(residuos / y_actual) * 100
            fig_ape = go.Figure(go.Scatter(
                x=dates_all, y=ape, mode="lines",
                line=dict(color=KM_GOLD, width=1.5),
                fill="tozeroy", fillcolor="rgba(200,169,110,0.08)",
            ))
            fig_ape.add_hline(y=metrics["test_mape"],
                              line=dict(color=KM_DANGER, dash="dash", width=2),
                              annotation_text=f"MAPE test = {metrics['test_mape']:.1f}%",
                              annotation_font=dict(color=KM_DANGER, size=11))
            apply_layout(fig_ape, title="Error Porcentual Absoluto (APE) semanal",
                         yaxis_title="APE (%)", height=360)
            st.plotly_chart(fig_ape, width="stretch")

    # ── Coeficientes ──
    st.markdown('<p class="section-header">Coeficientes del Modelo</p>', unsafe_allow_html=True)

    coef_data = []
    for feat, coef in zip(feature_cols, model.coef_):
        if coef > 0:
            is_media = feat.startswith("logadstock")
            label = feat.replace("logadstock_", "").replace("_", " ").title()
            coef_data.append({
                "Feature": label, "Coeficiente": coef,
                "Color": KM_GOLD if is_media else KM_GRAY,
            })
    coef_df = pd.DataFrame(coef_data).sort_values("Coeficiente", ascending=True)

    fig_coef = go.Figure(go.Bar(
        y=coef_df["Feature"], x=coef_df["Coeficiente"], orientation="h",
        marker_color=coef_df["Color"],
        text=[f"{v:,.0f}" for v in coef_df["Coeficiente"]],
        textposition="outside", textfont=dict(size=11, color=KM_CREAM),
    ))
    apply_layout(fig_coef, title="Coeficientes activos del modelo (β > 0)",
                 xaxis_title="Coeficiente (€/unidad escalada)",
                 height=max(320, len(coef_df) * 44 + 100))
    st.plotly_chart(fig_coef, width="stretch")
    st.caption("Dorado = Canales de Marketing   ·   Gris = Variables Exógenas (temperatura, festivos, etc.)")

    # ── Simulador adstock ──
    st.markdown('<p class="section-header">Simulador de Adstock · Memoria de Marca</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-card">
        <h3>¿Qué es el adstock?</h3>
        <p>
            La publicidad no desaparece al día siguiente: el consumidor recuerda el anuncio durante semanas.
            <strong>Alpha</strong> controla cuánto dura ese recuerdo (0 = sin memoria, 0.95 = meses);
            <strong>Lag</strong>, cuántas semanas tarda en hacer efecto.
            Email tiene alpha bajo (~0.1); Exterior puede tener alpha alto (~0.7).
        </p>
    </div>
    """, unsafe_allow_html=True)

    col_sl1, col_sl2 = st.columns(2)
    with col_sl1: alpha_sim = st.slider("Alpha · Decaimiento semanal", 0.05, 0.95, 0.50, 0.05, key="alpha_ads")
    with col_sl2: lag_sim   = st.slider("Lag · Semanas de retardo",    0, 4, 1, key="lag_ads")

    n_w   = 20
    decay = np.array([alpha_sim**t for t in range(n_w)])
    hl    = -np.log(2) / np.log(alpha_sim) if alpha_sim > 0 else 0
    accum = np.zeros(n_w)
    for t in range(n_w):
        accum[t] = 1.0 + (alpha_sim * accum[t-1] if t > 0 else 0)
    ss = 1.0 / (1 - alpha_sim) if alpha_sim < 1 else np.inf

    # Usamos los mismos n_w/decay/accum para las dos subplots, más una tercera vista
    # comparando la serie real de un canal raw vs su logadstock (estilo notebook 2).
    col_d, col_a = st.columns(2)
    with col_d:
        fig_dec = go.Figure()
        fig_dec.add_trace(go.Bar(
            x=list(range(n_w)), y=decay,
            marker_color=KM_GOLD, opacity=0.85,
            hovertemplate="Semana %{x}: %{y:.1%}<extra></extra>",
            name="Efecto residual",
        ))
        fig_dec.add_vline(x=hl, line=dict(color=KM_DANGER, dash="dash", width=1.5))
        fig_dec.add_annotation(
            x=hl, y=1.0, text=f"vida media · {hl:.1f} sem",
            font=dict(size=10, color=KM_DANGER), showarrow=False,
            yanchor="bottom", yshift=2, xanchor="left", xshift=4,
        )
        apply_layout(fig_dec, title="Decaimiento del recuerdo publicitario",
                     xaxis_title="Semanas tras el anuncio",
                     yaxis_title="Efecto residual", height=340, showlegend=False)
        fig_dec.update_yaxes(tickformat=".0%", range=[0, 1.12])
        st.plotly_chart(fig_dec, width="stretch")

    with col_a:
        fig_acc = go.Figure(go.Scatter(
            x=list(range(n_w)), y=accum, mode="lines", fill="tozeroy",
            fillcolor="rgba(139,105,20,0.14)",
            line=dict(color=KM_GOLD_DARK, width=2.8, shape="spline"),
            hovertemplate="Semana %{x}: Adstock = %{y:.2f}<extra></extra>",
            name="Adstock acumulado",
        ))
        if ss < 50:
            fig_acc.add_hline(
                y=ss,
                line=dict(color=KM_CREAM, dash="dash", width=1.2),
                annotation_text=f"estado estacionario · {ss:.2f}",
                annotation_position="top right",
                annotation_font=dict(size=10, color=KM_CREAM),
            )
        apply_layout(fig_acc, title="Acumulación con inversión constante",
                     xaxis_title="Semanas de inversión",
                     yaxis_title="Adstock acumulado", height=340, showlegend=False)
        st.plotly_chart(fig_acc, width="stretch")

    # ── Osciloscopio de adstock: pulso + estela ──
    st.markdown(animated_header("Osciloscopio · El Eco de Cada Campaña",
                                label="▶ INTERACTIVO · pulsa Sweep"), unsafe_allow_html=True)

    N_OSC = 36
    pulses = [(3, 1.0), (11, 0.7), (19, 1.3), (27, 0.5)]
    raw_in = np.zeros(N_OSC)
    for idx, mag in pulses:
        if idx < N_OSC:
            raw_in[idx] = mag
    # Aplica adstock con los alpha/lag actuales
    lagged = np.zeros(N_OSC)
    if lag_sim < N_OSC:
        lagged[lag_sim:] = raw_in[:N_OSC - lag_sim]
    adst = np.zeros(N_OSC)
    for t in range(N_OSC):
        adst[t] = lagged[t] + (alpha_sim * adst[t-1] if t > 0 else 0.0)

    fig_osc = make_subplots(
        rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.06,
        subplot_titles=("Impulso de inversión (raw)", "Memoria adstock · eco acumulado"),
    )
    # Línea CRT (sweep) — se moverá con los frames
    fig_osc.add_trace(go.Scatter(
        x=[0, 0], y=[0, max(1.0, raw_in.max() * 1.15)],
        mode="lines", line=dict(color="rgba(200,169,110,0.35)", width=1, dash="dot"),
        hoverinfo="skip", showlegend=False,
    ), row=1, col=1)
    sweep_top_idx = 0

    # Raw (barras stem) — visible hasta la semana actual
    fig_osc.add_trace(go.Bar(
        x=list(range(1)), y=[raw_in[0]], marker_color=KM_CREAM,
        marker_line=dict(color=KM_CREAM, width=2), width=0.35,
        hovertemplate="Semana %{x}: impulso %{y:.2f}<extra></extra>",
        showlegend=False,
    ), row=1, col=1)
    raw_bar_idx = 1

    # Sweep inferior
    fig_osc.add_trace(go.Scatter(
        x=[0, 0], y=[0, max(1.0, adst.max() * 1.15)],
        mode="lines", line=dict(color="rgba(200,169,110,0.35)", width=1, dash="dot"),
        hoverinfo="skip", showlegend=False,
    ), row=2, col=1)
    sweep_bot_idx = 2

    # Adstock (estela) — la onda va creciendo semana a semana
    fig_osc.add_trace(go.Scatter(
        x=[0], y=[adst[0]], mode="lines",
        line=dict(color=KM_GOLD, width=2.6, shape="spline"),
        fill="tozeroy", fillcolor="rgba(200,169,110,0.18)",
        hovertemplate="Semana %{x}: adstock %{y:.2f}<extra></extra>",
        showlegend=False,
    ), row=2, col=1)
    adst_line_idx = 3

    frames_osc = []
    for t in range(1, N_OSC + 1):
        frames_osc.append(go.Frame(
            data=[
                go.Scatter(x=[t-1, t-1], y=[0, max(1.0, raw_in.max() * 1.15)],
                           mode="lines", line=dict(color=KM_CREAM, width=1.4, dash="dot")),
                go.Bar(x=list(range(t)), y=raw_in[:t], marker_color=KM_CREAM,
                       marker_line=dict(color=KM_CREAM, width=2), width=0.35),
                go.Scatter(x=[t-1, t-1], y=[0, max(1.0, adst.max() * 1.15)],
                           mode="lines", line=dict(color=KM_CREAM, width=1.4, dash="dot")),
                go.Scatter(x=list(range(t)), y=adst[:t], mode="lines",
                           line=dict(color=KM_GOLD, width=2.6, shape="spline"),
                           fill="tozeroy", fillcolor="rgba(200,169,110,0.18)"),
            ],
            traces=[sweep_top_idx, raw_bar_idx, sweep_bot_idx, adst_line_idx],
            name=str(t),
        ))
    fig_osc.frames = frames_osc

    apply_layout(fig_osc,
                 height=520, showlegend=False,
                 margin=dict(l=60, r=30, t=90, b=50),
                 title=dict(text="Cada barra = campaña semanal. La onda dorada = memoria residual acumulada.",
                            y=0.98, yanchor="top"))
    for ann in fig_osc.layout.annotations:
        ann.font = dict(color=KM_CREAM, size=11)
        ann.y = ann.y - 0.02 if ann.y is not None else ann.y
    fig_osc.update_xaxes(title_text="Semana", row=2, col=1, range=[-0.5, N_OSC - 0.5])
    fig_osc.update_xaxes(range=[-0.5, N_OSC - 0.5], row=1, col=1)
    fig_osc.update_yaxes(title_text="Impulso", row=1, col=1, range=[0, max(1.0, raw_in.max() * 1.15)])
    fig_osc.update_yaxes(title_text="Adstock", row=2, col=1, range=[0, max(1.0, adst.max() * 1.15)])
    fig_osc.update_layout(updatemenus=[play_button(
        play_label="▶ Sweep", duration=90,
        x=1.0, y=1.08, xanchor="right", yanchor="bottom",
    )])
    fig_osc.add_annotation(**play_hint_annotation(
        text="⚡ Pulsa ▶ Sweep para ver el barrido",
        x=0.02, y=1.08, xref="paper", yref="paper", xanchor="left", yanchor="bottom",
    ))
    st.plotly_chart(fig_osc, width="stretch")
    st.markdown(caption(
        f"Cuatro impulsos de inversión en semanas <b>{', '.join(str(p[0]) for p in pulses)}</b>. "
        f"Con α = <b>{alpha_sim:.2f}</b> y lag = <b>{lag_sim}</b>, cada impulso deja una <b>estela dorada</b> "
        f"que decae exponencialmente y se <b>superpone</b> con el siguiente — por eso las campañas encadenadas "
        f"construyen memoria de marca. Pulsa <b>▶ Sweep</b> para recorrer la línea temporal."
    ), unsafe_allow_html=True)

    # Comparativa real: inversión raw vs logadstock (inspirado en notebook 2)
    st.markdown('<p class="section-header">Transformación real · Raw vs Logadstock</p>', unsafe_allow_html=True)
    canal_opts = {GROUP_LABELS[k]: k for k in [g.replace("inv_", "") for g in inv_group_cols]}
    sel_lab = st.selectbox("Canal", list(canal_opts.keys()), index=0, key="adstock_compare")
    sel_key = canal_opts[sel_lab]
    inv_col = f"inv_{sel_key}"
    log_col = f"logadstock_{sel_key}"

    fig_cmp = make_subplots(
        rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08,
        subplot_titles=(f"Inversión raw · {sel_lab}", f"Logadstock · {sel_lab}"),
    )
    fig_cmp.add_trace(go.Scatter(
        x=dp["semana_inicio"], y=dp[inv_col] / 1e3,
        mode="lines", line=dict(color=GROUP_COLORS[sel_key], width=1.6),
        fill="tozeroy", fillcolor=f"rgba(200,169,110,0.10)",
        hovertemplate="€%{y:.0f}k/sem<extra></extra>", name="raw",
    ), row=1, col=1)
    fig_cmp.add_trace(go.Scatter(
        x=dp["semana_inicio"], y=dp[log_col],
        mode="lines", line=dict(color=KM_GOLD, width=1.6),
        fill="tozeroy", fillcolor=f"rgba(200,169,110,0.14)",
        hovertemplate="%{y:.2f}<extra></extra>", name="logadstock",
    ), row=2, col=1)
    apply_layout(fig_cmp, title="", height=420, showlegend=False)
    fig_cmp.update_yaxes(title_text="€k / sem", row=1, col=1)
    fig_cmp.update_yaxes(title_text="logadstock", row=2, col=1)
    fig_cmp.update_annotations(font=dict(color=KM_GOLD, size=12))
    st.plotly_chart(fig_cmp, width="stretch")
    st.markdown(caption(
        "Arriba: inversión semanal cruda (lo que se pagó). "
        "Abajo: tras aplicar adstock + saturación log — así es como el modelo 've' el canal. "
        "Las caídas se suavizan por el recuerdo; los picos se aplanan por rendimientos decrecientes."
    ), unsafe_allow_html=True)

    if alpha_sim < 0.30:
        mem = "**corta** — efecto se disipa rápidamente. Típico de Paid Search, Email."
    elif alpha_sim < 0.60:
        mem = "**media** — recuerdo dura varias semanas. Típico de Display, Video Online."
    else:
        mem = "**larga** — impacto persiste meses. Típico de Radio, Exterior, Prensa."
    st.info(f"Con Alpha = {alpha_sim:.2f} la memoria de marca es {mem} Vida media: **{hl:.1f} semanas**.")

    with st.expander("Fórmulas matemáticas"):
        st.latex(r"Adstock_t = x_t + \alpha \cdot Adstock_{t-1}")
        st.latex(r"Saturacion(A) = \log\!\left(1 + \frac{A}{k}\right)")
        st.latex(r"\hat{y}_t = \beta_0 + \sum_j \beta_j \cdot Saturacion(Adstock_j)_t + \sum_k \gamma_k Z_{k,t}")
        st.markdown("- **Alpha** = factor de decaimiento (0 = sin memoria, 1 = permanente)\n"
                    "- **k** = punto de saturación (percentil 60 del adstock positivo)\n"
                    "- **β** = coeficientes de medios (restringidos ≥ 0)\n"
                    "- **γ** = coeficientes de variables de control")

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