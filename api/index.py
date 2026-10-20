"""
=============================================================================
SpamShield AI — Vercel Serverless Entrypoint & Flask Application
=============================================================================
A modern cybersecurity SMS Spam Detection web application built with:
- Python 3 & Flask
- Scikit-learn (TF-IDF Vectorizer + LinearSVC Pipeline)
- Pre-trained spam_model.pkl

Compatible with: Local execution and Vercel Serverless Functions
=============================================================================
"""

import os
import pickle
import warnings
from flask import Flask, render_template, request, jsonify

# Suppress version mismatch warnings for clean logging
warnings.filterwarnings("ignore")

# Resolve directories safely across both local and Vercel serverless environments
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)

def resolve_directory(dir_name):
    candidates = [
        os.path.join(PARENT_DIR, dir_name),
        os.path.join(CURRENT_DIR, dir_name),
        os.path.join(os.getcwd(), dir_name),
        os.path.join(os.getcwd(), "api", dir_name)
    ]
    for c in candidates:
        if os.path.exists(c) and os.path.isdir(c):
            return c
    return os.path.join(PARENT_DIR, dir_name)

TEMPLATE_DIR = resolve_directory("templates")
STATIC_DIR = resolve_directory("static")

# Initialize Flask WSGI application instance
app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
    static_url_path="/static"
)

# -----------------------------------------------------------------------------
# MODEL LOADER
# -----------------------------------------------------------------------------
def load_spam_model():
    """
    Locates and unpickles the trained TF-IDF + LinearSVC pipeline.
    Searches adjacent files, parent directory, and working directory.
    """
    candidate_paths = [
        os.path.join(CURRENT_DIR, "spam_model.pkl"),
        os.path.join(PARENT_DIR, "spam_model.pkl"),
        os.path.join(os.getcwd(), "spam_model.pkl"),
        os.path.join(os.getcwd(), "api", "spam_model.pkl"),
        os.path.join(CURRENT_DIR, "spam_model (1).pkl"),
        os.path.join(PARENT_DIR, "spam_model (1).pkl"),
        "spam_model.pkl"
    ]
    for p in candidate_paths:
        if os.path.exists(p):
            try:
                with open(p, "rb") as f:
                    model = pickle.load(f)
                return model, p, None
            except Exception as e:
                return None, p, str(e)
    return None, None, "Trained model 'spam_model.pkl' not found in candidate paths."

# Load model at startup
model, loaded_path, load_error = load_spam_model()


# -----------------------------------------------------------------------------
# APPLICATION ROUTES
# -----------------------------------------------------------------------------
@app.route("/", methods=["GET"])
def index():
    """Serves the main SpamShield AI cybersecurity dashboard."""
    return render_template(
        "index.html",
        model_loaded=(model is not None),
        load_error=load_error
    )


@app.route("/predict", methods=["POST"])
def predict():
    """
    Evaluates incoming SMS text payload using TF-IDF + LinearSVC pipeline.
    Returns JSON response containing prediction label and decision distance.
    """
    global model, load_error
    if model is None:
        model, _, load_error = load_spam_model()
        if model is None:
            return jsonify({
                "error": f"Machine learning model is unavailable: {load_error}"
            }), 500

    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "error": "Empty message. Please enter or paste an SMS text to scan."
        }), 400

    try:
        # Predict using trained pipeline
        prediction = model.predict([message])[0]

        # Calculate decision function distance score if supported
        decision_score = None
        if hasattr(model, "decision_function"):
            try:
                decision_score = float(model.decision_function([message])[0])
            except Exception:
                decision_score = None

        return jsonify({
            "message": message,
            "prediction": str(prediction),
            "score": decision_score
        })
    except Exception as ex:
        return jsonify({
            "error": f"Inference processing failed: {str(ex)}"
        }), 500


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint for deployment monitoring."""
    return jsonify({
        "status": "healthy",
        "app": "SpamShield AI",
        "model_loaded": model is not None,
        "model_source": loaded_path
    })


# Local execution handler
if __name__ == "__main__":
    print(f"[*] SpamShield AI Flask Server running on http://127.0.0.1:5000")
    print(f"[*] Model loaded: {model is not None} ({loaded_path})")
    app.run(host="127.0.0.1", port=5000, debug=True)
