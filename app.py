"""
=============================================================================
SpamShield AI — Main Flask Web Application Entrypoint
=============================================================================
Project: SpamShield AI — Smart Messages. Safer Digital Life.
Model: TF-IDF Vectorizer + LinearSVC (spam_model.pkl)
Framework: Flask + Vanilla CSS/JS
Compatibility: Local execution (python app.py) & Vercel deployment

Note: Original Streamlit application is backed up in app_streamlit_backup.py
=============================================================================
"""

import sys
import os

# Ensure api directory is reachable
api_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "api")
if api_dir not in sys.path:
    sys.path.insert(0, api_dir)

# Import the configured Flask WSGI app from api/index.py
from index import app, model, loaded_path

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print("=" * 70)
    print(" SpamShield AI — Flask Web Application Server")
    print("=" * 70)
    print(f"[*] Access URL:   http://127.0.0.1:{port}")
    print(f"[*] Model loaded: {model is not None}")
    if loaded_path:
        print(f"[*] Model path:   {loaded_path}")
    print("=" * 70)
    app.run(host="0.0.0.0", port=port, debug=False)
