from collections import defaultdict
from decimal import Decimal
import plotly.graph_objects as go



def plot_flows_sankey(flows, title="Money flows"):
            agg = defaultdict(Decimal)
            for (s, r, _), (amount, _) in flows.items():
                if s != r:
                    agg[(s, r)] += amount
            nodes = sorted({t for pair in agg for t in pair})
            idx = {n: i for i, n in enumerate(nodes)}
            link = dict(source=[idx[s] for s, _ in agg], target=[idx[r] for _, r in agg],
                        value=[float(v)  for v in agg.values()])
            return go.Figure(go.Sankey(node=dict(label=nodes), link=link), layout_title_text=title)