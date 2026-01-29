import streamlit as st
import base64
from pathlib import Path
import utils
from streamlit_extras.stylable_container import stylable_container

##################################################################
#                           LAYOUT                               #
##################################################################

st.set_page_config(page_title="Accueil", layout="wide")

st.caption("Mes pronostics")

# Variables
N_NUM = 50
COLS_NUM = 10  # 10 boutons par ligne
N_STAR = 10
COLS_STAR = 10

# Initialisation des états des numéros/étoiles
for i in range(1, N_NUM + 1):
    st.session_state.setdefault(f"enabled_{i}", False)
for i in range(1, N_STAR + 1):
    st.session_state.setdefault(f"enabled_star_{i}", False)

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
                if st.button(str(i), key=f"toggle_{i}"):
                    st.session_state[state_key] = not enabled
                    st.rerun()

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
                if st.button(str(i), key=f"toggle_star_{i}"):
                    st.session_state[state_key] = not enabled
                    st.rerun()

# Affichage des états
st.write(
    {f"star_{i}": st.session_state[f"enabled_star_{i}"] for i in range(1, N_STAR + 1)}
)
st.write({f"bouton_{i}": st.session_state[f"enabled_{i}"] for i in range(1, N_NUM + 1)})
