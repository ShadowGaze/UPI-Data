from flask import Blueprint, render_template, request, abort
from app.models.db import get_db, get_distinct
from app.models import transaction_model, user_model, merchant_model

transactions_bp = Blueprint('transactions', __name__)


@transactions_bp.route('/transactions')
def list_transactions():
    db = get_db()
    search = request.args.get('search', '').strip()
    status = request.args.get('status', '')
    fraud = request.args.get('fraud', '')
    page = max(1, int(request.args.get('page', 1)))

    rows, total = transaction_model.get_list(
        db, search, status, fraud, page, 50)
    total_pages = max(1, (total + 49) // 50)
    statuses = get_distinct(db, 'transactions', 'status')

    return render_template('transactions_list.html',
                           transactions=rows, search=search, status=status, fraud=fraud,
                           page=page, total_pages=total_pages, total=total, statuses=statuses)


@transactions_bp.route('/transactions/<tid>')
def transaction_detail(tid):
    db = get_db()
    txn = transaction_model.get_by_id(db, tid)
    if not txn:
        abort(404)

    user = user_model.get_by_id(db, txn['user_id'])
    merchant = None
    if txn['receiver_type'] == 'merchant':
        merchant = merchant_model.get_by_id(db, txn['receiver_id'])

    return render_template('transaction_detail.html',
                           txn=txn, user=user, merchant=merchant)
