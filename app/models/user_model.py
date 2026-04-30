from app.models.db import fetchall, fetchone


def get_list(db, search, page, per_page):
    conds, params = [], []
    if search:
        conds.append("(user_id LIKE ? OR city LIKE ? OR preferred_app LIKE ?)")
        params += [f"%{search}%"] * 3
    where = ("WHERE " + " AND ".join(conds)) if conds else ""
    total = fetchone(db, f"SELECT COUNT(*) FROM users {where}", params)[0]
    offset = (page - 1) * per_page
    rows = fetchall(db,
                    f"SELECT * FROM users {where} LIMIT ? OFFSET ?", params + [per_page, offset])
    return rows, total


def get_by_id(db, uid):
    return fetchone(db, "SELECT * FROM users WHERE user_id=?", (uid,))


def count_all(db):
    return fetchone(db, "SELECT COUNT(*) FROM users")[0]
