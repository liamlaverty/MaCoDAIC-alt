import pandas as pd
import textwrap


def _wrap_text(text, width=80):
    if pd.isna(text) or not str(text).strip():
        return ""
    return "<br>".join(textwrap.wrap(str(text), width=width))