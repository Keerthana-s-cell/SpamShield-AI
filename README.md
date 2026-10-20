# 🛡️ SpamShield AI — Smart Messages. Safer Digital Life.

> **AI-Powered SMS Spam & Smishing Detection System**  
> Built with **Python**, **Scikit-learn**, and **Flask** (Vercel Serverless Ready).  
> *Original Streamlit edition backed up in `app_streamlit_backup.py`*.

---

## 📌 Project Overview
**SpamShield AI** is an intelligent cybersecurity web application designed to protect mobile users from fraudulent text messages, smishing campaigns, promotional unsolicited spam, and lottery scams.

The application loads an existing pre-trained machine learning pipeline comprising **TF-IDF (Term Frequency-Inverse Document Frequency)** feature vectorization and a **Linear Support Vector Classifier (LinearSVC)**. It provides real-time inference, risk assessment cards, dynamic session threat telemetry, and an expandable model methodology section.

---

## 🎨 Design & Aesthetic Features
- **Cybersecurity Modern Theme:** Deep navy and obsidian background palette (`#04070f`, `#080d1a`, `#0d1b2e`) with electric blue (`#38bdf8`) and neon cyan (`#00f2fe`) glowing highlights.
- **Glassmorphism Panels:** Translucent card containers with backdrop blur, glowing borders, and rounded corners.
- **Dynamic Session Dashboard:** Real-time telemetry tracking total messages scanned, spam detected, clean messages, and threat incidence ratio during the current browser session.
- **One-Click Sample Payloads:** Instant testing buttons for legitimate messages, urgent promotional spam, and smishing prize scams.
- **Balanced Security Warnings:** Displays actionable recommendations for suspicious messages while adhering to ethical ML standards (never asserting absolute certainty).
- **Responsive Layout:** Optimized for desktop monitors, laptops, and mobile screens.

---

## 📁 Project Directory Structure
```
ml project/
├── api/
│   ├── index.py              # Vercel serverless WSGI entrypoint (Flask)
│   └── spam_model.pkl        # Model pipeline bundled inside api directory
├── static/
│   ├── css/
│   │   └── style.css         # Cybersecurity dark theme & glassmorphic styling
│   └── js/
│       └── app.js            # Live character counter, AJAX scanning, telemetry
├── templates/
│   └── index.html            # Main HTML dashboard layout & result cards
├── app.py                    # Root Flask app (for local execution: python app.py)
├── app_streamlit_backup.py   # Complete backup of original Streamlit application
├── spam_model.pkl            # Original trained TF-IDF + LinearSVC pipeline
├── requirements.txt          # Production dependencies: Flask & scikit-learn
├── vercel.json               # Vercel serverless deployment configuration
├── run_app.bat               # 1-Click launcher for local Flask web application
├── run_streamlit_backup.bat  # 1-Click launcher for backup Streamlit app
└── README.md                 # Project documentation & deployment guide
```

---

## 🚀 Running Locally

### Step 1: Install Dependencies
Open your PowerShell or Command Prompt in the project folder and run:
```bash
pip install -r requirements.txt
```

### Step 2: Start the Web Server
- **Option A (One-Click):** Double-click `run_app.bat` in the project directory.
- **Option B (PowerShell / Terminal):**
  ```powershell
  python app.py
  ```
The web dashboard will be available at: **`http://127.0.0.1:5000`**.

---

## 🌐 Deploying to Vercel via GitHub (Step-by-Step)

### Step 1: Commit and Push Files to Your GitHub Repository
Open PowerShell or your terminal in the project directory:

```bash
# 1. Check changed files
git status

# 2. Stage all files (Flask app, api/index.py, templates, static, vercel.json, model)
git add .

# 3. Commit the changes
git commit -m "Convert SpamShield AI to Vercel-ready Flask web application"

# 4. Push to your GitHub repository
git push origin main
```
*(If your default branch is `master`, replace `main` with `master`).*

### Step 2: Import Project in Vercel
1. Log in to [vercel.com](https://vercel.com/) with your GitHub account.
2. Click the **"Add New..."** button in your Vercel Dashboard and select **"Project"**.
3. Locate your repository (`spamshield-ai` or your repo name) from the list and click **"Import"**.
4. In the **Configure Project** screen:
   - **Framework Preset:** Select **"Other"** (Vercel automatically detects Python via `api/index.py` and `vercel.json`).
   - **Root Directory:** Leave as `./` (default).
   - **Build & Output Settings:** Leave default (no build command needed).
   - **Environment Variables:** None needed.
5. Click **"Deploy"**.

### Step 3: Verify the Live Deployment
1. Wait 30–60 seconds while Vercel builds the Python serverless bundle and deploys the CDN assets.
2. Click on the generated domain (e.g., `https://spamshield-ai.vercel.app`).
3. Test sample messages, character counting, and threat scanning on your live public URL!

---

## 🎯 Model Pipeline & Evaluation Metrics

- **Dataset:** SMS Spam Collection (5,572 labeled messages)
- **Feature Extraction:** TF-IDF (Term Frequency – Inverse Document Frequency)
- **Classifier:** Linear Support Vector Classifier (`LinearSVC`)

### Test Partition Metrics (80/20 Test Split)
| Metric | Score | Note |
| :--- | :---: | :--- |
| **Accuracy** | **98.48%** | Overall correct classifications on holdout split |
| **Spam Precision** | **98.53%** | Minimizes false alarms on legitimate communications |
| **Spam Recall** | **89.93%** | High capture rate of unsolicited spam/smishing |
| **Spam F1-Score** | **94.04%** | Harmonic balance between precision and recall |

---

## 📄 License & Credits
- **Built with:** Python, Scikit-learn, and Flask
- **Project:** SpamShield AI — College Machine Learning Showcase
- **Theme:** Cybersecurity Dashboard Aesthetic
