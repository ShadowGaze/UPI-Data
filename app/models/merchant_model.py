from app.models.db import fetchall, fetchone


def get_list(db, search, category, page, per_page):
    conds, params = [], []
    if search:
        conds.append(
            "(merchant_id LIKE ? OR merchant_name LIKE ? OR city LIKE ?)")
        params += [f"%{search}%"] * 3
    if category:
        conds.append("merchant_category=?")
        params.append(category)
    where = ("WHERE " + " AND ".join(conds)) if conds else ""
    total = fetchone(db, f"SELECT COUNT(*) FROM merchants {where}", params)[0]
    offset = (page - 1) * per_page
    rows = fetchall(db,
                    f"SELECT * FROM merchants {where} LIMIT ? OFFSET ?", params + [per_page, offset])
    return rows, total


def get_by_id(db, mid):
    return fetchone(db, "SELECT * FROM merchants WHERE merchant_id=?", (mid,))


def count_all(db):
    return fetchone(db, "SELECT COUNT(*) FROM merchants")[0]


def get_category_peers(db, category, exclude_id):
    return fetchall(db,
                    "SELECT m.merchant_id, m.merchant_name, m.rating,"
                    " COUNT(t.transaction_id) as txn_count"
                    " FROM merchants m"
                    ' LEFT JOIN transactions t ON m.merchant_id=t.receiver_id AND t.receiver_type="merchant"'
                    " WHERE m.merchant_category=? AND m.merchant_id!=?"
                    " GROUP BY m.merchant_id ORDER BY txn_count DESC LIMIT 5",
                    (category, exclude_id))
