def button_css(enabled: bool) -> str:
    if enabled:
        return """
        button {
            width: 40px;
            height: 40px;
            background-color: red !important;
            color: white !important;
            border: 1px solid red !important;
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
        color: red !important;
        border: 1px solid red !important;
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
            background-color: grey !important;
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
