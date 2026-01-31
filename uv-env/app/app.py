import streamlit as st
import utils

###############################################################
#                         LAYOUT                              #
###############################################################
st.set_page_config(page_title="BeMillionnaire", layout="wide")

st.title("Mes Pronostics")
st.switch_page("pages/0_Historique.py")  # Redirection vers la page d'accueil
