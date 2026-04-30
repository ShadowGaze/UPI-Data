from app.models.db import fetchall, fetchone


def get_recent(db, limit=10):
    return fetchall(db,
                    "SELECT * FROM transactions ORDER BY timestamp DESC LIMIT ?", (limit,))


def get_stats(db):
    total = fetchone(db, "SELECT COUNT(*) FROM transactions")[0]
    fraud = fetchone(
        db, "SELECT COUNT(*) FROM transactions WHERE is_fraud=1")[0]
    return {
        "total_transactions": total,
        "total_fraud":        fraud,
        "total_amount":       fetchone(db, "SELECT ROUND(SUM(amount),2) FROM transactions")[0] or 0,
        "fraud_rate":         round(fraud / max(1, total) * 100, 2),
    }


def get_list(db, search, status, fraud, page, per_page):
    conds, params = [], []
    if search:
        conds.append(
            "(transaction_id LIKE ? OR user_id LIKE ? OR payment_app LIKE ? OR transaction_type LIKE ?)")
        params += [f"%{search}%"] * 4
    if status:
        conds.append("status=?")
        params.append(status)
    if fraud != "":
        conds.append("is_fraud=?")
        params.append(int(fraud))
    where = ("WHERE " + " AND ".join(conds)) if conds else ""
    total = fetchone(
        db, f"SELECT COUNT(*) FROM transactions {where}", params)[0]
    offset = (page - 1) * per_page
    rows = fetchall(db,
                    f"SELECT * FROM transactions {where} ORDER BY timestamp DESC LIMIT ? OFFSET ?",
                    params + [per_page, offset])
    return rows, total


def get_by_id(db, tid):
    return fetchone(db, "SELECT * FROM transactions WHERE transaction_id=?", (tid,))


def get_by_user(db, uid, limit=20):
    return fetchall(db,
                    "SELECT * FROM transactions WHERE user_id=? ORDER BY timestamp DESC LIMIT ?",
                    (uid, limit))


def get_by_merchant(db, mid, limit=20):
    return fetchall(db,
                    'SELECT * FROM transactions WHERE receiver_id=? AND receiver_type="merchant"'
                    " ORDER BY timestamp DESC LIMIT ?", (mid, limit))


def get_user_stats(db, uid):
    return fetchone(db,
                    "SELECT COUNT(*) as total, ROUND(SUM(amount),2) as total_amount,"
                    " SUM(is_fraud) as fraud_count, ROUND(AVG(amount),2) as avg_amount"
                    " FROM transactions WHERE user_id=?", (uid,))


def get_merchant_stats(db, mid):
    return fetchone(db,
                    "SELECT COUNT(*) as total, ROUND(SUM(amount),2) as total_amount,"
                    " SUM(is_fraud) as fraud_count, ROUND(AVG(amount),2) as avg_amount"
                    ' FROM transactions WHERE receiver_id=? AND receiver_type="merchant"', (mid,))


# ── Analysis queries ──────────────────────────────────────────────────────────
def fraud_by_app(db):
    return fetchall(db,
                    "SELECT payment_app, SUM(is_fraud) as fraud_count, COUNT(*) as total"
                    " FROM transactions GROUP BY payment_app ORDER BY total DESC")


def by_day_of_week(db):
    return fetchall(db,
                    "SELECT day_of_week, COUNT(*) as count, ROUND(AVG(amount),2) as avg_amount"
                    " FROM transactions GROUP BY day_of_week")


def by_type(db):
    return fetchall(db,
                    "SELECT transaction_type, COUNT(*) as count, ROUND(SUM(amount),2) as total"
                    " FROM transactions GROUP BY transaction_type ORDER BY count DESC")


def by_city_tier(db):
    return fetchall(db,
                    "SELECT user_city_tier, COUNT(*) as count, SUM(is_fraud) as fraud"
                    " FROM transactions GROUP BY user_city_tier")
