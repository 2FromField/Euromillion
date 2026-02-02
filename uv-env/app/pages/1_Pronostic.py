import streamlit as st
import base64
from pathlib import Path
import utils
from streamlit_extras.stylable_container import stylable_container
import altair as alt
import pandas as pd

##################################################################
#                           DONNEES                              #
##################################################################

# Configuration de l'environnement
cfg = utils.get_cfg()
env = cfg.get("env", "dev")  # "dev" ou "prod"
project_name = cfg["common"]["project_name"]  # euromillion
env_cfg = cfg[env]  # Accès à la section env (dev/prod)

# Chargement des données
table_path = env_cfg["data"]["TABLE"]
data = utils.get_data(table_path)


##################################################################
#                         PRONOSTICS                             #
##################################################################

# Style CSS
css_path = Path(__file__).resolve().parents[1] / "style.css"
st.markdown(
    f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True
)

st.set_page_config(page_title="Accueil", layout="wide")

st.markdown(
    f"<h1 style='margin-bottom:30px;'>Mes Pronostics</h1>",
    unsafe_allow_html=True,
)

# Variables
N_NUM = 50
COLS_NUM = 6  # 10 boutons par ligne
N_STAR = 12
COLS_STAR = 6

# Initialisation des états des numéros/étoiles
for i in range(1, N_NUM + 1):
    st.session_state.setdefault(f"enabled_{i}", False)
for i in range(1, N_STAR + 1):
    st.session_state.setdefault(f"enabled_star_{i}", False)

c1, c2, c3 = st.columns([1, 5, 1], gap="small")


def toggle_num(i):
    k = f"enabled_{i}"
    st.session_state[k] = not st.session_state.get(k, False)


def toggle_star(i):
    k = f"enabled_star_{i}"
    st.session_state[k] = not st.session_state.get(k, False)


with c2:

    # Numéros
    for row_start in range(1, N_NUM + 1, COLS_NUM):  # 1, 11, 21, 31, 41
        cols = st.columns(COLS_NUM)
        for j in range(COLS_NUM):
            i = row_start + j
            if i > N_NUM:
                break

            state_key = f"enabled_{i}"
            enabled = st.session_state[state_key]

            with cols[j]:
                with stylable_container(
                    f"btn_wrap_{i}", css_styles=utils.button_css(enabled)
                ):
                    st.button(
                        str(i),
                        key=f"toggle_{i}",
                        on_click=toggle_num,
                        args=(i,),
                    )

    # Etoiles
    for row_start in range(1, N_STAR + 1, COLS_STAR):  # 1, 11, 21, 31, 41
        cols = st.columns(COLS_STAR)
        for j in range(COLS_STAR):
            i = row_start + j
            if i > N_STAR:
                break

            state_key = f"enabled_star_{i}"
            enabled = st.session_state[state_key]

            with cols[j]:
                with stylable_container(
                    f"btn_star_{i}", css_styles=utils.star_css(enabled)
                ):
                    st.button(
                        str(i),
                        key=f"toggle_star_{i}",
                        on_click=toggle_star,
                        args=(i,),
                    )

# Récupération des états "true" (numéros et étoiles sélectionnées)
nb_true = {
    i for i in range(1, N_NUM + 1) if st.session_state.get(f"enabled_{i}", False)
}
stars_true = {
    i for i in range(1, N_STAR + 1) if st.session_state.get(f"enabled_star_{i}", False)
}

# Affichage de la sélection
b1, b2, b3 = st.columns([1, 4, 1], gap="small")
with b2:
    # Exemple d'affichage
    utils.render(nb_true, stars_true)


def transform_to_list(numbers):
    if numbers is None:
        numbers = []
    if isinstance(numbers, (set, tuple)):
        numbers = list(numbers)
    if isinstance(numbers, int):
        numbers = [numbers]
    return numbers


# Liste des chiffres/nombres sélectionnés
list_nb = transform_to_list(nb_true)
list_star = transform_to_list(stars_true)

# Réciprocité avec l'historique des résultats
df_src = data.copy()

# Entetes de colonnes
num_cols = ["n1", "n2", "n3", "n4", "n5"]
star_cols = ["e1", "e2"]

# Sécuriser les types
df_src = df_src.copy()
df_src["Date"] = pd.to_datetime(df_src["Date"], errors="coerce")
df_src[num_cols + star_cols] = df_src[num_cols + star_cols].apply(
    pd.to_numeric, errors="coerce"
)

# Garde-fous (sinon impossible)
if len(list_nb) > 5:
    st.warning("Impossible : un tirage ne contient que 5 numéros.")
elif len(list_star) > 2:
    st.warning("Impossible : un tirage ne contient que 2 étoiles.")
else:
    mask = pd.Series(True, index=df_src.index)

    # Tous les numéros sélectionnés doivent être présents sur la même ligne
    if list_nb:
        mask &= df_src[num_cols].isin(list_nb).sum(axis=1).ge(len(list_nb))

    # Toutes les étoiles sélectionnées doivent être présentes sur la même ligne
    if list_star:
        mask &= df_src[star_cols].isin(list_star).sum(axis=1).ge(len(list_star))

    matches = df_src.loc[mask].sort_values("Date", ascending=False)

    if matches.empty:
        st.info("Aucun tirage historisé ne contient cette combinaison.")
    else:
        t1, t2, t3 = st.columns([1, 1, 3], gap="small")
        last_row = matches.iloc[0]  # ligne la plus récente
        with t1:
            st.markdown(
                f"<h5 style='margin-top:20px;'>Tirage similaire :</h5>",
                unsafe_allow_html=True,
            )
        with t2:
            st.markdown(
                f"<h5 style='margin-top:20px;'>{last_row['Date'].strftime('%Y-%m-%d')}</h5>",
                unsafe_allow_html=True,
            )
        with t3:
            utils.render(
                {int(last_row[c]) for c in num_cols},
                {int(last_row[c]) for c in star_cols},
            )

##################################################################
#                         STATISTIQUES                           #
##################################################################

st.markdown(
    f"<h1 style='margin-bottom:30px;'>STATISTIQUES</h1>",
    unsafe_allow_html=True,
)

# Format de date (sans heures)
data["Date"] = pd.to_datetime(data["Date"], errors="coerce").dt.normalize()

# Filtre
min_d = data["Date"].min()
max_d = data["Date"].max()

options = {
    "Last 3 days": 3,
    "Last week": 7,
    "Last month": 30,
    "Last 3 months": 90,
    "Last 6 months": 180,
    "Last year": 365,
    "Last 2 years": 730,
    "Last 3 years": 1095,
    "Last 5 years": 1825,
    "Last 10 years": 3650,
    "All time": None,
}

labels = list(options.keys())

p1, p2 = st.columns([3, 1], gap="small")
with p1:
    period = st.selectbox(
        "Laps de temps observé",
        labels,
        index=labels.index("All time"),
        key="period_select",
    )
    # Variable de temps
    end = max_d
    days = options[period]

    start = min_d if days is None else max(end - pd.Timedelta(days=days), min_d)
with p2:
    st.markdown(
        f"<h5 style='margin-top:28px;'>{start.date()} → {end.date()}</h5>",
        unsafe_allow_html=True,
    )

df_filtered = data[data["Date"].between(start, end)].copy()

# ✅ Graphs doivent utiliser df_filtered
df_plot = df_filtered

num_cols = ["n1", "n2", "n3", "n4", "n5"]
star_cols = ["e1", "e2"]

# S'assurer que c'est numérique
df_plot[num_cols + star_cols] = df_plot[num_cols + star_cols].apply(
    pd.to_numeric, errors="coerce"
)

# Long format + fréquences
nums_long = df_plot[num_cols].melt(value_name="val").dropna()
stars_long = df_plot[star_cols].melt(value_name="val").dropna()

num_freq = (
    nums_long["val"]
    .value_counts()
    .sort_index()
    .rename_axis("val")
    .reset_index(name="freq")
)
star_freq = (
    stars_long["val"]
    .value_counts()
    .sort_index()
    .rename_axis("val")
    .reset_index(name="freq")
)

# Thème + interactivité
base = alt.Chart().properties(height=320).interactive()

highlight_nums = alt.FieldOneOfPredicate(field="val", oneOf=list_nb)

chart_nums = (
    alt.Chart(num_freq, title="Fréquence des numéros")
    .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
    .encode(
        x=alt.X("val:O", title="Numéro"),
        y=alt.Y("freq:Q", title="Fréquence"),
        color=alt.condition(
            highlight_nums,
            alt.value("blue"),  # couleur des sélectionnés
            alt.value("#9ca3af"),  # couleur des autres
        ),
        tooltip=[
            alt.Tooltip("val:O", title="Numéro"),
            alt.Tooltip("freq:Q", title="Fréquence"),
        ],
    )
)

highlight_stars = alt.FieldOneOfPredicate(field="val", oneOf=list_star)

chart_stars = (
    alt.Chart(star_freq, title="Fréquence des étoiles")
    .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
    .encode(
        x=alt.X("val:O", title="Étoile"),
        y=alt.Y("freq:Q", title="Fréquence"),
        color=alt.condition(
            highlight_stars,
            alt.value("yellow"),  # sélectionnées
            alt.value("#9ca3af"),  # autres
        ),
        tooltip=[
            alt.Tooltip("val:O", title="Étoile"),
            alt.Tooltip("freq:Q", title="Fréquence"),
        ],
    )
)

# Affichage côte à côte dans Streamlit
c1, c2 = st.columns(2, gap="large")
with c1:
    st.altair_chart(chart_nums, use_container_width=True)
with c2:
    st.altair_chart(chart_stars, use_container_width=True)
