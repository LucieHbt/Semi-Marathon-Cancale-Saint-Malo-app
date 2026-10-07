"""Données chronométriques – semi Cancale Saint-Malo, 2022 à 2026 (Streamlit) """
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

DATA = Path(__file__).parent / "data" / "resultats.csv"

# Palette
FOND, TEAL, ROUGE = "#0F2B30", "#3AB5B0", "#C24247"
OR, ARGENT, BRONZE = "#E0B400", "#9A9A9A", "#E8743B"
SEXES = {"Homme": "Hommes", "Femme": "Femmes"}

st.set_page_config(page_title="Statistiques - Semi-Marathon Cancale Saint-Malo", page_icon="🏁", layout="wide")

st.markdown(
    f"""
    <style>

    .stApp {{background:linear-gradient(rgba(1,114,132,.40),rgba(13,43,48,.60)),
    url("https://semicancalestmalo.fr/assets/victoire.jpg") center / cover fixed no-repeat;}}

    header[data-testid="stHeader"] {{background: transparent;}}

    .st-emotion-cache-lhe5w4 {{padding: 1rem 1rem 1rem;}}

    .stApp [data-testid="stCaptionContainer"],
    .stApp [data-testid="stCaptionContainer"] * {{color: rgba(255,255,255,.70);}}
    .stApp [data-testid="stWidgetLabel"] p {{color: white;font-weight: 600;}}

    .st-key-bandeau {{
        color: white;
        border-radius: 14px;
        padding: 16px 22px 24px 22px;
        background:
            linear-gradient(90deg,{TEAL},{ROUGE})
            bottom / 100% 3px no-repeat,
            rgba(15,43,48,.92);
        backdrop-filter: blur(6px);
        box-shadow: 0 8px 22px rgba(0,0,0,.25);

        display: flex;
        align-items: center;
        width: 100%;
    }}

    /* Logo + texte */

    .st-key-bandeau .hero {{display: flex;align-items: center;gap: 12px;}}
    .st-key-bandeau .hero-logo {{width: 44px;height: 44px;object-fit: contain;}}
    .st-key-bandeau .hero-text {{display: flex;flex-direction: column;text-align: left;}}
    .st-key-bandeau .hero-title {{color: #fff;font-size: 1.5rem;font-weight: 700;}}
    .st-key-bandeau .hero-subtitle {{color: rgba(255,255,255,.70);font-size: 1.2rem;}}
    .st-key-bandeau .h {{color: #fff;font-size: 1.5rem;font-weight: 700;line-height: 1.15;margin: 0;padding: 0;}}
    .st-key-bandeau .kicker {{color: rgba(255,255,255,.70);font-size: .85rem;font-weight: 400;line-height: 1.2;margin: 4px 0 0 0;padding: 0;letter-spacing: normal;text-transform: none;}}

    .st-key-bandeau label {{color: white;}}

    .st-key-bandeau [role="radiogroup"] {{
        background: rgba(255,255,255,.07);
        border: 1px solid rgba(255,255,255,.12);
        border-radius: 999px;
        padding: 4px;
        gap: 2px;
        width: fit-content;
        margin-left: auto;
    }}

    .st-key-bandeau button[role="radio"] {{
        background: transparent !important;
        border: 0 !important;
        border-radius: 999px !important;
        padding: 6px 20px;
        transition: all .18s ease;
    }}

    .st-key-bandeau button[role="radio"] * {{
        color: rgba(255,255,255,.65) !important;
        font-weight: 500;
    }}

    .st-key-bandeau button[role="radio"]:hover {{
        background: rgba(255,255,255,.12) !important;
    }}

    .st-key-bandeau button[role="radio"]:hover * {{
        color: #fff !important;
    }}

    .st-key-bandeau button[role="radio"][aria-checked="true"] {{
        background: linear-gradient(
            135deg,
            {TEAL},
            #2A8F9B
        ) !important;
        box-shadow: 0 3px 10px rgba(58,181,176,.45);
    }}

    .st-key-bandeau button[role="radio"][aria-checked="true"] * {{
        color: #fff !important;
    }}

    .st-key-bandeau [data-testid="stColumn"]:last-child {{
        display: flex;
        align-items: center;
        justify-content: flex-end;
    }}

    .st-key-bandeau [data-testid="stColumn"]:last-child
    [data-testid="stElementContainer"] {{
        width: 100%;
        display: flex;
        justify-content: flex-end;
    }}

    .st-key-bandeau [data-testid="stButtonGroup"] {{
        background: transparent;
        width: fit-content;
    }}


    /* =========================
       MOBILE
       ========================= */

    @media (max-width: 640px) {{

        .st-key-bandeau {{
            padding: 12px 14px 18px 14px;
        }}

        .st-key-bandeau .hero {{
            gap: 9px;
        }}

        .st-key-bandeau .hero-logo {{
            width: 36px;
            height: 36px;
        }}

        .st-key-bandeau .h {{
            font-size: 1.15rem;
        }}

        .st-key-bandeau .kicker {{
            font-size: .75rem;
        }}

        .st-key-bandeau button[role="radio"] {{
            padding: 6px 12px;
        }}

        .st-key-bandeau [data-testid="stColumn"]:last-child
        [data-testid="stElementContainer"],
        .st-key-bandeau [data-testid="stButtonGroup"] {{
            width: 100%;
        }}

        .st-key-bandeau [role="radiogroup"] {{
            width: 100%;
            justify-content: space-between;
        }}
    }}


    /* =========================
       KPI
       ========================= */

    .kpi-card {{
        display: flex;
        align-items: center;
        gap: 16px;
        background: #fff;
        border: 3px solid var(--c);
        border-radius: 14px;
        padding: 16px 20px;
        box-shadow: 0 8px 22px rgba(0,0,0,.28);
        font-family: 'Poppins', sans-serif;
    }}

    .kpi-ico {{
        flex: none;
        width: 58px;
        height: 58px;
        border-radius: 50%;
        background: var(--c);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.7rem;
        box-shadow: 0 3px 8px rgba(0,0,0,.25);
    }}

    .kpi-lab {{
        color: #6b6b6b;
        font-size: .72rem;
        font-weight: 600;
        letter-spacing: .06em;
        text-transform: uppercase;
    }}

    .kpi-val {{
        color: #0B3A4F;
        font-size: 2.1rem;
        font-weight: 800;
        line-height: 1.1;
    }}

    .kpi-moy {{
        color: #6b6b6b;
        font-size: .8rem;
        margin-top: 2px;
    }}

    .kpi-moy b {{
        color: #0B3A4F;
        font-weight: 800;
        font-size: .95rem;
        padding-left: 4px;
    }}


    /* =========================
       DISTRIBUTION
       ========================= */

    .st-key-distrib {{
        background: rgba(15,43,48,.62);
        backdrop-filter: blur(4px);
        border-radius: 0 0 12px 12px;
        padding: 10px 14px 6px 14px;
        margin-top: 0;
    }}

    .st-key-distrib div[data-testid="stPlotlyChart"] {{
        background: transparent;
        border-radius: 0;
    }}


    /* =========================
       FILTRES CATÉGORIES
       ========================= */

    .st-key-pills_cat button[role="radio"] {{
        background: rgba(15,43,48,.55) !important;
        border: 1px solid rgba(255,255,255,.28) !important;
        border-radius: 999px !important;
        backdrop-filter: blur(4px);
        transition: all .15s ease;
    }}

    .st-key-pills_cat button[role="radio"] * {{
        color: rgba(255,255,255,.85) !important;
    }}

    .st-key-pills_cat button[role="radio"]:hover {{
        border-color: rgba(255,255,255,.7) !important;
        background: rgba(255,255,255,.12) !important;
    }}

    .st-key-pills_cat button[role="radio"][aria-checked="true"] {{
        background: rgba(255,255,255,.22) !important;
        border: 1px solid #fff !important;
    }}

    .st-key-pills_cat button[role="radio"][aria-checked="true"] * {{
        color: #fff !important;
        font-weight: 700;
    }}


    /* =========================
       TITRES DE SECTIONS
       ========================= */

    .titre {{
        display: flex;
        align-items: center;
        gap: 12px;
        background: rgba(15,43,48,.92);
        backdrop-filter: blur(4px);
        border-radius: 12px 12px 0 0;
        padding: 9px 16px;
        box-shadow: inset 0 -3px 0 var(--c);
        font-family: 'Poppins', sans-serif;
    }}

    .titre .ico {{
        flex: none;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: var(--c);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        line-height: 1;
        color: #fff;
        font-weight: 700;
        box-shadow: 0 2px 6px rgba(0,0,0,.3);
    }}

    .titre .tt {{
        color: #fff;
        font-size: 1rem;
        font-weight: 700;
        letter-spacing: .02em;
    }}

    .titre .ss {{
        color: rgba(255,255,255,.6);
        font-size: .72rem;
        font-weight: 400;
        margin-top: -1px;
    }}

    .titre .chip {{
        margin-left: auto;
        color: #fff;
        font-size: .72rem;
        font-weight: 600;
        padding: 3px 12px;
        border-radius: 999px;
        background: rgba(255,255,255,.1);
        border: 1px solid rgba(255,255,255,.22);
        white-space: nowrap;
    }}


    /* =========================
       PODIUM
       ========================= */

    @import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,400;0,600;1,800&display=swap');

    .pod-wrap {{
        display: flex;
        align-items: flex-end;
        gap: 14px;
        padding: 22px 14px 16px 14px;
        background: rgba(15,43,48,.62);
        backdrop-filter: blur(4px);
        border-radius: 0 0 10px 10px;
        min-height: 340px;
        box-sizing: border-box;
        font-family: 'Poppins', sans-serif;
    }}

    .pod-vide {{
        justify-content: center;
        align-items: center;
        color: rgba(255,255,255,.8);
    }}

    .pod-col {{
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 14px;
        min-width: 0;
    }}

    .pod-card {{
        background: #fff;
        border: 3px solid var(--c);
        border-radius: 14px;
        padding: 16px 8px 10px 8px;
        text-align: center;
        box-sizing: border-box;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        box-shadow: 0 8px 22px rgba(0,0,0,.28);
    }}

    .pod-card.p1 {{
        height: 300px;
        padding-top: 22px;
        box-shadow: 0 12px 30px rgba(0,0,0,.38);
    }}

    .pod-card.p2 {{
        height: 262px;
    }}

    .pod-card.p3 {{
        height: 224px;
    }}

    .pod-medal {{
        flex: none;
        width: 58px;
        height: 58px;
        margin: 0 auto 10px auto;
        border-radius: 50%;
        background: var(--c);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 3px 8px rgba(0,0,0,.25);
    }}

    .pod-card.p1 .pod-medal {{
        width: 78px;
        height: 78px;
    }}

    .pod-nom {{
        color: #0B3A4F;
        font-weight: 800;
        font-style: italic;
        text-transform: uppercase;
        font-size: .88rem;
        line-height: 1.15;
        overflow-wrap: anywhere;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }}

    .pod-card.p1 .pod-nom {{
        font-size: 1rem;
    }}

    .pod-club {{
        color: #6b6b6b;
        font-size: .68rem;
        text-transform: uppercase;
        margin-top: 6px;
        line-height: 1.2;
        overflow-wrap: anywhere;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }}

    .pod-meta {{
        color: #6b6b6b;
        font-size: .75rem;
        margin-top: 4px;
    }}

    .pod-meta i {{
        color: {TEAL};
        font-style: normal;
        font-weight: 600;
        padding: 0 2px;
    }}

    .pod-temps {{
        color: #0B3A4F;
        font-weight: 800;
        font-size: 1.25rem;
        margin-top: 10px;
    }}

    .pod-card.p1 .pod-temps {{
        font-size: 1.5rem;
    }}

    div[data-testid="stPlotlyChart"] {{
        background: white;
        border-radius: 0 0 10px 10px;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
@st.cache_data
def charger() -> pd.DataFrame:
    df = pd.read_csv(DATA).fillna({"Club": "", "Cat": ""})
    # 2022-2025 : catégorie suffixée par le sexe (M0H, SEF...) -> on retire le suffixe
    df["Cat"] = df["Cat"].str.replace(r"^(\w{2})[HF]$", r"\1", regex=True)
    return df


ORDRE_CAT = ["CA", "JU", "ES", "SE"] + [f"M{i}" for i in range(10)]


def hms(s: float) -> str:
    if pd.isna(s):
        return "–"
    s = int(round(s))
    return f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}"


ICO_F = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.4" stroke-linecap="round"><circle cx="12" cy="9" r="5.5"/><path d="M12 14.5V22M8.5 18.5h7"/></svg>'
ICO_H = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><circle cx="10" cy="14" r="5.5"/><path d="M14 10l6-6M14.5 4H20v5.5"/></svg>'

df = charger()
annees = sorted(df["Annee"].unique())

# ----------------------------------------------------------------------------
# Bandeau : titre, onglets d'année, indicateurs
# ----------------------------------------------------------------------------
with st.container(key="bandeau"):
    c_titre, c_annee = st.columns([1.6, 1], vertical_alignment="center")
    c_titre.markdown(
        f"""
        <div class="hero">
            <img
                src="https://semicancalestmalo.fr/assets/logo.png"
                class="hero-logo">
            <div class="hero-text">
                <div class="hero-title">Semi-Marathon Cancale-Saint-Malo</div>
                <div class="hero-subtitle">Statistiques chronométriques</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with c_annee:
        annee = st.segmented_control("Édition",annees,default=annees[-1],label_visibility="collapsed") or annees[-1]

d = df[df["Annee"] == annee]
arr = d[d["Temps_s"].notna()]

def titre(icone: str, texte: str, sous: str = "", puce: str = "", couleur: str = "white") -> str:
    sous_html = f"<div class='ss'>{sous}</div>" if sous else ""
    puce_html = f"<span class='chip'>{puce}</span>" if puce else ""
    return (
        f"<div class='titre' style='--c:{couleur}'><div class='ico'>{icone}</div>"
        f"<div><div class='tt'>{texte}</div>{sous_html}</div>{puce_html}</div>"
    )

MEDAILLE = (
    '<svg width="{t}" height="{t}" viewBox="0 0 24 24" fill="none" stroke="white" '
    'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M7.2 3h9.6l1.4 5H5.8z"/><circle cx="12" cy="14.5" r="5.5"/>'
    '<path d="M12 11.7l.9 1.8 2 .3-1.45 1.4.35 2-1.8-.95-1.8.95.35-2L9.1 13.8l2-.3z"/></svg>'
)


def split_nom(nom: str) -> tuple[str, str]:
    """'EL OUARDI Hamza' -> ('EL OUARDI', 'Hamza')."""
    mots = nom.split()
    i = 0
    while i < len(mots) - 1 and mots[i].replace("-", "").replace("'", "").isupper():
        i += 1
    return " ".join(mots[:i]) or nom, " ".join(mots[i:])


def carte(r, place: int, couleur: str) -> str:
    nom, prenom = split_nom(r.Nom)
    club = f"<div class='pod-club'>{r.Club}</div>" if r.Club else ""
    cat = f"<i>/</i> {r.Cat}" if r.Cat else ""
    return (
        f"<div class='pod-card p{place}' style='--c:{couleur}'>"
        f"<div class='pod-medal'>{MEDAILLE.format(t=40 if place == 1 else 30)}</div>"
        f"<div class='pod-nom'>{prenom} {nom}</div>{club}"
        f"<div class='pod-meta'>{r.Sx} {cat}</div>"
        f"<div class='pod-temps'>{hms(r.Temps_s)}</div></div>"
    )


def podium(d: pd.DataFrame, sexe: str) -> str:
    s = d[(d["Sx"] == sexe) & d["Temps_s"].notna()].copy()
    s["Place"] = s["Temps_s"].rank(method="dense")  # ex æquo = même place
    s = s[s["Place"] <= 3].sort_values(["Place", "Nom"])
    couleurs = {1: OR, 2: ARGENT, 3: BRONZE}
    if s.empty:
        return "<div class='pod-wrap pod-vide'>Aucun arrivant dans cette catégorie</div>"
    cols = {}
    for place in (1, 2, 3):
        cartes = "".join(carte(r, place, couleurs[place]) for r in s[s["Place"] == place].itertuples())
        cols[place] = f"<div class='pod-col'>{cartes}</div>"
    return f"<div class='pod-wrap'>{cols[2]}{cols[1]}{cols[3]}</div>"


def densite(t: pd.Series, grille: np.ndarray, bw: float) -> np.ndarray:
    """Estimation de densité gaussienne, exprimée en coureurs par minute."""
    t = t.dropna().to_numpy()
    if len(t) == 0:
        return np.zeros_like(grille)
    z = (grille[:, None] - t[None, :]) / bw
    return np.exp(-0.5 * z**2).sum(axis=1) / (bw * np.sqrt(2 * np.pi)) * 60

def kpi(col, icone, label, n, temps, couleur):
    col.markdown(
        f"<div class='kpi-card' style='--c:{couleur}'>"
        f"<div class='kpi-ico'>{icone}</div>"
        f"<div><div class='kpi-lab'>{label}</div>"
        f"<div class='kpi-val'>{n:,}</div>".replace(",", " ")
        + f"<div class='kpi-moy'>Temps moyen<b>{hms(temps)}</b></div></div></div>",
        unsafe_allow_html=True,
    )


st.write("")
k3, k1, k2 = st.columns(3)
kpi(k1, "🏁", "Participants", len(d), arr["Temps_s"].mean(), FOND)
kpi(k2, "🏃", "Hommes", int((d["Sx"] == "Homme").sum()),
    arr.loc[arr["Sx"] == "Homme", "Temps_s"].mean(), ROUGE)
kpi(k3, "🏃‍♀️", "Femmes", int((d["Sx"] == "Femme").sum()),
    arr.loc[arr["Sx"] == "Femme", "Temps_s"].mean(), TEAL)

# ----------------------------------------------------------------------------
# Podiums
# ----------------------------------------------------------------------------
cats = [c for c in ORDRE_CAT if c in set(d["Cat"])]
cats += sorted(c for c in set(d["Cat"]) if c and c not in ORDRE_CAT)
choix = st.pills("", ["Scratch"] + cats, default="Scratch", key="pills_cat") or "Scratch"
dp = d if choix == "Scratch" else d[d["Cat"] == choix] # sélection
dp_arr = dp[dp["Temps_s"].notna()]  # arrivants de la sélection

p1, p2 = st.columns(2)
for col, sexe, libelle, ico, coul in (
    (p1, "Femme", "Podium Femmes", ICO_F, TEAL),
    (p2, "Homme", "Podium Hommes", ICO_H, ROUGE),
):
    col.markdown(
        titre(ico, libelle, f"Édition {annee}", "Toutes catégories" if choix == "Scratch" else f"Catégorie {choix}", coul),
        unsafe_allow_html=True,
    )
    col.markdown(podium(dp, sexe), unsafe_allow_html=True)

st.write("")

# ----------------------------------------------------------------------------
# Distribution des temps + répartition par sexe
# ----------------------------------------------------------------------------
st.markdown(
    titre("🔎", "Distribution des temps officiels", 
          f"Édition {annee} · temps pistolet" + ("" if choix == "Scratch" else f" · catégorie {choix}"),
          f"{len(dp_arr):,} arrivants".replace(",", " ")),
    unsafe_allow_html=True,
)

with st.container(key="distrib"):
    g_dist, g_donut_sex = st.columns([3.4, 1])

    lo = int(arr["Temps_s"].min() // 300 * 300)
    hi = int(arr["Temps_s"].max() // 300 * 300 + 600)
    grille = np.arange(lo, hi + 1, 30, dtype=float)

    with g_dist:
        fig = go.Figure()
        for sexe, couleur, nom in (("Homme", ROUGE, "Hommes"), ("Femme", TEAL, "Femmes")):
            y = densite(dp_arr.loc[arr["Sx"] == sexe, "Temps_s"], grille, bw=240)
            fig.add_trace(go.Scatter(
                x=grille, y=y, name=nom, mode="lines", fill="tozeroy",
                line=dict(color=couleur, width=2),
                fillcolor="rgba(194,66,91,.60)" if sexe == "Homme" else "rgba(58,181,176,.60)",
                hovertemplate=f"{nom}<br>%{{customdata}} · ≈%{{y:.0f}} coureurs<extra></extra>",
                customdata=[hms(v) for v in grille],
            ))
        ticks = list(range(lo, hi + 1, 300))
        fig.update_layout(
            height=380, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
            xaxis=dict(tickvals=ticks, ticktext=[hms(t) for t in ticks], tickangle=-35,
                       showgrid=False, color="white"),
            yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
            hovermode="x unified",
        )
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

    with g_donut_sex:
        rep = dp["Sx"].value_counts()
        ordre = [k for k in ("Homme", "Femme") if k in rep] + [k for k in rep.index if k not in SEXES]
        couleurs = {"Homme": ROUGE, "Femme": TEAL}
        fig = go.Figure(go.Pie(
            labels=ordre, values=[rep[k] for k in ordre], hole=0.72, sort=False,
            marker=dict(colors=[couleurs.get(k, "#8FA3A8") for k in ordre]),
            texttemplate="%{label}<br>%{percent:.1%}", textposition="outside",
            hovertemplate="%{label}: %{value} coureurs<extra></extra>", showlegend=False,
        ))
        fig.update_layout(height=380, margin=dict(l=60, r=60, t=20, b=20),
                          paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

st.caption(f"Édition {annee}" + ("" if choix == "Scratch" else f" · catégorie {choix}")
           + f" · {len(dp_arr)} arrivants sur {len(dp)} partants · "
           "temps pistolet · abandons exclus des moyennes et distributions.")