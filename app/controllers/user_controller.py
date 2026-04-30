from flask import Blueprint, render_template, request, abort
from app.models.db import get_db
from app.models import user_model, transaction_model

users_bp = Blueprint('users', __name__)


@users_bp.route('/users')
def list_users():
    db = get_db()
    search = request.args.get('search', '').strip()
    page = max(1, int(request.args.get('page', 1)))

    rows, total = user_model.get_list(db, search, page, 50)
    total_pages = max(1, (total + 49) // 50)

    return render_template('users_list.html',
                           users=rows, search=search,
                           page=page, total_pages=total_pages, total=total)


@users_bp.route('/users/<uid>')
def user_detail(uid):
    db = get_db()
    user = user_model.get_by_id(db, uid)
    if not user:
        abort(404)

    txns = transaction_model.get_by_user(db, uid)
    user_stats = transaction_model.get_user_stats(db, uid)

    return render_template('user_detail.html',
                           user=user, transactions=txns, user_stats=user_stats)
