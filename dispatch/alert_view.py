def generate_watchlist_table(alerts):
    header = "| Symbol | Strategy | Entry | TP | SL | Score | Catalyst |\n"
    header += "|--------|----------|-------|----|----|-------|-----------|\n"
    rows = []
    for a in alerts:
        row = f"| {a['symbol']} | {a.get('strategy','-')} | £{a.get('entry','-')} | £{a.get('target','-')} | £{a.get('stop','-')} | {a['score']}% | {a.get('catalyst','-')} |"
        rows.append(row)
    return header + "\n".join(rows)

