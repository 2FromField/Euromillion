import streamlit as st
import base64
from pathlib import Path
import utils
import pandas as pd
from streamlit_extras.stylable_container import stylable_container

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

min_d = data["Date"].min().date()
max_d = data["Date"].max().date()

with st.form("date_filter"):
    start_date, end_date = st.date_input(
        "Plage de dates",
        value=(
            max(max_d.replace(year=max_d.year - 1), min_d),
            max_d,
        ),  # par défaut: 1 an
        min_value=min_d,
        max_value=max_d,
    )
    apply = st.form_submit_button("Appliquer")

if apply:
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    data_filtered = data[data["Date"].between(start, end)]
    st.dataframe(data_filtered, use_container_width=True)
else:
    data_filtered = None
    st.caption("Choisis tes dates puis clique sur **Appliquer**.")

h = st.columns(9, gap="small")
for col, title in zip(h, ["Date", "n1", "n2", "n3", "n4", "n5", "e1", "e2", "Jackpot"]):
    col.caption(title)

if data_filtered != None:
    for row in data_filtered.itertuples(index=False):
        c = st.columns(9, gap="small")
        c[0].write(row.Date)
        c[1].write(row.n1)
        c[2].write(row.n2)
        c[3].write(row.n3)
        c[4].write(row.n4)
        c[5].write(row.n5)
        c[6].write(row.e1)
        c[7].write(row.e2)
        c[8].write(row.Jackpot)
