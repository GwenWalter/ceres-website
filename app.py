import base64
from pathlib import Path

import requests
import streamlit as st
import plotly.graph_objects as go

########### CONSTANTES ###########

HARVEST_YEAR = 2025
GEOJSON_URL = (
    "https://raw.githubusercontent.com/gregoiredavid/france-geojson/"
    "master/departements-version-simplifiee.geojson"
)
EXCLUDED_DEPTS = {"2A", "2B"}  # Corse — hors périmètre démo
BACKGROUND_FILE = Path(__file__).parent / "ceres_fond.png"

CERES_ICON_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" style="height:0.9em;width:auto;vertical-align:-0.08em;margin-right:0.15em;"><g stroke="#1B4332" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M32 56V14"/><path d="M32 18c-6 0-10-4-10-10 6 0 10 4 10 10Z"/><path d="M32 26c-6 0-10-4-10-10 6 0 10 4 10 10Z"/><path d="M32 34c-6 0-10-4-10-10 6 0 10 4 10 10Z"/><path d="M32 42c-6 0-10-4-10-10 6 0 10 4 10 10Z"/><path d="M32 18c6 0 10-4 10-10-6 0-10 4-10 10Z"/><path d="M32 26c6 0 10-4 10-10-6 0-10 4-10 10Z"/><path d="M32 34c6 0 10-4 10-10-6 0-10 4-10 10Z"/><path d="M32 42c6 0 10-4 10-10-6 0-10 4-10 10Z"/><path d="M32 56c-6-2-10-6-12-12"/></g></svg>'
)

########### PAGE CONFIG (premier appel st.*) ###########

_ICON_FILE = Path(__file__).parent / "ceres_icon.png"
st.set_page_config(
    page_title="Ceres AI · Récolte 2025",
    page_icon=str(_ICON_FILE) if _ICON_FILE.exists() else "🌾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

########### FOND — CERES EN FILIGRANE ###########


@st.cache_data
def load_background_css() -> str:
    """Encode le PNG filigrane en base64 et le pose en fond fixe, pleine page (contain), voilé de blanc."""
    if not BACKGROUND_FILE.exists():
        return ""
    b64 = base64.b64encode(BACKGROUND_FILE.read_bytes()).decode()
    return f"""
.stApp {{
    background-image:
        linear-gradient(rgba(250,250,248,0.78), rgba(250,250,248,0.78)),
        url("data:image/png;base64,{b64}");
    background-repeat: no-repeat, no-repeat;
    background-position: center center, center center;
    background-attachment: fixed, fixed;
    background-size: cover, contain;
}}
.stApp::before {{
    content: "";
    position: fixed;
    inset: 0;
    background: rgba(255,255,255,0.45);
    z-index: 0;
    pointer-events: none;
}}
.main .block-container {{ position: relative; z-index: 1; }}
"""


########### CSS — Ceres Light ###########

CERES_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700&family=DM+Sans:wght@400;500;700&display=swap');

/* ── page ── */
.stApp {{ background-color: #FAFAF8; }}
{load_background_css()}
.main .block-container {{
    max-width: 1280px;
    padding-top: 2.2rem;
    font-family: 'DM Sans', sans-serif;
    color: #1B4332;
}}
#MainMenu, footer, header {{ visibility: hidden; }}

/* ── hero ── */
p.ceres-hero, .ceres-hero {{
    font-family: 'Fraunces', serif !important;
    font-size: clamp(2.6rem, 5vw, 4.2rem) !important;
    font-weight: 700 !important;
    letter-spacing: -2px !important;
    color: #1B4332 !important;
    text-align: center !important;
    margin-bottom: 0.3rem !important;
    line-height: 1.05 !important;
    text-shadow: 0 1px 0 rgba(250,250,248,0.9);
}}
.ceres-sub {{
    font-size: 1.7rem;
    color: #6B7B6E;
    text-align: center;
    margin-bottom: 1rem;
}}

/* ── millésime — étiquette éditoriale, pas un filtre ── */
.ceres-season {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 1.6rem;
}}
.ceres-season::before,
.ceres-season::after {{
    content: "";
    height: 1px;
    width: 88px;
    background: linear-gradient(90deg, transparent, #C9A961, transparent);
}}
.ceres-season-text {{
    font-family: 'Fraunces', serif;
    font-size: 1.2rem;
    font-weight: 600;
    font-style: italic;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #B08D3E;
    white-space: nowrap;
}}

/* ── hint vide ── */
.ceres-hint {{
    text-align: center;
    color: #6B7B6E;
    font-size: 0.95rem;
    margin: 0.6rem 0 0.2rem;
}}

/* ── map container ── */
[data-testid="stPlotlyChart"] {{
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #ECE9DF;
    background: rgba(250, 250, 248, 0.72);
}}

/* ── floating result card ── */
.ceres-card {{
    position: fixed;
    right: 2.2rem;
    bottom: 2.2rem;
    z-index: 999;
    width: 400px;
    box-sizing: border-box;
    background: #FFFFFF;
    border: 1.5px solid #FAF3DD;
    border-radius: 22px;
    padding: 2rem 2.2rem;
    box-shadow: 0 12px 44px rgba(27,67,50,0.22);
    animation: ceres-rise 0.35s cubic-bezier(.2,.8,.3,1);
    overflow-wrap: break-word;
}}
@keyframes ceres-rise {{
    from {{ opacity: 0; transform: translateY(14px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
.ceres-card-dept {{
    font-family: 'Fraunces', serif;
    font-size: 1.9rem;
    font-weight: 600;
    color: #1B4332;
    line-height: 1.1;
}}
.ceres-card-badge {{
    font-size: 1rem;
    color: #B08D3E;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    margin-bottom: 1.2rem;
}}
.ceres-metric-label {{ font-size: 1.25rem; color: #6B7B6E; margin: 0.8rem 0 0; }}
.ceres-metric-value {{
    font-size: 1.9rem !important;
    font-weight: 700 !important;
    font-variant-numeric: tabular-nums;
    line-height: 1.15 !important;
}}
.ceres-metric-value--pred {{ color: #40916C; }}
.ceres-metric-value--reel {{ color: #D4A373; }}
.ceres-metric-value--ecart {{ color: #1B4332; font-size: 1.6rem !important; }}
.ceres-unit {{ font-size: 1.9rem; font-weight: 400; color: #6B7B6E; }}
.ceres-metric-value--ecart .ceres-unit {{ font-size: 1.6rem; }}

/* ── comparison bars ── */
.ceres-bar-track {{
    background: #F1EFE7;
    border-radius: 8px;
    height: 20px;
    margin: 0.5rem 0 0.25rem;
    overflow: hidden;
}}
.ceres-bar-pred, .ceres-bar-reel {{
    height: 100%;
    border-radius: 8px;
    transition: width 0.6s cubic-bezier(.2,.8,.3,1);
}}
.ceres-bar-pred {{ background: #40916C; }}
.ceres-bar-reel {{ background: #D4A373; }}
.ceres-bar-caption {{ font-size: 1rem; color: #6B7B6E; }}

/* ── footer ── */
.ceres-footer {{
    text-align: center;
    color: #6B7B6E;
    font-size: 0.75rem;
    margin-top: 2rem;
}}

/* ── mobile : carte flottante → bloc sous la carte ── */
@media (max-width: 900px) {{
    .ceres-card {{
        position: static;
        width: 100%;
        margin-top: 1rem;
        animation: none;
    }}
    .ceres-sub {{ font-size: 1.25rem; }}
    .ceres-metric-value {{ font-size: 2.8rem; }}
}}
</style>
"""
st.markdown(CERES_CSS, unsafe_allow_html=True)

########### DONNEES — GEOJSON DEPARTEMENTS ###########


@st.cache_data(ttl=86400, show_spinner="Chargement de la carte de France…")
def load_geojson():
    resp = requests.get(GEOJSON_URL, timeout=30)
    resp.raise_for_status()
    geo = resp.json()
    geo["features"] = [
        f for f in geo["features"]
        if f["properties"]["code"] not in EXCLUDED_DEPTS
    ]
    return geo


########### API — UN APPEL PAR DEPARTEMENT (lazy + cache) ###########


@st.cache_data(show_spinner=False)
def fetch_prediction(dept_code: str, year: int, api_base: str):
    """Retourne (prediction, reel) en q/ha. Les erreurs ne sont pas mises en cache."""
    # L'API stocke DEPT_ID en entier : "01" -> "1", sinon 404 sur les dépts 01-09
    resp = requests.get(
        f"{api_base}/predict",
        params={"DEPT_ID": dept_code.lstrip("0"), "harvest_year": year},
        timeout=120,
    )
    resp.raise_for_status()
    data = resp.json()
    return float(data["prediction"]), float(data["reel"])


########### SESSION STATE ###########

if "dept_id" not in st.session_state:
    st.session_state.dept_id = None
if "ecarts" not in st.session_state:
    st.session_state.ecarts = {}
if "ecarts_done" not in st.session_state:
    st.session_state.ecarts_done = False

geojson = load_geojson()
codes = [f["properties"]["code"] for f in geojson["features"]]
names = {f["properties"]["code"]: f["properties"]["nom"] for f in geojson["features"]}

if "API_URL" not in st.secrets:
    st.error(
        "Secret `API_URL` manquant. Ajoutez-le dans `.streamlit/secrets.toml` "
        "(local) ou dans les secrets Streamlit Cloud."
    )
    st.stop()

api_url = st.secrets["API_URL"].rstrip("/")


def norm_dept(code):
    """Plotly renvoie souvent un int (51) — nos clés GeoJSON sont des str ("51", "01")."""
    if code is None:
        return None
    s = str(code).strip()
    if s in names:
        return s
    if s.isdigit():
        padded = s.zfill(2)
        if padded in names:
            return padded
    return None

########### SIDEBAR — ANCRES DE CONFIANCE ###########

with st.sidebar:
    st.markdown("### Ceres AI")
    st.markdown(
        '<div class="ceres-season" style="justify-content:flex-start">'
        '<span class="ceres-season-text">Récolte 2025</span></div>',
        unsafe_allow_html=True,
    )
    st.divider()
    if st.button("Tester l'API", use_container_width=True):
        test_dept = (st.session_state.dept_id or "51").lstrip("0")
        test_url = (
            f"{api_url}/predict?DEPT_ID={test_dept}&harvest_year={HARVEST_YEAR}"
        )
        try:
            r = requests.get(
                f"{api_url}/predict",
                params={"DEPT_ID": test_dept, "harvest_year": HARVEST_YEAR},
                timeout=30,
            )
            st.caption(f"`GET {test_url}`")
            st.caption(f"HTTP **{r.status_code}**")
            st.code(r.text[:500] or "(vide)", language="json")
        except requests.exceptions.RequestException as err:
            st.caption(f"`GET {test_url}`")
            st.error(f"{err.__class__.__name__}: {err}")

########### HERO ###########

st.markdown(
    '<p class="ceres-hero">' + CERES_ICON_SVG + 'Ceres AI</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="ceres-sub">Prédiction du rendement de blé tendre par département</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="ceres-season"><span class="ceres-season-text">Récolte 2025</span></div>',
    unsafe_allow_html=True,
)

########### MODE ECART (HEATMAP) ###########

_, col_toggle = st.columns([3, 2])
with col_toggle:
    heatmap_on = st.toggle("Colorer la carte par écart prédit − réel", value=False)

if heatmap_on and not st.session_state.ecarts_done:
    progress = st.progress(0, text=f"Chargement des écarts — 0/{len(codes)} départements…")
    for i, code in enumerate(codes):
        try:
            pred, reel = fetch_prediction(code, HARVEST_YEAR, api_url)
            st.session_state.ecarts[code] = pred - reel
        except requests.exceptions.RequestException:
            pass
        progress.progress(
            (i + 1) / len(codes),
            text=f"Chargement des écarts — {i + 1}/{len(codes)} départements…",
        )
    progress.empty()
    st.session_state.ecarts_done = True

if heatmap_on and st.session_state.ecarts_done and not st.session_state.ecarts:
    st.warning("Écarts indisponibles — modèle 2025 en cours de déploiement.")
    if st.button("Réessayer le chargement des écarts"):
        st.session_state.ecarts_done = False
        st.rerun()

########### CARTE DE FRANCE ###########

fig = go.Figure()

# Trace de base : tous les départements (une seule trace = clics fiables)
selected = st.session_state.dept_id
fig.add_trace(
    go.Choropleth(
        geojson=geojson,
        locations=codes,
        featureidkey="properties.code",
        z=[0] * len(codes),
        colorscale=[[0, "#F1EFE7"], [1, "#F1EFE7"]],
        showscale=False,
        marker_line_color=[
            "#FFD95A" if c == selected else "#6B7B6E" for c in codes
        ],
        marker_line_width=[
            3 if c == selected else 0.7 for c in codes
        ],
        customdata=[names[c] for c in codes],
        hovertemplate="<b>%{customdata} (%{location})</b><extra></extra>",
        name="departements",
    )
)

# Trace heatmap : uniquement les départements avec un écart connu
if heatmap_on and st.session_state.ecarts:
    hm_codes = [c for c in codes if c in st.session_state.ecarts]
    hm_vals = [st.session_state.ecarts[c] for c in hm_codes]
    fig.add_trace(
        go.Choropleth(
            geojson=geojson,
            locations=hm_codes,
            featureidkey="properties.code",
            z=hm_vals,
            zmid=0,
            colorscale=[
                [0.0, "#C44536"],   # sous-estimé (prédit < réel) → rouge
                [0.35, "#E8A87C"],
                [0.5, "#40916C"],   # écart ≈ 0 → vert (bonne prédiction)
                [0.65, "#7FA8C9"],
                [1.0, "#2C5F8A"],   # surestimé (prédit > réel) → bleu
            ],
            marker_line_color="#6B7B6E",
            marker_line_width=0.7,
            colorbar=dict(
                title=dict(text="Écart prédit − réel (q/ha)", font=dict(size=12, color="#1B4332")),
                tickfont=dict(size=11, color="#1B4332"),
                thickness=12,
                len=0.7,
                x=-0.06,
                xanchor="left",
            ),
            customdata=[names[c] for c in hm_codes],
            hovertemplate="<b>%{customdata} (%{location})</b><br>Écart : %{z:+.1f} q/ha<extra></extra>",
            name="ecarts",
        )
    )

fig.update_geos(
    fitbounds="locations",
    visible=False,
    bgcolor="rgba(0,0,0,0)",
    projection_type="mercator",
)
fig.update_layout(
    height=720,
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor="rgba(0,0,0,0)",
    dragmode=False,
    font=dict(family="DM Sans, sans-serif", color="#1B4332"),
)

event = st.plotly_chart(
    fig,
    width="stretch",
    on_select="rerun",
    selection_mode="points",
    config={"scrollZoom": False, "displayModeBar": False},
    key="france_map",
)

# Clic carte → département sélectionné
map_sel = None
if event and event.selection and event.selection.get("points"):
    point = event.selection["points"][0]
    map_sel = point.get("location")
    if map_sel is None and point.get("customdata") in names.values():
        for c, n in names.items():
            if n == point.get("customdata"):
                map_sel = c
                break
    if map_sel is None and "pointNumber" in point:
        curve = point.get("curveNumber", 0)
        idx = point["pointNumber"]
        if curve == 0 and 0 <= idx < len(codes):
            map_sel = codes[idx]
        elif heatmap_on and st.session_state.ecarts:
            hm_codes = [c for c in codes if c in st.session_state.ecarts]
            if curve == 1 and 0 <= idx < len(hm_codes):
                map_sel = hm_codes[idx]

dept_from_map = norm_dept(map_sel)
if dept_from_map and dept_from_map != st.session_state.dept_id:
    st.session_state.dept_id = dept_from_map
    st.rerun()

########### ACCES RAPIDE — CHIPS ###########

st.markdown("**Accès rapide**")
chip_filter = st.text_input(
    "Filtrer un département",
    placeholder="Filtrer un département… (nom ou numéro)",
    label_visibility="collapsed",
    key="chip_filter",
)
chip_options = [f"{c} {names[c]}" for c in codes]
if chip_filter:
    needle = chip_filter.strip().lower()
    chip_options = [o for o in chip_options if needle in o.lower()]

if chip_options:
    chip = st.pills(
        "Accès rapide",
        chip_options,
        selection_mode="single",
        label_visibility="collapsed",
        key="chips",
    )
    if chip:
        chip_code = norm_dept(chip.split(" ", 1)[0])
        if chip_code and chip_code != st.session_state.dept_id:
            st.session_state.dept_id = chip_code
            st.rerun()
else:
    st.caption("Aucun département ne correspond au filtre.")

########### RESULTAT — CARTE FLOTTANTE ###########

dept = st.session_state.dept_id

if dept is None:
    st.markdown(
        '<p class="ceres-hint">✦ Cliquez un département pour comparer prédiction et réel. '
        "La carte attend votre premier clic — chaque terroir a son chiffre.</p>",
        unsafe_allow_html=True,
    )
else:
    result = None
    with st.spinner("Appel API Ceres en cours… Premier appel : jusqu'à 1 minute, le modèle se réveille."):
        try:
            result = fetch_prediction(dept, HARVEST_YEAR, api_url)
        except requests.exceptions.HTTPError as err:
            status = err.response.status_code if err.response is not None else None
            if status == 404:
                st.warning(
                    f"Pas de données pour le département {dept} "
                    f"en récolte {HARVEST_YEAR}."
                )
            elif status == 500:
                req_url = (
                    f"{api_url}/predict?DEPT_ID={dept}&harvest_year={HARVEST_YEAR}"
                )
                st.error(
                    "Erreur serveur GCP (HTTP 500) — le modèle plante sur `model.predict()` "
                    "(colonnes features du CSV X_test ≠ modèle déployé). "
                    "Ce n'est pas un bug Streamlit : l'API doit être redéployée."
                )
                st.caption(f"Requête envoyée : `{req_url}`")
                st.caption(
                    "Vérifiez la même URL dans "
                    "[Swagger](https://ceres-332649143814.europe-west1.run.app/docs). "
                    "Utilisez **Tester l'API** dans la barre latérale."
                )
            else:
                st.error(f"L'API Ceres a renvoyé une erreur (HTTP {status}).")
        except requests.exceptions.Timeout:
            st.error(
                "L'API Ceres met trop de temps à répondre (> 2 min). "
                "Réessayez dans un instant."
            )
        except requests.exceptions.RequestException as err:
            st.error(
                f"Impossible de joindre l'API Ceres ({err.__class__.__name__}). "
                "Vérifiez votre connexion, puis recliquez le département."
            )

    if result is not None:
        prediction, reel = result
        ecart = prediction - reel
        erreur_pct = (ecart / reel) * 100 if reel else 0.0
        bar_max = max(prediction, reel) or 1.0
        w_pred = prediction / bar_max * 100
        w_reel = reel / bar_max * 100

        st.markdown(
            f"""
            <div class="ceres-card">
              <div class="ceres-card-dept">{names[dept]} ({dept})</div>
              <div class="ceres-card-badge">Récolte {HARVEST_YEAR}</div>
              <p class="ceres-metric-label">Prédit</p>
              <p class="ceres-metric-value ceres-metric-value--pred">{prediction:.1f} <span class="ceres-unit">q/ha</span></p>
              <p class="ceres-metric-label">Réel</p>
              <p class="ceres-metric-value ceres-metric-value--reel">{reel:.1f} <span class="ceres-unit">q/ha</span></p>
              <p class="ceres-metric-label">Écart</p>
              <p class="ceres-metric-value ceres-metric-value--ecart">{ecart:+.1f} q/ha <span class="ceres-unit">({erreur_pct:+.1f} %)</span></p>
              <div class="ceres-bar-track"><div class="ceres-bar-pred" style="width:{w_pred:.0f}%"></div></div>
              <p class="ceres-bar-caption">Prédit</p>
              <div class="ceres-bar-track"><div class="ceres-bar-reel" style="width:{w_reel:.0f}%"></div></div>
              <p class="ceres-bar-caption">Réel</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

########### FOOTER ###########

st.markdown(
    '<p class="ceres-footer">Ceres AI — démo · données Agreste · modèle servi sur Cloud Run</p>',
    unsafe_allow_html=True,
)
