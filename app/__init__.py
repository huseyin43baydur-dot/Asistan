import logging
import os
from flask import Flask

logger = logging.getLogger(__name__)

ALLOWED_MODELS = {"gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"}


def create_app():
    app = Flask(__name__, template_folder="ui/templates")

    secret_key = os.environ.get("SECRET_KEY")
    if not secret_key:
        logger.warning(
            "SECRET_KEY ortam değişkeni ayarlanmamış. "
            "Üretim ortamında güçlü bir anahtar kullanın."
        )
        secret_key = "asistan-gizli-anahtar-degistirin"
    app.secret_key = secret_key

    from app.ui.interface import ui_bp
    app.register_blueprint(ui_bp)

    return app
