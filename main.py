from app import create_app

if __name__ == "__main__":
    import os
    _debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app = create_app()
    app.run(debug=_debug, host="0.0.0.0", port=5000)
