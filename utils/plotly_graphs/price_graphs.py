import plotly.graph_objects as go
import pandas as pd

from utils.plotly_graphs.graph_config import AVG_LINE, BAND, EDGE


def plot_price_band(retailer_history: pd.DataFrame) -> go.Figure:
    """
    retailer_history: long-format DataFrame, one row per retailer per iteration.
    Returns a Plotly Figure showing min / mean / max retail price per iteration.
    """
    required = {"iteration", "price"}
    missing = required - set(retailer_history.columns)
    if missing:
        raise ValueError(f"retailer_history is missing columns: {missing}")
 
    df = retailer_history.copy()
    df["price"] = df["price"].astype(float)
 
    agg = (
        df.groupby("iteration")
        .agg(
            price_min=("price", "min"),
            price_avg=("price", "mean"),
            price_max=("price", "max"),
            n=("price", "count"),
        )
        .reset_index()
        .sort_values("iteration")
    )
 
    x = agg["iteration"].tolist()
    x_rev = x[::-1]
 
    fig = go.Figure()
 
    # ---- min–max band (drawn first so it sits behind the lines) ----
    fig.add_trace(go.Scatter(
        x=x + x_rev,
        y=agg["price_max"].tolist() + agg["price_min"].tolist()[::-1],
        fill="toself", fillcolor=BAND,
        line=dict(color="rgba(0,0,0,0)"),
        hoverinfo="skip", name="Price range (min–max)",
    ))
 
    # ---- thin max edge ----
    fig.add_trace(go.Scatter(
        x=x, y=agg["price_max"], mode="lines",
        line=dict(color=EDGE, width=1, dash="dot"),
        name="Max price",
        hovertemplate="<b>Max</b>: $%{y:.2f}<extra></extra>",
    ))
    # ---- thin min edge ----
    fig.add_trace(go.Scatter(
        x=x, y=agg["price_min"], mode="lines",
        line=dict(color=EDGE, width=1, dash="dot"),
        name="Min price",
        hovertemplate="<b>Min</b>: $%{y:.2f}<extra></extra>",
    ))
    # ---- average line (on top, bold) ----
    fig.add_trace(go.Scatter(
        x=x, y=agg["price_avg"], mode="lines+markers",
        line=dict(color=AVG_LINE, width=2.5),
        marker=dict(size=8),
        name="Average price",
        customdata=agg[["n"]],
        hovertemplate=(
            "<b>Avg</b>: $%{y:.2f}"
            "<br>(%{customdata[0]} retailers)<extra></extra>"
        ),
    ))
 
    fig.update_layout(
        title="Retail Price per Iteration (min / avg / max across retailers)",
        template="plotly_white",
        xaxis=dict(title="Iteration", dtick=1),
        yaxis=dict(title="Price ($)", rangemode="tozero"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        hovermode="x unified",
        margin=dict(t=80, r=40),
    )
    return fig
