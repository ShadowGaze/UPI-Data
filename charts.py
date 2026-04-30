import os


def generate_all(db, root_path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    charts_dir = os.path.join(root_path, "static", "charts")
    os.makedirs(charts_dir, exist_ok=True)

    TEAL = "#01696f"
    PURPLE = "#a12c7b"
    COLORS = ["#01696f", "#4f98a3", "#a12c7b", "#437a22", "#d19900", "#006494"]

    def clean(ax):
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(labelsize=9)

    # ── Chart 1: Fraud vs Legitimate ─────────────────────────────────────────
    rows = db.execute(
        "SELECT is_fraud, COUNT(*) FROM transactions GROUP BY is_fraud").fetchall()
    counts = {r[0]: r[1] for r in rows}
    fig, ax = plt.subplots(figsize=(5, 3.5))
    bars = ax.bar(["Legitimate", "Fraud"],
                  [counts.get(0, 0), counts.get(1, 0)],
                  color=[TEAL, PURPLE], width=0.5)
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2,
                b.get_height() + 20, f"{b.get_height():,}", ha="center", fontsize=9)
    ax.set_title("Fraud vs Legitimate Transactions", fontweight="bold")
    ax.set_ylabel("Count")
    clean(ax)
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, "fraud_bar.png"),
                dpi=100, bbox_inches="tight")
    plt.close()

    # ── Chart 2: Transactions by Payment App ─────────────────────────────────
    rows = db.execute(
        "SELECT payment_app, COUNT(*) FROM transactions GROUP BY payment_app ORDER BY COUNT(*) DESC"
    ).fetchall()
    if rows:
        apps, cnts = zip(*rows)
        fig, ax = plt.subplots(figsize=(6, 3.5))
        ax.bar(apps, cnts, color=TEAL)
        ax.set_title("Transactions by Payment App", fontweight="bold")
        ax.set_ylabel("Count")
        plt.xticks(rotation=20, ha="right", fontsize=9)
        clean(ax)
        plt.tight_layout()
        plt.savefig(os.path.join(charts_dir, "payment_apps.png"),
                    dpi=100, bbox_inches="tight")
        plt.close()

    # ── Chart 3: Hourly Volume ────────────────────────────────────────────────
    rows = db.execute(
        "SELECT hour_of_day, COUNT(*) FROM transactions GROUP BY hour_of_day ORDER BY hour_of_day"
    ).fetchall()
    if rows:
        hours, hcnts = zip(*rows)
        fig, ax = plt.subplots(figsize=(7, 3.5))
        ax.plot(hours, hcnts, color=TEAL,
                linewidth=2, marker="o", markersize=4)
        ax.fill_between(hours, hcnts, alpha=0.15, color=TEAL)
        ax.set_title("Transaction Volume by Hour of Day", fontweight="bold")
        ax.set_xlabel("Hour")
        ax.set_ylabel("Count")
        ax.set_xticks(range(0, 24))
        clean(ax)
        plt.tight_layout()
        plt.savefig(os.path.join(charts_dir, "hourly.png"),
                    dpi=100, bbox_inches="tight")
        plt.close()

    # ── Chart 4: Transaction Type Pie ────────────────────────────────────────
    rows = db.execute(
        "SELECT transaction_type, COUNT(*) FROM transactions"
        " GROUP BY transaction_type ORDER BY COUNT(*) DESC LIMIT 6"
    ).fetchall()
    if rows:
        types, tcnts = zip(*rows)
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(tcnts, labels=types, autopct="%1.1f%%", colors=COLORS,
               startangle=140, wedgeprops={"edgecolor": "white", "linewidth": 1.5})
        ax.set_title("Transaction Type Distribution", fontweight="bold")
        plt.tight_layout()
        plt.savefig(os.path.join(charts_dir, "txn_pie.png"),
                    dpi=100, bbox_inches="tight")
        plt.close()
