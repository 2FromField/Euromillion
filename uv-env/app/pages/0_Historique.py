import streamlit as st
import base64
from pathlib import Path
import utils
import pandas as pd
from streamlit_extras.stylable_container import stylable_container

# Style CSS
css_path = Path(__file__).resolve().parents[1] / "style.css"
st.markdown(
    f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True
)

# Configuration de l'environnement
cfg = utils.load_config("config.yaml")
env = cfg.get("env", "dev")  # "dev" ou "prod"
project_name = cfg["common"]["project_name"]  # euromillion
env_cfg = cfg[env]  # Accès à la section env (dev/prod)

# Chargement des données
table_path = env_cfg["data"]["TABLE"]
data = utils.load_df(table_path)

##################################################################
#                           LAYOUT                               #
##################################################################

st.markdown(
    f"<h1>Historique des résultats</h1>",
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
