from flask import Blueprint, render_template
from app.models.db import get_db
from app.models import transaction_model, user_model, merchant_model

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    db = get_db()
    # Combine stats from all three models
    txn_stats = transaction_model.get_stats(db)
    stats = {
        **txn_stats,
        "total_users":     user_model.count_all(db),
        "total_merchants": merchant_model.count_all(db),
    }
    recent = transaction_model.get_recent(db)
    return render_template('index.html', stats=stats, recent=recent)
