import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

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
    palette = px.colors.qualitative.Set2  # distinct, colorblind-friendlier
 
    fig = go.Figure()
    for i, name in enumerate(names):
        sub = df[df["retailer_name"] == name]
        fig.add_trace(go.Scatter(
            x=sub["iteration"], y=sub["balance"],
            mode="lines+markers",
            name=name,
            line=dict(color=palette[i % len(palette)], width=2.5),
            marker=dict(size=8),
            customdata=sub[["stock", "price"]].astype(float),
            hovertemplate=(
                f"<b>{name}</b><br>"
                "Balance: $%{y:.2f}<br>"
                "Stock: %{customdata[0]:.0f}<br>"
                "Price: $%{customdata[1]:.2f}"
                "<extra></extra>"
            ),
        ))
 
    fig.update_layout(
        title="Retailer Money over Iterations",
        template="plotly_white",
        xaxis=dict(title="Iteration", dtick=1),
        yaxis=dict(title="Balance ($)", rangemode="tozero"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        hovermode="x unified",
        margin=dict(t=80, r=40),
    )
    return fig
 