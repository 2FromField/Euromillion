import streamlit as st
import yaml
from pathlib import Path
import pandas as pd


def load_config(path: str | Path = "config.yaml") -> dict:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@st.cache_data
def get_cfg():
    return load_config("config.yaml")


def load_df(file_path):
    df = pd.read_csv(file_path, sep=";")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.normalize()
    return df


@st.cache_data
def get_data(path):
    return load_df(path)


def button_css(enabled: bool) -> str:
    if enabled:
        return """
        button {
            width: 40px;
            height: 40px;
            background-color: blue !important;
            color: white !important;
            border: 1px solid blue !important;
            border-radius: 10px !important;
            padding: 0.4rem 0.6rem !important;
            margin-bottom: 20px;
        }
        """
    return """
    button {
        width: 40px;
        height: 40px;
        background-color: transparent !important;
        color: grey !important;
        border: 1px solid grey !important;
        border-radius: 10px !important;
        padding: 0.4rem 0.6rem !important;
        margin-bottom: 20px;
    }
    """


def star_css(enabled: bool) -> str:
    if enabled:
        return """
        button {
            width: 40px;
            height: 40px;
            background-color: yellow !important;
            color: black !important;
            border: 1px solid yellow !important;
            padding:0;
            margin-bottom: 20px;
            clip-path: polygon(
                50% 2%,
                61% 35%,
                98% 35%,
                68% 57%,
                79% 91%,
                50% 70%,
                21% 91%,
                32% 57%,
                2% 35%,
                39% 35%
            );
            appearance: none;
            -webkit-appearance: none;
        }
        """
    return """
        button {
            width: 40px;
            height: 40px;
            background-color: #808080 !important;
            color: white !important;
            border: 1px solid yellow !important;
            padding:0;
            margin-bottom: 20px;
            clip-path: polygon(
                50% 2%,
                61% 35%,
                98% 35%,
                68% 57%,
                79% 91%,
                50% 70%,
                21% 91%,
                32% 57%,
                2% 35%,
                39% 35%
            );
        }
    """


def render(text, numbers, stars, size=40):
    st.markdown(
        f"""
        <style>
          .wrap {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            align-items: center;
            margin-bottom: 50px;
          }}

          .num-circle {{
            width: {size}px;
            height: {size}px;
            border-radius: 999px;
            background: blue;
            color: white;
            display: inline-flex;
            justify-content: center;
            align-items: center;
            font-weight: 700;
            line-height: 1;
          }}

          .star-circle {{
            width: {size}px;
            height: {size}px;

            background: yellow;
            color: black;
            display: inline-flex;
            justify-content: center;
            align-items: center;
            font-weight: 700;
            line-height: 1;

            /* forme étoile */
            clip-path: polygon(
              50% 2%,
              61% 35%,
              98% 35%,
              68% 57%,
              79% 91%,
              50% 70%,
              21% 91%,
              32% 57%,
              2% 35%,
              39% 35%
            );
          }}

          .label {{
            font-size: 1.05em;
            margin-right: 6px;
          }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Normaliser les entrées (set/list/tuple/int -> list)
    if numbers is None:
        numbers = []
    if isinstance(numbers, (set, tuple)):
        numbers = list(numbers)
    if isinstance(numbers, int):
        numbers = [numbers]

    if stars is None:
        stars = []
    if isinstance(stars, (set, tuple)):
        stars = list(stars)
    if isinstance(stars, int):
        stars = [stars]

    # Optionnel : tri pour un affichage stable
    numbers = sorted(numbers)
    stars = sorted(stars)

    html = (
        '<div class="wrap">'
        f'<h5 class="label" style="margin-top: 5px;">{text}</h5>'
        + "".join(f'<span class="num-circle">{n}</span>' for n in numbers)
        + "".join(f'<span class="star-circle">{s}</span>' for s in stars)
        + "</div>"
    )

    st.markdown(html, unsafe_allow_html=True)
