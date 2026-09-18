"""
Markdown tables for the bank flow matrix.

Usage in the notebook:
    from IPython.display import Markdown, display
    display(Markdown(flows_to_markdown(history['flows'][-1], title="Money flows, last month")))
"""
from collections import defaultdict
from decimal import Decimal


def _short(owner_type: str) -> str:
    """'ResidentialEntity' -> 'Residential'."""
    return owner_type.removesuffix('Entity')


def _cell(text: str) -> str:
    """Escape characters that break a markdown table cell."""
    return str(text).replace('|', '\\|').replace('\n', ' ')


def flows_to_markdown(flows: dict, title: str | None = None,
                      include_same_type: bool = False,
                      include_sector_summary: bool = True) -> str:
    """
    Make a markdown table from one flow matrix (the dict that take_flows() returns).

    Args:
        - flows: {(sender_type, receiver_type, purpose): [amount, count]}
        - title: Optional heading above the tables.
        - include_same_type: Include transfers inside one sector (for example
          Residential to Residential). These do not move money between tanks.
        - include_sector_summary: Add a second table with inflow, outflow and
          net change for each sector.
    Returns:
        - str: Markdown text.
    """
    rows = [(s, r, p, Decimal(a), int(n)) for (s, r, p), (a, n) in flows.items()
            if include_same_type or s != r]
    if not rows:
        return f'**{title}**\n\nNo flows in this period.' if title else 'No flows in this period.'

    rows.sort(key=lambda row: row[3], reverse=True)
    total = sum(row[3] for row in rows)

    lines = []
    if title:
        lines += [f'**{title}**', '']
    lines += ['| From | To | Purpose | Amount | Share | Transfers | Avg / transfer |',
              '|:---|:---|:---|---:|---:|---:|---:|']
    for s, r, p, amount, count in rows:
        share = amount / total if total else Decimal(0)
        avg = amount / count if count else Decimal(0)
        lines.append(f'| {_short(s)} | {_short(r)} | {_cell(p)} | {amount:,.2f} | '
                     f'{share:.1%} | {count:,} | {avg:,.2f} |')
    lines.append(f'| **Total** | | | **{total:,.2f}** | 100.0% | '
                 f'**{sum(row[4] for row in rows):,}** | |')

    if include_sector_summary:
        inflow = defaultdict(Decimal)
        outflow = defaultdict(Decimal)
        for s, r, _, amount, _ in rows:
            if s != r:
                outflow[s] += amount
                inflow[r] += amount
        sectors = sorted(set(inflow) | set(outflow),
                         key=lambda t: inflow[t] - outflow[t], reverse=True)
        lines += ['', '| Sector | In | Out | Net |', '|:---|---:|---:|---:|']
        for t in sectors:
            net = inflow[t] - outflow[t]
            lines.append(f'| {_short(t)} | {inflow[t]:,.2f} | {outflow[t]:,.2f} | {net:+,.2f} |')

    return '\n'.join(lines)