"""
=============================================================================
SpamShield AI — Smart Messages. Safer Digital Life.
=============================================================================
A modern cybersecurity-themed SMS Spam Detection web application built with:
- Streamlit
- Scikit-learn (TF-IDF Vectorizer + LinearSVC Pipeline)
- Python 3

Author: Academic Machine Learning Project
Compatible with: Local execution, GitHub, and Streamlit Community Cloud
=============================================================================
"""

import os
import pickle
import warnings
from datetime import datetime
import streamlit as st

# Suppress unpickling version warnings for a clean user interface
warnings.filterwarnings("ignore")

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & THEME
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SpamShield AI — Smart Messages. Safer Digital Life.",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# 2. CYBERSECURITY CUSTOM CSS STYLING
# -----------------------------------------------------------------------------
# Custom dark navy, neon cyan, electric blue, and glassmorphism styling
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global Body and App Styling */
    html, body, [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 15% 15%, #0d1b2e 0%, #080d1a 45%, #04070f 100%) !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Hide standard Streamlit header and deploy button if desired */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* Main container padding */
    .block-container {
        padding-top: 1.8rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1200px !important;
    }

    /* Glassmorphic Container Card */
    .cyber-card {
        background: rgba(13, 23, 42, 0.65);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(0, 242, 254, 0.16);
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.6), 0 0 1px 1px rgba(0, 242, 254, 0.08);
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }
    .cyber-card:hover {
        border-color: rgba(0, 242, 254, 0.32);
        box-shadow: 0 14px 40px -10px rgba(0, 242, 254, 0.12), 0 0 1px 1px rgba(0, 242, 254, 0.18);
    }

    /* Header Container */
    .header-box {
        text-align: center;
        padding: 30px 20px 20px 20px;
        margin-bottom: 20px;
    }

    .cyber-badge {
        display: inline-block;
        padding: 6px 16px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        border-radius: 50px;
        background: rgba(0, 242, 254, 0.08);
        border: 1px solid rgba(0, 242, 254, 0.4);
        color: #00f2fe;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.25);
        margin-bottom: 14px;
    }

    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -1px;
        background: linear-gradient(135deg, #ffffff 20%, #70d6ff 60%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 6px;
    }

    .sub-title {
        font-size: 1.15rem;
        font-weight: 500;
        color: #94a3b8;
        letter-spacing: 0.5px;
        margin-bottom: 14px;
    }

    .intro-text {
        font-size: 0.95rem;
        color: #cbd5e1;
        max-width: 760px;
        margin: 0 auto;
        line-height: 1.6;
    }

    /* Stat Dashboard Cards */
    .stat-card {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(56, 189, 248, 0.18);
        border-radius: 14px;
        padding: 18px 20px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
        position: relative;
        overflow: hidden;
        transition: transform 0.25s ease, border-color 0.25s ease;
    }
    .stat-card:hover {
        transform: translateY(-3px);
        border-color: rgba(56, 189, 248, 0.45);
    }
    .stat-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #00f2fe, #3b82f6);
    }
    .stat-card.spam-stat::before {
        background: linear-gradient(90deg, #f97316, #ef4444);
    }
    .stat-card.ham-stat::before {
        background: linear-gradient(90deg, #10b981, #06b6d4);
    }
    .stat-card.ratio-stat::before {
        background: linear-gradient(90deg, #8b5cf6, #ec4899);
    }

    .stat-val {
        font-size: 2.1rem;
        font-weight: 800;
        color: #f8fafc;
        font-family: 'JetBrains Mono', monospace;
        margin: 4px 0;
    }
    .stat-lbl {
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 1px;
        color: #94a3b8;
        text-transform: uppercase;
    }

    /* Prediction Cards */
    .result-card-spam {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.12) 0%, rgba(249, 115, 22, 0.08) 100%);
        border: 1px solid rgba(239, 68, 68, 0.4);
        border-radius: 16px;
        padding: 24px 28px;
        box-shadow: 0 0 35px rgba(239, 68, 68, 0.18);
        margin-top: 20px;
    }
    .result-card-ham {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%, rgba(6, 182, 212, 0.08) 100%);
        border: 1px solid rgba(16, 185, 129, 0.4);
        border-radius: 16px;
        padding: 24px 28px;
        box-shadow: 0 0 35px rgba(16, 185, 129, 0.18);
        margin-top: 20px;
    }

    .result-badge-spam {
        display: inline-block;
        padding: 6px 14px;
        font-size: 0.8rem;
        font-weight: 800;
        letter-spacing: 1.5px;
        border-radius: 6px;
        background: rgba(239, 68, 68, 0.2);
        color: #fca5a5;
        border: 1px solid rgba(239, 68, 68, 0.6);
        margin-bottom: 10px;
    }
    .result-badge-ham {
        display: inline-block;
        padding: 6px 14px;
        font-size: 0.8rem;
        font-weight: 800;
        letter-spacing: 1.5px;
        border-radius: 6px;
        background: rgba(16, 185, 129, 0.2);
        color: #6ee7b7;
        border: 1px solid rgba(16, 185, 129, 0.6);
        margin-bottom: 10px;
    }

    .result-title-spam {
        font-size: 1.8rem;
        font-weight: 800;
        color: #ef4444;
        margin-bottom: 8px;
    }
    .result-title-ham {
        font-size: 1.8rem;
        font-weight: 800;
        color: #10b981;
        margin-bottom: 8px;
    }

    .msg-preview-box {
        background: rgba(10, 15, 30, 0.8);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 10px;
        padding: 14px 18px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.88rem;
        color: #e2e8f0;
        margin: 14px 0;
        word-break: break-word;
        white-space: pre-wrap;
    }

    .security-notice {
        font-size: 0.82rem;
        color: #94a3b8;
        border-left: 3px solid #f59e0b;
        padding-left: 12px;
        margin-top: 14px;
        line-height: 1.5;
    }

    /* Metric Badges in Model Info */
    .metric-chip {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(0, 242, 254, 0.25);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }
    .metric-chip-num {
        font-size: 1.6rem;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
        color: #00f2fe;
    }
    .metric-chip-name {
        font-size: 0.75rem;
        color: #94a3b8;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-top: 4px;
    }

    /* Character Counter */
    .counter-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: #00f2fe;
        background: rgba(0, 242, 254, 0.08);
        padding: 4px 12px;
        border-radius: 6px;
        border: 1px solid rgba(0, 242, 254, 0.2);
    }

    /* Streamlit Button & Text Area Customization */
    div[data-testid="stTextArea"] textarea {
        background-color: #0b1324 !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 12px !important;
        color: #f1f5f9 !important;
        font-size: 0.96rem !important;
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    div[data-testid="stTextArea"] textarea:focus {
        border-color: #00f2fe !important;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.25) !important;
    }

    /* Streamlit Expander */
    div[data-testid="stExpander"] {
        background: rgba(13, 23, 42, 0.6) !important;
        border: 1px solid rgba(0, 242, 254, 0.2) !important;
        border-radius: 14px !important;
        overflow: hidden;
    }
    div[data-testid="stExpander"] details summary {
        font-weight: 600 !important;
        color: #7dd3fc !important;
    }

    /* Footer */
    .footer-container {
        text-align: center;
        padding-top: 40px;
        padding-bottom: 20px;
        color: #64748b;
        font-size: 0.85rem;
        border-top: 1px solid rgba(148, 163, 184, 0.1);
        margin-top: 50px;
    }
    .footer-container strong {
        color: #94a3b8;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 3. SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
# Initialize session statistics strictly from real session usage (no fabrication)
if "total_scanned" not in st.session_state:
    st.session_state.total_scanned = 0

if "spam_detected" not in st.session_state:
    st.session_state.spam_detected = 0

if "ham_detected" not in st.session_state:
    st.session_state.ham_detected = 0

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "sms_input" not in st.session_state:
    st.session_state.sms_input = ""


# -----------------------------------------------------------------------------
# 4. MODEL LOADER (TF-IDF + LinearSVC Pipeline)
# -----------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_spam_model():
    """
    Loads the trained model pipeline from the project directory.
    Supports 'spam_model.pkl' or fallback 'spam_model (1).pkl'.
    Does not modify or retrain the existing pipeline.
    """
    candidate_filenames = ["spam_model.pkl", "spam_model (1).pkl"]
    for filename in candidate_filenames:
        if os.path.exists(filename):
            try:
                with open(filename, "rb") as f:
                    model = pickle.load(f)
                return model, filename, None
            except Exception as e:
                return None, filename, str(e)
    return None, None, "Model file 'spam_model.pkl' was not found in the project root."


model, loaded_filename, load_error = load_spam_model()


# -----------------------------------------------------------------------------
# 5. HEADER SECTION
# -----------------------------------------------------------------------------
st.markdown("""
<div class="header-box">
    <div class="cyber-badge">
        <span>🛡️ AI-POWERED SMS PROTECTION</span>
    </div>
    <div class="main-title">SpamShield AI</div>
    <div class="sub-title">Smart Messages. Safer Digital Life.</div>
    <p class="intro-text">
        Every day, millions of deceptive SMS messages (smishing, urgent lottery scams, and fraudulent bank alerts)
        are transmitted to exploit digital users. <strong>SpamShield AI</strong> utilizes machine learning powered by
        <strong>TF-IDF Vectorization</strong> and <strong>Linear Support Vector Classification (LinearSVC)</strong>
        to inspect message semantics in real time and evaluate whether incoming texts exhibit patterns typical of spam.
    </p>
</div>
""", unsafe_allow_html=True)

# If model loading failed, notify the user immediately with clean error handling
if model is None:
    st.error(f"""
    🚨 **Model Loading Alert:** Could not load the machine learning model.
    - **Details:** {load_error}
    - **Solution:** Ensure that your trained `spam_model.pkl` file is placed inside the project directory.
    """)


# -----------------------------------------------------------------------------
# 6. SESSION DASHBOARD
# -----------------------------------------------------------------------------
st.markdown("### 📊 Session Threat Telemetry")

total = st.session_state.total_scanned
spam = st.session_state.spam_detected
ham = st.session_state.ham_detected
spam_ratio = (spam / total * 100.0) if total > 0 else 0.0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-lbl">Total Scanned</div>
        <div class="stat-val">{total}</div>
        <div style="font-size:0.75rem; color:#64748b;">Current Active Session</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card spam-stat">
        <div class="stat-lbl">Spam Detected</div>
        <div class="stat-val" style="color:#f87171;">{spam}</div>
        <div style="font-size:0.75rem; color:#64748b;">Flagged Messages</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card ham-stat">
        <div class="stat-lbl">Legitimate Messages</div>
        <div class="stat-val" style="color:#34d399;">{ham}</div>
        <div style="font-size:0.75rem; color:#64748b;">Verified Clean</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card ratio-stat">
        <div class="stat-lbl">Spam Ratio</div>
        <div class="stat-val" style="color:#c084fc;">{spam_ratio:.1f}%</div>
        <div style="font-size:0.75rem; color:#64748b;">Threat Incidence</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")


# -----------------------------------------------------------------------------
# 7. SMS SCANNER SECTION
# -----------------------------------------------------------------------------
st.markdown("### 🔍 SMS Threat Scanner")

# Predefined educational sample messages
SAMPLE_LEGIT = "Hey, are you still meeting at the library at 4 PM to work on the computer networks assignment?"
SAMPLE_PROMO = "URGENT! 50% discount on all premium electronics today only. Call 0800888999 or reply YES to claim your exclusive voucher!"
SAMPLE_PRIZE = "CONGRATULATIONS! Your mobile number was selected as a winner of £1,000 cash or Apple gift card! Call 09061701461 to claim. T&Cs apply."

# Callback functions for buttons to ensure clean Streamlit state synchronization
def load_sample_into_input(sample_text):
    st.session_state.sms_input = sample_text

def clear_input_and_results():
    st.session_state.sms_input = ""
    st.session_state.last_result = None

# Sample message buttons
st.markdown("<p style='font-size:0.88rem; color:#94a3b8; margin-bottom:8px;'><strong>Try a sample message:</strong></p>", unsafe_allow_html=True)

btn_c1, btn_c2, btn_c3 = st.columns([1, 1, 1])

with btn_c1:
    st.button("💬 Sample: Legitimate Message", use_container_width=True, on_click=load_sample_into_input, args=(SAMPLE_LEGIT,))

with btn_c2:
    st.button("🏷️ Sample: Promotional Spam", use_container_width=True, on_click=load_sample_into_input, args=(SAMPLE_PROMO,))

with btn_c3:
    st.button("🎁 Sample: Suspicious Prize Scam", use_container_width=True, on_click=load_sample_into_input, args=(SAMPLE_PRIZE,))

# SMS Input Text Area
message_input = st.text_area(
    label="Message Content",
    key="sms_input",
    height=140,
    placeholder="Paste your SMS message here...",
    label_visibility="collapsed"
)

# Live Character and Word Counter
char_count = len(message_input)
word_count = len(message_input.split()) if message_input.strip() else 0

counter_c1, counter_c2 = st.columns([1, 1])
with counter_c1:
    st.markdown(
        f"<span class='counter-tag'>Characters: <strong>{char_count}</strong> | Words: <strong>{word_count}</strong></span>",
        unsafe_allow_html=True
    )
with counter_c2:
    if total > 0:
        if st.button("🔄 Reset Session Stats", key="reset_stats_btn", help="Reset all message counters back to zero"):
            st.session_state.total_scanned = 0
            st.session_state.spam_detected = 0
            st.session_state.ham_detected = 0
            st.session_state.last_result = None
            st.rerun()

st.write("")

# Action Buttons: SCAN MESSAGE and CLEAR
act_c1, act_c2 = st.columns([3, 1])

with act_c1:
    scan_clicked = st.button("⚡ SCAN MESSAGE FOR THREATS", type="primary", use_container_width=True)

with act_c2:
    st.button("🧹 Clear Input", use_container_width=True, on_click=clear_input_and_results)

# Scan Execution Logic
if scan_clicked:
    cleaned_input = message_input.strip()
    if not cleaned_input:
        st.warning("⚠️ **Input Required:** Please enter or paste an SMS message before scanning, or select one of the sample messages above.")
    elif model is None:
        st.error("🚨 Cannot scan message: Machine learning model is unavailable.")
    else:
        # Perform inference with the trained pipeline
        try:
            prediction_label = model.predict([cleaned_input])[0]
            
            # Decision function score (distance to separating hyperplane)
            decision_score = None
            if hasattr(model, "decision_function"):
                decision_score = float(model.decision_function([cleaned_input])[0])
            
            # Update telemetry session state
            st.session_state.total_scanned += 1
            if prediction_label == "spam":
                st.session_state.spam_detected += 1
            else:
                st.session_state.ham_detected += 1
            
            # Record result
            st.session_state.last_result = {
                "message": cleaned_input,
                "label": prediction_label,
                "decision_score": decision_score,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.rerun()
        except Exception as ex:
            st.error(f"Inference Error: {ex}")


# -----------------------------------------------------------------------------
# 8. PREDICTION RESULTS DISPLAY
# -----------------------------------------------------------------------------
if st.session_state.last_result is not None:
    res = st.session_state.last_result
    label = res["label"]
    scanned_text = res["message"]
    timestamp = res["timestamp"]
    score = res["decision_score"]

    st.markdown("### 📋 Threat Inspection Report")

    if label == "spam":
        # SPAM WARNING CARD
        st.markdown(f"""
        <div class="result-card-spam">
            <div class="result-badge-spam">⚠️ ALERT: THREAT IDENTIFIED</div>
            <div class="result-title-spam">🚨 SPAM DETECTED</div>
            <p style="color:#fecaca; font-size:0.95rem; margin-bottom:12px;">
                The classification engine has evaluated this SMS and determined that it may be 
                <strong>unwanted, predatory, promotional spam, or a fraudulent phishing attempt (smishing)</strong>.
            </p>
            <div style="font-size:0.82rem; color:#94a3b8; margin-top:8px;">
                <strong>Analyzed Text:</strong>
            </div>
            <div class="msg-preview-box">{scanned_text}</div>
            <div style="font-size:0.84rem; color:#fca5a5; margin-top:10px;">
                <strong>🛡️ Recommended Safety Actions:</strong>
                <ul style="margin: 6px 0 0 18px; padding:0; line-height:1.5;">
                    <li><strong>Do not click</strong> any hyperlinks, shortened URLs, or download attachments.</li>
                    <li><strong>Never share</strong> personal identification numbers, passwords, OTPs, or financial information.</li>
                    <li><strong>Report and block</strong> the sender number on your mobile carrier or device settings.</li>
                </ul>
            </div>
            <div class="security-notice">
                <strong>Safety Disclaimer:</strong> Machine learning classifications represent statistical assessments 
                derived from message text features. This model never claims a message is guaranteed fraudulent; 
                always exercise personal discretion when handling unexpected communications.
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        # HAM SUCCESS CARD
        st.markdown(f"""
        <div class="result-card-ham">
            <div class="result-badge-ham">✅ VERIFIED: STANDARD PATTERNS</div>
            <div class="result-title-ham">🛡️ MESSAGE APPEARS LEGITIMATE</div>
            <p style="color:#a7f3d0; font-size:0.95rem; margin-bottom:12px;">
                The classification model did not identify characteristics typical of spam or smishing in this text. 
                Its vocabulary and structure align with standard interpersonal communication.
            </p>
            <div style="font-size:0.82rem; color:#94a3b8; margin-top:8px;">
                <strong>Analyzed Text:</strong>
            </div>
            <div class="msg-preview-box">{scanned_text}</div>
            <div style="font-size:0.84rem; color:#6ee7b7; margin-top:10px;">
                <strong>💡 Good Cybersecurity Practices:</strong>
                <ul style="margin: 6px 0 0 18px; padding:0; line-height:1.5;">
                    <li>Even legitimate-looking messages from unknown numbers should be verified through official channels.</li>
                    <li>Be cautious if an acquaintance asks for urgent financial transfers or gift cards unexpectedly.</li>
                </ul>
            </div>
            <div class="security-notice">
                <strong>Safety Disclaimer:</strong> The absence of detected spam signals does not guarantee absolute safety. 
                Sophisticated spear-phishing or novel impersonation tactics may mimic legitimate conversations. 
                Never claim any message is unconditionally safe without independent sender verification.
            </div>
        </div>
        """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 9. HOW SPAMSHIELD AI WORKS
# -----------------------------------------------------------------------------
st.write("")
with st.expander("ℹ️ How SpamShield AI Works", expanded=False):
    info_c1, info_c2, info_c3 = st.columns(3)
    with info_c1:
        st.markdown("""
        **1. Dataset**  
        Trained using 5,572 SMS messages labeled as spam or legitimate.
        """)

    with info_c2:
        st.markdown("""
        **2. Text Processing**  
        TF-IDF converts SMS text into numerical features.
        """)

    with info_c3:
        st.markdown("""
        **3. Classification**  
        LinearSVC classifies the message as spam or legitimate.
        """)

    st.markdown("---")
    st.markdown("#### 🎯 Evaluation Metrics on Test Split")
    st.markdown("""
    The following performance figures represent the empirical results evaluated on the holdout test partition 
    *(test split partition, not guaranteed real-world performance)*:
    """)

    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.markdown("""
        <div class="metric-chip">
            <div class="metric-chip-num">98.48%</div>
            <div class="metric-chip-name">Test Accuracy</div>
        </div>
        """, unsafe_allow_html=True)

    with m_col2:
        st.markdown("""
        <div class="metric-chip">
            <div class="metric-chip-num">98.53%</div>
            <div class="metric-chip-name">Spam Precision</div>
        </div>
        """, unsafe_allow_html=True)

    with m_col3:
        st.markdown("""
        <div class="metric-chip">
            <div class="metric-chip-num">89.93%</div>
            <div class="metric-chip-name">Spam Recall</div>
        </div>
        """, unsafe_allow_html=True)

    with m_col4:
        st.markdown("""
        <div class="metric-chip">
            <div class="metric-chip-num">94.04%</div>
            <div class="metric-chip-name">Spam F1-Score</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.caption("⚠️ **Note:** These metrics were achieved on the benchmark SMS Spam test split. Performance on real-world networks may vary depending on zero-day phrasing, obfuscation, and evolving smishing strategies.")



# -----------------------------------------------------------------------------
# 10. APPLICATION FOOTER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="footer-container">
    <div><strong>SpamShield AI — Smart Messages. Safer Digital Life.</strong></div>
    <div style="margin-top:6px;">Built with Python, Scikit-learn and Streamlit</div>
    <div style="margin-top:4px; font-size:0.75rem; color:#475569;">
        Academic Machine Learning Showcase &bull; Cybersecurity &bull; NLP Pipeline
    </div>
</div>
""", unsafe_allow_html=True)
