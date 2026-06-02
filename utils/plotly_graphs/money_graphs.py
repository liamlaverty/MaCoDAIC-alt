import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from utils.plotly_graphs.graph_utils import _wrap_text

def plot_retailer_profit(retailer_history: pd.DataFrame) -> go.Figure:
    """
    retailer_history: long-format DataFrame, one row per retailer per iteration.
    Returns a Plotly Figure.
    """
    required = {"iteration", "retailer_name", "profit"}
    missing = required - set(retailer_history.columns)
    if missing:
        raise ValueError(f"retailer_history is missing columns: {missing}")
 
    df = retailer_history.copy()
    # profit may be Decimal -> cast to float for plotting
    df["profit"] = df["profit"].astype(float)
    df = df.sort_values(["retailer_name", "iteration"])
 
    names = sorted(df["retailer_name"].unique())
    palette = px.colors.qualitative.Set2
 
    fig = go.Figure()
    for i, name in enumerate(names):
        sub = df[df["retailer_name"] == name].copy()
        sub["reasoning"] = sub["reasoning"].apply(_wrap_text)
        sub["notes_to_self"] = sub["notes_to_self"].apply(_wrap_text)
        fig.add_trace(go.Scatter(
            x=sub["iteration"], y=sub["profit"],
            mode="lines+markers",
            name=name,
            line=dict(color=palette[i % len(palette)], width=2.5),
            marker=dict(size=8),
            customdata=sub[["stock",
                            "price",
                            "retailer_model",
                            "retailer_temperature",
                            "reasoning",
                            "notes_to_self"]],
            hovertemplate=(
                f"<b>{name}</b><br>"
                "<i>Profit</i>: $%{y:.2f}<br>"
                "<i>Stock</i>: %{customdata[0]:.0f}<br>"
                "<i>Price</i>: $%{customdata[1]:.2f}<br>"
                "<i>Model</i>: %{customdata[2]} (%{customdata[3]})<br>"
                # "<i>Reasoning</i>: %{customdata[3]}<br>"
                # "<i>Notes</i>: %{customdata[4]}<br>"
                "<extra></extra>"
            ),
        ))
 
    fig.update_layout(
        title="Retailer Profit over Iterations",
        template="plotly_white",
        height=600,
        xaxis=dict(title="Iteration", dtick=1),
        yaxis=dict(title="Profit ($)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        hovermode="x unified",
        margin=dict(t=80, r=40),
    )
    return fig


def plot_retailer_money(retailer_history: pd.DataFrame) -> go.Figure:
    """
    retailer_history: long-format DataFrame, one row per retailer per iteration.
    Returns a Plotly Figure.
    """
    required = {"iteration", "retailer_name", "balance"}
    missing = required - set(retailer_history.columns)
    if missing:
        raise ValueError(f"retailer_history is missing columns: {missing}")
 
    df = retailer_history.copy()
    # balance may be Decimal -> cast to float for plotting
    df["balance"] = df["balance"].astype(float)
    df = df.sort_values(["retailer_name", "iteration"])
 
    names = sorted(df["retailer_name"].unique())
    palette = px.colors.qualitative.Set2
 
    fig = go.Figure()
    for i, name in enumerate(names):
        sub = df[df["retailer_name"] == name].copy()
        sub["reasoning"] = sub["reasoning"].apply(_wrap_text)
        sub["notes_to_self"] = sub["notes_to_self"].apply(_wrap_text)
        fig.add_trace(go.Scatter(
            x=sub["iteration"], y=sub["balance"],
            mode="lines+markers",
            name=name,
            line=dict(color=palette[i % len(palette)], width=2.5),
            marker=dict(size=8),
            customdata=sub[["stock",
                            "price",
                            "retailer_model",
                            "retailer_temperature",
                            "reasoning",
                            "notes_to_self"]],
            hovertemplate=(
                f"<b>{name}</b><br>"
                "<i>Balance</i>: $%{y:.2f}<br>"
                "<i>Stock</i>: %{customdata[0]:.0f}<br>"
                "<i>Price</i>: $%{customdata[1]:.2f}<br>"
                "<i>Model</i>: %{customdata[2]} (%{customdata[3]})<br>"
                # "<i>Reasoning</i>: %{customdata[3]}<br>"
                # "<i>Notes</i>: %{customdata[4]}<br>"
                "<extra></extra>"
            ),
        ))
 
    fig.update_layout(
        title="Retailer Money over Iterations",
        template="plotly_white",
        height=600,
        xaxis=dict(title="Iteration", dtick=1),
        yaxis=dict(title="Balance ($)", rangemode="tozero"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        hovermode="x unified",
        margin=dict(t=80, r=40),
    )
    return fig
 