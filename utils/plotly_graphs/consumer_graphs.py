import plotly.graph_objects as go
import pandas as pd

from utils.plotly_graphs.graph_config import BAL_BAND, BAL_LINE, UTIL_BAND, UTIL_LINE


def plot_consumer_utility_vs_balance(history: pd.DataFrame) -> go.Figure:
    """
    history: long-format DataFrame with columns
             ['iteration', 'consumer', 'utility', 'balance']
             (one row per consumer per iteration)
    Returns a Plotly Figure (call .show() or .write_html(...)).
    """
    required = {"iteration", "utility", "balance"}
    missing = required - set(history.columns)
    if missing:
        raise ValueError(f"history is missing columns: {missing}")
 
    # Aggregate across consumers, per iteration
    agg = (
        history.groupby("iteration")
        .agg(
            util_mean=("utility", "mean"),
            util_min=("utility", "min"),
            util_max=("utility", "max"),
            bal_mean=("balance", "mean"),
            bal_min=("balance", "min"),
            bal_max=("balance", "max"),
        )
        .reset_index()
        .sort_values("iteration")
    )
 
    x = agg["iteration"].tolist()
    x_rev = x[::-1]  # for the closed band polygon
 
    fig = go.Figure()
 
    # ---------- UTILITY band (left axis) ----------
    fig.add_trace(go.Scatter(
        x=x + x_rev,
        y=agg["util_max"].tolist() + agg["util_min"].tolist()[::-1],
        fill="toself", fillcolor=UTIL_BAND,
        line=dict(color="rgba(0,0,0,0)"),
        hoverinfo="skip", showlegend=True,
        name="Utility min-max", yaxis="y1",
    ))
    # ---------- UTILITY mean line (left axis) ----------
    fig.add_trace(go.Scatter(
        x=x, y=agg["util_mean"],
        mode="lines+markers",
        line=dict(color=UTIL_LINE, width=2.5),
        marker=dict(size=8),
        name="Utility (mean)", yaxis="y1",
        hovertemplate="Iter %{x}<br>Utility: %{y:.2f}<extra></extra>",
    ))
 
    # ---------- BALANCE band (right axis) ----------
    fig.add_trace(go.Scatter(
        x=x + x_rev,
        y=agg["bal_max"].tolist() + agg["bal_min"].tolist()[::-1],
        fill="toself", fillcolor=BAL_BAND,
        line=dict(color="rgba(0,0,0,0)"),
        hoverinfo="skip", showlegend=True,
        name="Balance min-max", yaxis="y2",
    ))
    # ---------- BALANCE mean line (right axis) ----------
    fig.add_trace(go.Scatter(
        x=x, y=agg["bal_mean"],
        mode="lines+markers",
        line=dict(color=BAL_LINE, width=2.5, dash="dot"),
        marker=dict(size=8, symbol="diamond"),
        name="Balance (mean)", yaxis="y2",
        hovertemplate="Iter %{x}<br>Balance: $%{y:.2f}<extra></extra>",
    ))
 
    fig.update_layout(
        title="Consumer Utility vs. Balance over Iterations",
        template="plotly_white",
        xaxis=dict(title="Iteration", dtick=1),
        yaxis=dict(
            title=dict(text="Utility (utils)", font=dict(color=UTIL_LINE)),
            tickfont=dict(color=UTIL_LINE),
            rangemode="tozero",
        ),
        yaxis2=dict(
            title=dict(text="Balance ($)", font=dict(color=BAL_LINE)),
            tickfont=dict(color=BAL_LINE),
            overlaying="y", side="right",
            rangemode="tozero",
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        hovermode="x unified",
        margin=dict(t=80, r=70),
    )
    return fig