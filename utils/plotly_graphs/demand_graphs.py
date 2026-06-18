import plotly.graph_objects as go

from utils.plotly_graphs.graph_config import (
    COMMERCIAL_COLOR,
    INDUSTRIAL_COLOR,
    RESIDENTIAL_COLOR,
    TARGET_LINE_COLOR,
)


def plot_demand_bar(
    residential_demand: float,
    residential_target: float,
    commercial_demand: float,
    commercial_target: float,
    industrial_demand: float,
    industrial_target: float,
    iteration: int | None = None,
) -> go.Figure:
    categories = ["Residential", "Commercial", "Industrial"]
    values = [residential_demand, commercial_demand, industrial_demand]
    targets = [residential_target, commercial_target, industrial_target]
    colors = [RESIDENTIAL_COLOR, COMMERCIAL_COLOR, INDUSTRIAL_COLOR]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker_color=colors,
        name="Current Demand",
    ))

    # Add target markers as short horizontal lines
    for i, (cat, target) in enumerate(zip(categories, targets)):
        fig.add_shape(
            type="line",
            x0=i - 0.4, x1=i + 0.4,
            y0=target, y1=target,
            line=dict(color=TARGET_LINE_COLOR, width=3, dash="dash"),
        )

    title = "RCI Demand — Current Iteration"
    if iteration is not None:
        title += f" ({iteration})"

    fig.update_layout(
        title=title,
        yaxis=dict(range=[0, 100], title="Demand"),
        xaxis=dict(title="Sector"),
        showlegend=False,
    )

    return fig


def plot_jobs_history(
    jobs_per_resident_history: list[float] | None = None,
    unemployment_rate_history: list[float] | None = None,
    vacancy_rate_history: list[float] | None = None,
    title: str = "Jobs and Employment Over Time",
) -> go.Figure:
    from plotly.subplots import make_subplots

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    if jobs_per_resident_history is not None:
        iterations = list(range(len(jobs_per_resident_history)))
        fig.add_trace(go.Scatter(
            x=iterations,
            y=jobs_per_resident_history,
            mode="lines",
            name="Jobs per Resident",
            line=dict(color=COMMERCIAL_COLOR, width=2.5),
            hovertemplate="Iteration %{x}<br>Jobs per Resident: %{y:.2f}<extra></extra>",
        ), secondary_y=False)

        fig.add_hline(
            y=1,
            line=dict(color=TARGET_LINE_COLOR, width=1.5, dash="dot"),
            annotation_text="1 job per resident",
            annotation_position="bottom right",
            secondary_y=False,
        )

    if unemployment_rate_history is not None:
        iterations = list(range(len(unemployment_rate_history)))
        fig.add_trace(go.Scatter(
            x=iterations,
            y=unemployment_rate_history,
            mode="lines",
            name="Unemployment Rate",
            line=dict(color="rgb(214, 90, 48)", width=2.5),
            hovertemplate="Iteration %{x}<br>Unemployment: %{y:.2%}<extra></extra>",
        ), secondary_y=True)

    if vacancy_rate_history is not None:
        iterations = list(range(len(vacancy_rate_history)))
        fig.add_trace(go.Scatter(
            x=iterations,
            y=vacancy_rate_history,
            mode="lines",
            name="Vacancy Rate",
            line=dict(color=RESIDENTIAL_COLOR, width=2.5, dash="dash"),
            hovertemplate="Iteration %{x}<br>Vacancy: %{y:.2%}<extra></extra>",
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
        title_text="Jobs per Resident",
        rangemode="tozero",
        secondary_y=False,
    )
    fig.update_yaxes(
        title_text="Rate",
        tickformat=".0%",
        range=[0, 1],
        secondary_y=True,
    )

    return fig


def plot_demand_history(
    residential_demand_history: list[float] | None = None,
    commercial_demand_history: list[float] | None = None,
    industrial_demand_history: list[float] | None = None,
    residential_target_history: list[float] | None = None,
    commercial_target_history: list[float] | None = None,
    industrial_target_history: list[float] | None = None,
    population_history: list[float] | None = None,
    population_label: str = "Population",
    title: str = "RCI Demand Over Time",
) -> go.Figure:
    # Determine iteration count from whichever list is provided
    length = 0
    for hist in (residential_demand_history, commercial_demand_history,
                 industrial_demand_history, residential_target_history,
                 commercial_target_history, industrial_target_history,
                 population_history):
        if hist is not None:
            length = max(length, len(hist))
    iterations = list(range(length))

    fig = go.Figure()

    # Solid lines for actual demand
    if residential_demand_history is not None:
        fig.add_trace(go.Scatter(
            x=iterations, y=residential_demand_history,
            mode="lines", name="Residential",
            line=dict(color=RESIDENTIAL_COLOR),
        ))
    if commercial_demand_history is not None:
        fig.add_trace(go.Scatter(
            x=iterations, y=commercial_demand_history,
            mode="lines", name="Commercial",
            line=dict(color=COMMERCIAL_COLOR),
        ))
    if industrial_demand_history is not None:
        fig.add_trace(go.Scatter(
            x=iterations, y=industrial_demand_history,
            mode="lines", name="Industrial",
            line=dict(color=INDUSTRIAL_COLOR),
        ))

    # Dashed lines for targets
    if residential_target_history is not None:
        fig.add_trace(go.Scatter(
            x=iterations, y=residential_target_history,
            mode="lines", name="Residential Target",
            line=dict(color=RESIDENTIAL_COLOR, dash="dash"),
        ))
    if commercial_target_history is not None:
        fig.add_trace(go.Scatter(
            x=iterations, y=commercial_target_history,
            mode="lines", name="Commercial Target",
            line=dict(color=COMMERCIAL_COLOR, dash="dash"),
        ))
    if industrial_target_history is not None:
        fig.add_trace(go.Scatter(
            x=iterations, y=industrial_target_history,
            mode="lines", name="Industrial Target",
            line=dict(color=INDUSTRIAL_COLOR, dash="dash"),
        ))

    # Black dotted line for population overlay
    if population_history is not None:
        fig.add_trace(go.Scatter(
            x=iterations, y=population_history,
            mode="lines", name=population_label,
            line=dict(color="black", dash="dot"),
        ))

    fig.update_layout(
        title=title,
        xaxis=dict(title="Iteration"),
        yaxis=dict(range=[0, max(max(residential_demand_history or [0]), max(commercial_demand_history or [0]), max(industrial_demand_history or [0]), max(residential_target_history or [0]), max(commercial_target_history or [0]), max(industrial_target_history or [0]), max(population_history or [0]))    ], title="Demand"),
    )

    return fig


def plot_demand_detail(
    demand_history: list[float] | None = None,
    demand_target_history: list[float] | None = None,
    population_history: list[float] | None = None,
    migration_history: list[float] | None = None,
    lots_history: list[float] | None = None,
    births_history: list[float] | None = None,
    deaths_history: list[float] | None = None,
    title: str = "Demand Detail",
    demand_color: str = RESIDENTIAL_COLOR,
) -> go.Figure:
    """Dual-axis chart: demand/target on right y-axis (-100 to 100),
    population/migration/lots on left y-axis (auto-scaled)."""
    from plotly.subplots import make_subplots

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Determine iteration count
    length = 0
    for hist in (demand_history, demand_target_history, population_history,
                 migration_history, lots_history, births_history, deaths_history):
        if hist is not None:
            length = max(length, len(hist))
    iterations = list(range(length))

    # Left y-axis (absolute values): population, migration, lots
    if population_history is not None:
        fig.add_trace(go.Scatter(
            x=iterations, y=population_history,
            mode="lines", name="Population",
            line=dict(color="black", dash="dot"),
        ), secondary_y=False)

    if migration_history is not None:
        fig.add_trace(go.Scatter(
            x=iterations, y=migration_history,
            mode="lines", name="Migration",
            line=dict(color="purple"),
        ), secondary_y=False)

    if lots_history is not None:
        fig.add_trace(go.Scatter(
            x=iterations, y=lots_history,
            mode="lines", name="Lots",
            line=dict(color="grey"),
        ), secondary_y=False)

    if births_history is not None:
        fig.add_trace(go.Scatter(
            x=iterations, y=births_history,
            mode="lines", name="Births",
            line=dict(color="green"),
        ), secondary_y=False)

    if deaths_history is not None:
        fig.add_trace(go.Scatter(
            x=iterations, y=deaths_history,
            mode="lines", name="Deaths",
            line=dict(color="red"),
        ), secondary_y=False)


    # Right y-axis (-100 to 100): demand and demand target
    if demand_history is not None:
        fig.add_trace(go.Scatter(
            x=iterations, y=demand_history,
            mode="lines", name="Demand",
            line=dict(color=demand_color),
        ), secondary_y=True)

    if demand_target_history is not None:
        fig.add_trace(go.Scatter(
            x=iterations, y=demand_target_history,
            mode="lines", name="Demand Target",
            line=dict(color=demand_color, dash="dash"),
        ), secondary_y=True)

    fig.update_layout(title=title, xaxis=dict(title="Iteration"))
    fig.update_yaxes(title_text="Absolute", secondary_y=False)
    fig.update_yaxes(title_text="Demand", range=[-100, 100], secondary_y=True)

    return fig
