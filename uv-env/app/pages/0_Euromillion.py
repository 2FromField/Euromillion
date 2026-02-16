import streamlit as st
import base64
from pathlib import Path
import utils
import gs_utils
import pandas as pd
from streamlit_extras.stylable_container import stylable_container
import altair as alt

##################################################################
#                        EUROMILLIOB                             #
##################################################################

st.set_page_config(page_title="Euromillion", layout="wide")

# Image d'entête
st.image(
    "https://cdn-media.fdj.fr/static/styles/507x760/public/contrib/images/2020-12/Logo1040x300_EMMM_Blanc.png",
    use_container_width=True,
)
st.divider()

# Style CSS
css_path = Path(__file__).resolve().parents[1] / "style.css"
st.markdown(
    f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True
)

# Configuration de l'environnement
cfg = utils.load_config()
env = cfg.get("env", "dev")  # "dev" ou "prod"
project_name = cfg["common"]["project_name"]  # euromillion
env_cfg = cfg[env]  # Accès à la section env (dev/prod)

# Chargement des données
if env == "dev":
    # table_path = env_cfg["data"]["TABLE"]
    # data = utils.load_df(table_path)
    data = gs_utils.load_table(env, "BDD")
else:  # "prod"
    data = gs_utils.load_table(env, "BDD")

##################################################################
#                         PRONOSTICS                             #
##################################################################

st.markdown(
    f"<h1 style='margin-bottom:30px color: gold;'>Mes Pronostics</h1>",
    unsafe_allow_html=True,
)

# Variables
N_NUM = 50
COLS_NUM = 4  # 4 boutons par ligne
N_STAR = 12
COLS_STAR = 4

# Initialisation des états des numéros/étoiles
for i in range(1, N_NUM + 1):
    st.session_state.setdefault(f"enabled_{i}", False)
for i in range(1, N_STAR + 1):
    st.session_state.setdefault(f"enabled_star_{i}", False)


def toggle_num(i):
    k = f"enabled_{i}"
    st.session_state[k] = not st.session_state.get(k, False)


def toggle_star(i):
    k = f"enabled_star_{i}"
    st.session_state[k] = not st.session_state.get(k, False)


st.markdown(
    """
<style>
/* scope uniquement sur la zone .st-key-grid_loto */
.st-key-grid_loto{
  padding: 0 16px !important;     /* <-- espace à gauche/droite */
}

/* centre chaque ligne de colonnes */
.st-key-grid_loto div[data-testid="stHorizontalBlock"]{
  width: fit-content !important;
  margin: 0 auto !important;
  flex-wrap: wrap !important;
  gap: 0.35rem !important;
}

/* 6 desktop */
.st-key-grid_loto div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]{
  flex: 0 0 calc(16.666% - 0.35rem) !important;
  min-width: 0 !important;
  padding: 0 !important;
}

/* 4 mobile */
@media (max-width: 640px){
  .st-key-grid_loto div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]{
    flex: 0 0 calc(25% - 0.35rem) !important;
  }
}

/* centre le bouton dans chaque case */
.st-key-grid_loto div[data-testid="stColumn"] > div{
  display: flex;
  justify-content: center;
}
</style>
""",
    unsafe_allow_html=True,
)

with st.container(key="grid_loto"):
    # --- Numéros ---
    for row_start in range(1, N_NUM + 1, COLS_NUM):
        cols = st.columns(COLS_NUM)
        for j in range(COLS_NUM):
            i = row_start + j
            if i > N_NUM:
                break
            enabled = st.session_state[f"enabled_{i}"]
            with cols[j]:
                # garde ton stylable_container uniquement pour le style du bouton
                with stylable_container(
                    f"btn_wrap_{i}", css_styles=utils.button_css(enabled)
                ):
                    st.button(str(i), key=f"toggle_{i}", on_click=toggle_num, args=(i,))

    # --- Etoiles ---
    for row_start in range(1, N_STAR + 1, COLS_STAR):
        cols = st.columns(COLS_STAR)
        for j in range(COLS_STAR):
            i = row_start + j
            if i > N_STAR:
                break
            enabled = st.session_state[f"enabled_star_{i}"]
            with cols[j]:
                with stylable_container(
                    f"btn_star_{i}", css_styles=utils.star_css(enabled)
                ):
                    st.button(
                        str(i), key=f"toggle_star_{i}", on_click=toggle_star, args=(i,)
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
    utils.render("Ma sélection :", nb_true, stars_true)


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
    last_row = matches.iloc[0]  # ligne la plus récente

    with stylable_container(
        "ant_tirage",
        css_styles="""
        {
          background-color: rgb(38, 38, 38);
          border-radius: 12px;
          padding: 12px;
        }
        """,
    ):
        t1, t2 = st.columns([1, 3], gap="small")

        with t1:
            date_txt = (
                last_row["Date"].strftime("%Y-%m-%d")
                if pd.notna(last_row["Date"])
                else ""
            )
            st.markdown(
                f"<h5 style='margin-top:20px;'>{date_txt}</h5>", unsafe_allow_html=True
            )

        with t2:
            utils.render(
                "Tirage similaire répertorié :",
                {int(last_row[c]) for c in num_cols if pd.notna(last_row[c])},
                {int(last_row[c]) for c in star_cols if pd.notna(last_row[c])},
            )

##################################################################
#                         STATISTIQUES                           #
##################################################################
st.divider()

st.markdown(
    f"<h1 style='margin-bottom:30px; margin-top: 30px; color: gold;'>STATISTIQUES</h1>",
    unsafe_allow_html=True,
)

# Format de date (sans heures)
data["Date"] = pd.to_datetime(data["Date"], errors="coerce").dt.normalize()

# Filtre
min_d = data["Date"].min()
max_d = data["Date"].max()

options = {
    "3 derniers jours": 3,
    "Dernière semaine": 7,
    "Dernier mois": 30,
    "3 derniers mois": 90,
    "6 derniers mois": 180,
    "Dernière année": 365,
    "2 dernières années": 730,
    "3 dernières années": 1095,
    "5 dernières années": 1825,
    "10 dernières années": 3650,
    "Tout l'historique": None,
}

labels = list(options.keys())

p1, p2 = st.columns([3, 1], gap="small")
with p1:
    period = st.selectbox(
        "Laps de temps observé",
        labels,
        index=labels.index("Tout l'historique"),
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


##################################################################
#                           LAYOUT                               #
##################################################################
st.divider()

st.markdown(
    f"<h1 style='margin-top: 30px; color: gold;'>Historique des résultats</h1>",
    unsafe_allow_html=True,
)

st.set_page_config(layout="wide")

min_d = data["Date"].min().date()
max_d = data["Date"].max().date()

with st.form("date_filter"):
    a1, a2, a3 = st.columns([4, 1, 1], gap="small")
    with a1:
        start_date, end_date = st.date_input(
            "Plage de dates",
            value=(
                max(max_d.replace(year=max_d.year - 1), min_d),
                max_d,
            ),  # par défaut: 1 an
            min_value=min_d,
            max_value=max_d,
        )
    with a2:
        nb_select = st.multiselect(
            "Numéros recherchés",
            options=list(range(1, 51)),
            default=[],
            placeholder="Choisir 1 ou plusieurs numéros",
        )
    with a3:
        star_select = st.multiselect(
            "Étoiles recherchées",
            options=list(range(1, 13)),
            default=[],
            placeholder="Choisir 1 ou plusieurs étoiles",
        )
    apply = st.form_submit_button("Appliquer")

# Appliqué le filtre de date
if apply:
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)

    num_cols = ["n1", "n2", "n3", "n4", "n5"]
    star_cols = ["e1", "e2"]

    data_filtered = data[data["Date"].between(start, end)].copy()

    # Garde-fous (sinon impossible)
    if len(nb_select) > 5:
        st.warning("Impossible : un tirage ne contient que 5 numéros.")
        df_view = data_filtered.iloc[0:0]
    elif len(star_select) > 2:
        st.warning("Impossible : un tirage ne contient que 2 étoiles.")
        data_filtered = data_filtered.iloc[0:0]
    else:
        mask = pd.Series(True, index=data_filtered.index)

        # Tous les numéros sélectionnés doivent être présents dans la ligne
        if nb_select:
            mask &= (
                data_filtered[num_cols].isin(nb_select).sum(axis=1).ge(len(nb_select))
            )

        # Toutes les étoiles sélectionnées doivent être présentes dans la ligne
        if star_select:
            mask &= (
                data_filtered[star_cols]
                .isin(star_select)
                .sum(axis=1)
                .ge(len(star_select))
            )

        data_filtered = data_filtered[mask]

    st.caption(f"Nombre de lignes trouvées: {len(data_filtered)}")
else:
    data_filtered = None
    st.caption("Choisis tes dates puis clique sur **Appliquer**.")

if data_filtered is not None:
    for row in data_filtered.itertuples(index=False):
        c = st.columns([2, 1, 1, 1, 1, 1, 1, 1, 2], gap="small")
        c[0].markdown(
            f"<span class='col-date'>{row.Date.strftime('%Y-%m-%d') if pd.notna(row.Date) else ''}</span>",
            unsafe_allow_html=True,
        )
        c[1].markdown(f"<span class='nb-badge'>{row.n1}</span>", unsafe_allow_html=True)
        c[2].markdown(f"<span class='nb-badge'>{row.n2}</span>", unsafe_allow_html=True)
        c[3].markdown(f"<span class='nb-badge'>{row.n3}</span>", unsafe_allow_html=True)
        c[4].markdown(f"<span class='nb-badge'>{row.n4}</span>", unsafe_allow_html=True)
        c[5].markdown(f"<span class='nb-badge'>{row.n5}</span>", unsafe_allow_html=True)
        c[6].markdown(
            f"<span class='star-badge'>{row.e1}</span>", unsafe_allow_html=True
        )
        c[7].markdown(
            f"<span class='star-badge'>{row.e2}</span>", unsafe_allow_html=True
        )
        c[8].markdown(
            f"<span class='col-date'>{row.Jackpot}</span>",
            unsafe_allow_html=True,
        )
