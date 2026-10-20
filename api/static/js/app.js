/* =============================================================================
   SpamShield AI — Client-Side Application Logic
   Features: Live character counter, sample payloads, AJAX inference, session telemetry
   ============================================================================= */

// Educational sample payload messages
const SAMPLES = {
    legit: "Hey, are you still meeting at the library at 4 PM to work on the computer networks assignment?",
    promo: "URGENT! 50% discount on all premium electronics today only. Call 0800888999 or reply YES to claim your exclusive voucher!",
    prize: "CONGRATULATIONS! Your mobile number was selected as a winner of £1,000 cash or Apple gift card! Call 09061701461 to claim. T&Cs apply."
};

// Session Threat Telemetry State (stored in sessionStorage so it persists during tab session)
const telemetry = {
    total: parseInt(sessionStorage.getItem('spamshield_total') || '0', 10),
    spam: parseInt(sessionStorage.getItem('spamshield_spam') || '0', 10),
    ham: parseInt(sessionStorage.getItem('spamshield_ham') || '0', 10),

    save() {
        sessionStorage.setItem('spamshield_total', this.total);
        sessionStorage.setItem('spamshield_spam', this.spam);
        sessionStorage.setItem('spamshield_ham', this.ham);
        this.render();
    },

    reset() {
        this.total = 0;
        this.spam = 0;
        this.ham = 0;
        this.save();
    },

    render() {
        document.getElementById('statTotal').textContent = this.total;
        document.getElementById('statSpam').textContent = this.spam;
        document.getElementById('statHam').textContent = this.ham;
        const ratio = this.total > 0 ? ((this.spam / this.total) * 100).toFixed(1) : "0.0";
        document.getElementById('statRatio').textContent = ratio + "%";
    }
};

// DOM Elements
const smsInput = document.getElementById('smsInput');
const charCountEl = document.getElementById('charCount');
const wordCountEl = document.getElementById('wordCount');
const scanBtn = document.getElementById('scanBtn');
const clearBtn = document.getElementById('clearBtn');
const resetStatsBtn = document.getElementById('resetStatsBtn');
const alertBox = document.getElementById('alertBox');
const resultsContainer = document.getElementById('resultsContainer');
const spamResultCard = document.getElementById('spamResultCard');
const hamResultCard = document.getElementById('hamResultCard');
const spamAnalyzedText = document.getElementById('spamAnalyzedText');
const hamAnalyzedText = document.getElementById('hamAnalyzedText');

// Update Character and Word Counter
function updateCounters() {
    const text = smsInput.value;
    charCountEl.textContent = text.length;
    const words = text.trim().length > 0 ? text.trim().split(/\s+/).length : 0;
    wordCountEl.textContent = words;
}

// Show Warning Alert
function showAlert(message) {
    alertBox.textContent = "⚠️ " + message;
    alertBox.style.display = "flex";
    setTimeout(() => {
        alertBox.style.display = "none";
    }, 4500);
}

// Hide Warning Alert
function hideAlert() {
    alertBox.style.display = "none";
}

// Load Sample Payload
function loadSample(key) {
    if (SAMPLES[key]) {
        smsInput.value = SAMPLES[key];
        updateCounters();
        hideAlert();
        smsInput.focus();
    }
}

// Clear Input and Results
function clearInput() {
    smsInput.value = "";
    updateCounters();
    hideAlert();
    resultsContainer.style.display = "none";
    spamResultCard.style.display = "none";
    hamResultCard.style.display = "none";
    smsInput.focus();
}

// Perform Prediction Scan
async function scanMessage() {
    hideAlert();
    const message = smsInput.value.trim();

    if (!message) {
        showAlert("Input Required: Please enter or paste an SMS message before scanning, or select one of the sample messages above.");
        return;
    }

    // Set button loading state
    const originalBtnText = scanBtn.innerHTML;
    scanBtn.innerHTML = "<span>⏳ SCANNING MESSAGE...</span>";
    scanBtn.disabled = true;

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        if (!response.ok || data.error) {
            throw new Error(data.error || "Server inference error");
        }

        // Update telemetry statistics
        telemetry.total += 1;
        if (data.prediction === "spam") {
            telemetry.spam += 1;
        } else {
            telemetry.ham += 1;
        }
        telemetry.save();

        // Render appropriate prediction card
        resultsContainer.style.display = "block";
        if (data.prediction === "spam") {
            spamAnalyzedText.textContent = message;
            spamResultCard.style.display = "block";
            hamResultCard.style.display = "none";
        } else {
            hamAnalyzedText.textContent = message;
            hamResultCard.style.display = "block";
            spamResultCard.style.display = "none";
        }

        // Smooth scroll to results
        resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    } catch (err) {
        showAlert("Scan Error: " + err.message);
    } finally {
        scanBtn.innerHTML = originalBtnText;
        scanBtn.disabled = false;
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Initialize telemetry display
    telemetry.render();

    // Input listener for counters
    smsInput.addEventListener('input', updateCounters);

    // Sample buttons
    document.getElementById('sampleLegitBtn').addEventListener('click', () => loadSample('legit'));
    document.getElementById('samplePromoBtn').addEventListener('click', () => loadSample('promo'));
    document.getElementById('samplePrizeBtn').addEventListener('click', () => loadSample('prize'));

    // Scan & Clear buttons
    scanBtn.addEventListener('click', scanMessage);
    clearBtn.addEventListener('click', clearInput);
    resetStatsBtn.addEventListener('click', () => telemetry.reset());

    // Keyboard shortcut: Ctrl + Enter to scan
    smsInput.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            scanMessage();
        }
    });
});
