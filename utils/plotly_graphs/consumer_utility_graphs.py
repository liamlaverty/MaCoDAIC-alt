import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils.plotly_graphs.graph_config import (
    BAL_LINE,
    COMMERCIAL_COLOR,
    INDUSTRIAL_COLOR,
    RESIDENTIAL_COLOR,
    TARGET_LINE_COLOR,
)


def plot_welfare_history(
    subsistence_unmet_count_history: list[int] | None = None,
    subsistence_shortfall_units_history: list[float] | None = None,
    title: str = "Welfare Over Time",
) -> go.Figure:
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    if subsistence_unmet_count_history is not None:
        iterations = list(range(len(subsistence_unmet_count_history)))
        fig.add_trace(go.Scatter(
            x=iterations,
            y=subsistence_unmet_count_history,
            mode="lines",
            name="Residents Unmet",
            line=dict(color=RESIDENTIAL_COLOR, width=2.5),
            hovertemplate="Iteration %{x}<br>Residents Unmet: %{y}<extra></extra>",
        ), secondary_y=False)

    if subsistence_shortfall_units_history is not None:
        iterations = list(range(len(subsistence_shortfall_units_history)))
        fig.add_trace(go.Scatter(
            x=iterations,
            y=subsistence_shortfall_units_history,
            mode="lines",
            name="Shortfall (units)",
            line=dict(color=BAL_LINE, width=2.5),
            hovertemplate="Iteration %{x}<br>Shortfall: %{y:.1f} units<extra></extra>",
        ), secondary_y=True)

    fig.update_layout(
        title=title,
        template="plotly_white",
        xaxis=dict(title="Iteration"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        hovermode="x unified",
        margin=dict(t=80, r=70),
    )
    fig.update_yaxes(
        title_text="Residents Unmet",
        rangemode="tozero",
        secondary_y=False,
    )
    fig.update_yaxes(
        title_text="Shortfall (units)",
        rangemode="tozero",
        secondary_y=True,
    )

    return fig


def plot_throughput_history(
    units_sold_history: list[int] | None = None,
    population_history: list[int] | None = None,
    subsistence_quantity: float = 10,
    discretionary_optimum: float = 16,
    title: str = "Throughput Over Time",
) -> go.Figure:
    fig = make_subplots(specs=[[{"secondary_y": False}]])

    if units_sold_history is not None and population_history is not None:
        iterations = list(range(len(units_sold_history)))
        units_per_resident = [
            sold / pop if pop > 0 else 0
            for sold, pop in zip(units_sold_history, population_history)
        ]
        fig.add_trace(go.Scatter(
            x=iterations,
            y=units_per_resident,
            mode="lines",
            name="Units per Resident",
            line=dict(color=COMMERCIAL_COLOR, width=2.5),
            hovertemplate="Iteration %{x}<br>Units/Resident: %{y:.2f}<extra></extra>",
        ))

    fig.add_hline(
        y=subsistence_quantity,
        line=dict(color=TARGET_LINE_COLOR, width=1.5, dash="dot"),
        annotation_text="Subsistence floor",
        annotation_position="bottom right",
    )
    fig.add_hline(
        y=discretionary_optimum,
        line=dict(color=INDUSTRIAL_COLOR, width=1.5, dash="dot"),
        annotation_text="Discretionary optimum",
        annotation_position="bottom right",
    )

    fig.update_layout(
        title=title,
        template="plotly_white",
        xaxis=dict(title="Iteration"),
        yaxis=dict(title="Units per Resident per Day", rangemode="tozero"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        hovermode="x unified",
        margin=dict(t=80, r=70),
    )

    return fig


def plot_shortage_vs_demand_target(
    unfilled_discretionary_demand_history: list[int] | None = None,
    commercial_demand_target_history: list[float] | None = None,
    title: str = "Shortage vs Commercial Demand Target",
) -> go.Figure:
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    if unfilled_discretionary_demand_history is not None:
        iterations = list(range(len(unfilled_discretionary_demand_history)))
        fig.add_trace(go.Scatter(
            x=iterations,
            y=unfilled_discretionary_demand_history,
            mode="lines",
            name="Unfilled Discretionary Demand",
            line=dict(color=BAL_LINE, width=2.5),
            hovertemplate="Iteration %{x}<br>Unfilled: %{y}<extra></extra>",
        ), secondary_y=False)

    if commercial_demand_target_history is not None:
        iterations = list(range(len(commercial_demand_target_history)))
        fig.add_trace(go.Scatter(
            x=iterations,
            y=commercial_demand_target_history,
            mode="lines",
            name="Commercial Demand Target",
            line=dict(color=COMMERCIAL_COLOR, width=2.5, dash="dash"),
            hovertemplate="Iteration %{x}<br>Demand Target: %{y:.1f}<extra></extra>",
        ), secondary_y=True)

    fig.update_layout(
        title=title,
        template="plotly_white",
        xaxis=dict(title="Iteration"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        hovermode="x unified",
        margin=dict(t=80, r=70),
    )
    fig.update_yaxes(
        title_text="Unfilled Units",
        rangemode="tozero",
        secondary_y=False,
    )
    fig.update_yaxes(
        title_text="Demand Target",
        range=[-100, 100],
        secondary_y=True,
    )

    return fig
