from flask import Blueprint, render_template, request, abort
from app.models.db import get_db, get_distinct
from app.models import merchant_model, transaction_model

merchants_bp = Blueprint('merchants', __name__)


@merchants_bp.route('/merchants')
def list_merchants():
    db = get_db()
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '')
    page = max(1, int(request.args.get('page', 1)))

    rows, total = merchant_model.get_list(db, search, category, page, 50)
    total_pages = max(1, (total + 49) // 50)
    categories = get_distinct(db, 'merchants', 'merchant_category')

    return render_template('merchants_list.html',
                           merchants=rows, search=search, category=category,
                           page=page, total_pages=total_pages, total=total,
                           categories=categories)


@merchants_bp.route('/merchants/<mid>')
def merchant_detail(mid):
    db = get_db()
    merchant = merchant_model.get_by_id(db, mid)
    if not merchant:
        abort(404)

    txns = transaction_model.get_by_merchant(db, mid)
    merchant_stats = transaction_model.get_merchant_stats(db, mid)
    peers = merchant_model.get_category_peers(
        db, merchant['merchant_category'], mid)

    return render_template('merchant_detail.html',
                           merchant=merchant, transactions=txns,
                           merchant_stats=merchant_stats, peers=peers)
