from flask import Blueprint, render_template, current_app
from app.models.db import get_db
from app.models import transaction_model
import charts

analysis_bp = Blueprint('analysis', __name__)


@analysis_bp.route('/analysis')
def analysis():
    db = get_db()

    # Generate Matplotlib charts (saved as PNG to static/charts/)
    charts.generate_all(db, current_app.root_path)

    return render_template('analysis.html',
                           fraud_by_app=transaction_model.fraud_by_app(db),
                           by_day=transaction_model.by_day_of_week(db),
                           by_type=transaction_model.by_type(db),
                           by_tier=transaction_model.by_city_tier(db))
