from decimal import Decimal

import plotly.graph_objects as go

from utils.plotly_graphs.graph_config import (
	COMMERCIAL_COLOR,
	INDUSTRIAL_COLOR,
	RESIDENTIAL_COLOR,
)


MoneyValue = Decimal | float | int


def plot_economy_money_history(
	industrial_money_history: list[MoneyValue] | None = None,
	commercial_money_history: list[MoneyValue] | None = None,
	residential_money_history: list[MoneyValue] | None = None,
	wholesale_money_history: list[MoneyValue] | None = None,
	government_money_history: list[MoneyValue] | None = None,
	title: str = "Money by Actor Type Over Time",
) -> go.Figure:
	"""Plot total bank balances by actor type for each simulation iteration."""
	fig = go.Figure()

	series = (
		(industrial_money_history, "Industrial", INDUSTRIAL_COLOR),
		(commercial_money_history, "Commercial", COMMERCIAL_COLOR),
		(residential_money_history, "Residential", RESIDENTIAL_COLOR),
		(wholesale_money_history, "Wholesale", "rgb(156, 39, 176)"),
		(government_money_history, "Government", "rgb(96, 125, 139)"),
	)

	for money_history, name, color in series:
		if money_history is None:
			continue

		balances = [float(balance) for balance in money_history]
		fig.add_trace(go.Scatter(
			x=list(range(len(balances))),
			y=balances,
			mode="lines",
			name=name,
			line=dict(color=color, width=2.5),
			hovertemplate=(
				f"<b>{name}</b><br>"
				"Iteration %{x}<br>Balance: $%{y:,.2f}<extra></extra>"
			),
		))

	fig.update_layout(
		title=title,
		template="plotly_white",
		xaxis=dict(title="Iteration"),
		yaxis=dict(title="Total Balance ($)", rangemode="tozero", tickformat="$,.2f"),
		legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
		hovermode="x unified",
		margin=dict(t=80, r=40),
	)

	return fig
