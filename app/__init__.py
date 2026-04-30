from flask import Flask, render_template
from app.models.db import close_db
from app.controllers.main_controller import main_bp
from app.controllers.transaction_controller import transactions_bp
from app.controllers.user_controller import users_bp
from app.controllers.merchant_controller import merchants_bp
from app.controllers.analysis_controller import analysis_bp


def create_app():
    app = Flask(__name__)

    # ── Register DB teardown ───────────────────────────────────────────────────
    app.teardown_appcontext(close_db)

    # ── Register Blueprints (Controllers) ─────────────────────────────────────
    app.register_blueprint(main_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(merchants_bp)
    app.register_blueprint(analysis_bp)

    # ── Error Handlers ────────────────────────────────────────────────────────
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500

    return app
