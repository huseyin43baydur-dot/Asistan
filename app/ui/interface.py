import datetime
import logging
import os
import urllib.parse

from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from openai import OpenAI

logger = logging.getLogger(__name__)

ui_bp = Blueprint("ui", __name__)


def _get_ai_response(prompt, model=None):
    """Send *prompt* to OpenAI and return the reply text."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return (
            "OpenAI API anahtarı ayarlanmamış. "
            "Lütfen OPENAI_API_KEY ortam değişkenini ayarlayın."
        )
    from app import ALLOWED_MODELS
    if model not in ALLOWED_MODELS:
        model = "gpt-4o-mini"
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    except Exception:  # noqa: BLE001
        logger.exception("OpenAI API çağrısı başarısız oldu")
        return "Bir hata oluştu, lütfen daha sonra tekrar deneyin."


def _handle_command(command):
    """Return a response string for known built-in commands or None."""
    lower = command.lower()

    if "saat kaç" in lower:
        now = datetime.datetime.now().strftime("%H:%M")
        return f"Saat {now}."

    if "google'da ara" in lower:
        query = lower.replace("google'da ara", "").strip()
        url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"
        return f'<a href="{url}" target="_blank" rel="noopener noreferrer">Google\'da aranıyor: {query}</a>'

    if "youtube aç" in lower:
        return '<a href="https://youtube.com" target="_blank" rel="noopener noreferrer">YouTube açılıyor →</a>'

    return None


# ── Routes ──────────────────────────────────────────────────────────────────

@ui_bp.route("/")
def dashboard():
    conversations = session.get("conversations", [])
    today = datetime.date.today().isoformat()
    return render_template("dashboard.html", conversations=conversations, today=today)


@ui_bp.route("/chat", methods=["GET", "POST"])
def chat():
    if "messages" not in session:
        session["messages"] = []

    if request.method == "POST":
        user_message = request.form.get("message", "").strip()
        if user_message:
            now = datetime.datetime.now().strftime("%H:%M")
            built_in = _handle_command(user_message)
            current_model = session.get("settings", {}).get("model", "gpt-4o-mini")
            reply = built_in if built_in is not None else _get_ai_response(user_message, model=current_model)

            messages = list(session["messages"])
            messages.append({"role": "user", "content": user_message, "time": now})
            messages.append({"role": "assistant", "content": reply, "time": now})
            session["messages"] = messages

            # Persist to conversation history shown on dashboard
            conversations = list(session.get("conversations", []))
            conversations.append(
                {
                    "id": len(conversations) + 1,
                    "date": datetime.date.today().isoformat(),
                    "category": "sohbet",
                    "content": user_message,
                }
            )
            session["conversations"] = conversations

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"messages": messages})

        return redirect(url_for("ui.chat"))

    return render_template("chat.html", messages=session.get("messages", []))


@ui_bp.route("/chat/clear", methods=["POST"])
def clear_chat():
    session["messages"] = []
    return jsonify({"status": "ok"})


@ui_bp.route("/settings", methods=["GET", "POST"])
def settings():
    saved = False
    if request.method == "POST":
        from app import ALLOWED_MODELS
        model = request.form.get("model", "gpt-4o-mini").strip()
        if model not in ALLOWED_MODELS:
            model = "gpt-4o-mini"
        session["settings"] = {"model": model}
        saved = True
    current_settings = session.get("settings", {"model": "gpt-4o-mini"})
    return render_template("settings.html", settings=current_settings, saved=saved)


if __name__ == "__main__":
    from app import create_app
    _debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    create_app().run(debug=_debug)
