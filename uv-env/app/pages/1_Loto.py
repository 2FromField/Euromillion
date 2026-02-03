import streamlit as st
import base64
from pathlib import Path
import utils
from streamlit_extras.stylable_container import stylable_container
import altair as alt
import pandas as pd

st.set_page_config(page_title="Loto", layout="wide")

st.markdown(
    f"<h1 style='margin-bottom:30px;'>Loto</h1>",
    unsafe_allow_html=True,
)
