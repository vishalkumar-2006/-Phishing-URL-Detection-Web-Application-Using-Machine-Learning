import streamlit as st
import pandas as pd
import pickle
import re
import time
import json
from datetime import datetime
from urllib.parse import urlparse

# ------------------------------
# Page Config
# ------------------------------
st.set_page_config(
    page_title="PhishGuard – URL Threat Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------
# Custom CSS
# ------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Sora:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
}

.stApp {
    background: #0a0e1a;
    color: #e2e8f0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0d1224 !important;
    border-right: 1px solid #1e2d4a;
}

/* Header */
.hero-header {
    background: linear-gradient(135deg, #0d1224 0%, #0a1628 50%, #0d1224 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 50%, rgba(0, 212, 255, 0.04) 0%, transparent 60%),
                radial-gradient(circle at 70% 50%, rgba(99, 102, 241, 0.04) 0%, transparent 60%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Space Mono', monospace;
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(90deg, #00d4ff, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 0.4rem 0;
}
.hero-subtitle {
    color: #64748b;
    font-size: 0.95rem;
    font-weight: 300;
    margin: 0;
}

/* Input area */
.input-card {
    background: #0d1224;
    border: 1px solid #1e2d4a;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}

/* Result cards */
.result-phishing {
    background: linear-gradient(135deg, #1a0a0a, #1f0d10);
    border: 1px solid #7f1d1d;
    border-left: 4px solid #ef4444;
    border-radius: 12px;
    padding: 1.5rem 2rem;
    margin: 1rem 0;
}
.result-safe {
    background: linear-gradient(135deg, #0a1a0f, #0d1f13);
    border: 1px solid #14532d;
    border-left: 4px solid #22c55e;
    border-radius: 12px;
    padding: 1.5rem 2rem;
    margin: 1rem 0;
}
.result-title {
    font-family: 'Space Mono', monospace;
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
}
.result-phishing .result-title { color: #ef4444; }
.result-safe .result-title { color: #22c55e; }
.result-subtitle { color: #94a3b8; font-size: 0.85rem; }

/* Confidence bar */
.conf-bar-wrap {
    background: #1e2d4a;
    border-radius: 999px;
    height: 8px;
    margin: 0.75rem 0 0.3rem;
    overflow: hidden;
}
.conf-bar-fill-danger {
    background: linear-gradient(90deg, #ef4444, #f97316);
    height: 100%;
    border-radius: 999px;
    transition: width 0.8s ease;
}
.conf-bar-fill-safe {
    background: linear-gradient(90deg, #22c55e, #10b981);
    height: 100%;
    border-radius: 999px;
    transition: width 0.8s ease;
}

/* Feature breakdown */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 0.75rem;
    margin-top: 1rem;
}
.feature-badge {
    background: #0d1628;
    border: 1px solid #1e2d4a;
    border-radius: 8px;
    padding: 0.6rem 0.8rem;
    font-size: 0.78rem;
}
.feature-badge-warn {
    border-color: #7c3aed44;
    background: #1a0d2e;
}
.feature-label {
    color: #64748b;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.feature-value {
    color: #e2e8f0;
    font-family: 'Space Mono', monospace;
    font-weight: 700;
    font-size: 0.9rem;
}
.feature-value-warn { color: #f59e0b; }

/* History table */
.hist-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.6rem 1rem;
    background: #0d1224;
    border: 1px solid #1e2d4a;
    border-radius: 8px;
    margin-bottom: 0.5rem;
    font-size: 0.82rem;
    gap: 1rem;
}
.tag-phish {
    background: #7f1d1d;
    color: #fca5a5;
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 0.7rem;
    font-family: 'Space Mono', monospace;
    white-space: nowrap;
}
.tag-safe {
    background: #14532d;
    color: #86efac;
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 0.7rem;
    font-family: 'Space Mono', monospace;
    white-space: nowrap;
}
.hist-url {
    color: #94a3b8;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    flex: 1;
    min-width: 0;
}
.hist-conf {
    color: #64748b;
    white-space: nowrap;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
}

/* Metric cards */
.metric-card {
    background: #0d1224;
    border: 1px solid #1e2d4a;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.metric-num {
    font-family: 'Space Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: #00d4ff;
    line-height: 1;
}
.metric-label {
    color: #64748b;
    font-size: 0.75rem;
    margin-top: 0.3rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Divider */
.section-divider {
    border: none;
    border-top: 1px solid #1e2d4a;
    margin: 1.5rem 0;
}

/* Override Streamlit defaults */
.stTextInput > div > div > input {
    background: #0d1628 !important;
    border: 1px solid #1e3a5f !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.9rem !important;
    padding: 0.75rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #00d4ff !important;
    box-shadow: 0 0 0 2px rgba(0,212,255,0.15) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #00d4ff22, #6366f122) !important;
    border: 1px solid #00d4ff66 !important;
    color: #00d4ff !important;
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    padding: 0.6rem 2rem !important;
    transition: all 0.2s ease !important;
    width: 100%;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #00d4ff44, #6366f144) !important;
    border-color: #00d4ff !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(0, 212, 255, 0.2) !important;
}
.stExpander {
    background: #0d1224 !important;
    border: 1px solid #1e2d4a !important;
    border-radius: 10px !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Space Mono', monospace !important;
    color: #00d4ff !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# Load Model
# ------------------------------
@st.cache_resource
def load_model():
    try:
        return pickle.load(open("phishing_model.pkl", "rb"))
    except FileNotFoundError:
        return None

model = load_model()

# ------------------------------
# Session State
# ------------------------------
if "history" not in st.session_state:
    st.session_state.history = []
if "total_scanned" not in st.session_state:
    st.session_state.total_scanned = 0
if "total_phishing" not in st.session_state:
    st.session_state.total_phishing = 0

# ------------------------------
# Feature Extraction
# ------------------------------
def extract_features(url):
    features = {}
    parsed = urlparse(url)
    hostname = parsed.hostname if parsed.hostname else ""

    features['length_url'] = len(url)
    features['length_hostname'] = len(hostname)
    features['ip'] = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0
    features['nb_dots'] = url.count('.')
    features['nb_hyphens'] = url.count('-')
    features['nb_at'] = url.count('@')
    features['nb_qm'] = url.count('?')
    features['nb_and'] = url.count('&')
    features['nb_eq'] = url.count('=')
    features['nb_underscore'] = url.count('_')
    features['nb_percent'] = url.count('%')
    features['nb_slash'] = url.count('/')
    features['nb_www'] = url.count('www')
    features['http_in_path'] = 1 if "http" in parsed.path else 0
    features['https_token'] = 1 if "https" in url else 0

    digits_url = sum(c.isdigit() for c in url)
    digits_host = sum(c.isdigit() for c in hostname)
    features['ratio_digits_url'] = digits_url / len(url) if len(url) > 0 else 0
    features['ratio_digits_host'] = digits_host / len(hostname) if len(hostname) > 0 else 0
    features['nb_subdomains'] = hostname.count('.') - 1 if hostname.count('.') > 0 else 0
    features['prefix_suffix'] = 1 if '-' in hostname else 0

    shortening_services = r"bit\.ly|goo\.gl|tinyurl|ow\.ly|t\.co|is\.gd|cli\.gs|yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|lnkd\.in|db\.tt|qr\.ae|adf\.ly|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|adcrun\.ch|ity\.im|q\.gs|viralurl\.com|is\.gd|vur\.me|bc\.vc|yu2\.it|twitthis\.com|u\.to|j\.mp|bee4\.biz|adflly\.com|pin\.gd|bitlly\.com|adf\.ly|go2l\.ink|x\.co|ow\.ly|smarturl\.it|yourls\.org|youtu\.be|ezurl"
    features['shortening_service'] = 1 if re.search(shortening_services, url) else 0
    features['path_extension'] = 1 if re.search(r'\.(exe|zip|rar|dll|scr|bat|msi|cmd|vbs|ps1)$', parsed.path) else 0

    return features


def get_risk_flags(features, url):
    """Return human-readable risk signals."""
    flags = []
    if features.get('ip'):
        flags.append(("🔴", "IP address used instead of domain"))
    if features.get('nb_at'):
        flags.append(("🔴", f"@ symbol present ({features['nb_at']}x)"))
    if features.get('http_in_path'):
        flags.append(("🔴", "HTTP embedded in URL path"))
    if features.get('shortening_service'):
        flags.append(("🟠", "URL shortening service detected"))
    if features.get('prefix_suffix'):
        flags.append(("🟠", "Hyphen in domain name"))
    if features.get('path_extension'):
        flags.append(("🔴", "Suspicious file extension in path"))
    if features.get('nb_subdomains', 0) > 2:
        flags.append(("🟠", f"Excessive subdomains ({features['nb_subdomains']})"))
    if features.get('length_url', 0) > 75:
        flags.append(("🟠", f"Long URL ({features['length_url']} chars)"))
    if features.get('nb_hyphens', 0) > 4:
        flags.append(("🟡", f"Many hyphens ({features['nb_hyphens']})"))
    if features.get('nb_percent', 0) > 0:
        flags.append(("🟡", f"URL-encoded characters ({features['nb_percent']})"))
    if not features.get('https_token'):
        flags.append(("🟡", "No HTTPS"))
    return flags


SELECTED_FEATURES = [
    'length_url', 'length_hostname', 'ip', 'nb_dots', 'nb_hyphens',
    'nb_at', 'nb_qm', 'nb_and', 'nb_eq', 'nb_underscore', 'nb_percent',
    'nb_slash', 'nb_www', 'http_in_path', 'https_token', 'ratio_digits_url',
    'ratio_digits_host', 'nb_subdomains', 'prefix_suffix', 'shortening_service',
    'path_extension'
]

# ------------------------------
# Sidebar
# ------------------------------
with st.sidebar:
    st.markdown("### 🛡️ PhishGuard")
    st.markdown("<p style='color:#64748b;font-size:0.8rem;margin-top:-0.5rem;'>URL Threat Detection</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Stats
    st.markdown("**Session Stats**")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-num'>{st.session_state.total_scanned}</div>
            <div class='metric-label'>Scanned</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class='metric-card'>
            <div class='metric-num' style='color:#ef4444'>{st.session_state.total_phishing}</div>
            <div class='metric-label'>Threats</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Threat Indicators**")
    indicators = [
        ("🔴", "Critical", "IP-based URLs, @ symbols, HTTP in path"),
        ("🟠", "High", "URL shorteners, hyphens in domain"),
        ("🟡", "Medium", "Long URLs, encoded chars, no HTTPS"),
    ]
    for icon, level, desc in indicators:
        st.markdown(f"<p style='font-size:0.78rem;margin:0.3rem 0;color:#94a3b8;'>{icon} <strong style='color:#e2e8f0'>{level}</strong> — {desc}</p>", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.session_state.total_scanned = 0
        st.session_state.total_phishing = 0
        st.rerun()

    st.markdown("<p style='color:#334155;font-size:0.7rem;margin-top:2rem;'>Model: Random Forest · 21 features</p>", unsafe_allow_html=True)

# ------------------------------
# Main Content
# ------------------------------
st.markdown("""
<div class='hero-header'>
    <div class='hero-title'>🛡️ PhishGuard</div>
    <p class='hero-subtitle'>Real-time phishing URL detection powered by machine learning · 21-feature analysis</p>
</div>
""", unsafe_allow_html=True)

if model is None:
    st.error("⚠️ **Model not found.** Please ensure `phishing_model.pkl` is in the working directory.")
    st.stop()

# ------------------------------
# Input Section
# ------------------------------
tab1, tab2 = st.tabs(["🔍 Single URL", "📋 Bulk Scan"])

with tab1:
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        url_input = st.text_input(
            "URL to analyze",
            placeholder="https://example.com or paste any suspicious link...",
            label_visibility="collapsed"
        )
    with col_btn:
        analyze_btn = st.button("SCAN →", use_container_width=True)

    if analyze_btn:
        if not url_input.strip():
            st.warning("Please enter a URL to scan.")
        else:
            with st.spinner("Analyzing URL..."):
                time.sleep(0.4)  # brief UX pause

                url = url_input.strip().lower()
                if not url.startswith(("http://", "https://")):
                    url = "https://" + url

                features = extract_features(url)
                features_df = pd.DataFrame([features])[SELECTED_FEATURES]
                prediction = model.predict(features_df)[0]
                probability = model.predict_proba(features_df)[0][1]
                confidence = probability if prediction == 1 else (1 - probability)
                risk_flags = get_risk_flags(features, url)

                # Update session
                st.session_state.total_scanned += 1
                if prediction == 1:
                    st.session_state.total_phishing += 1

                st.session_state.history.insert(0, {
                    "url": url_input.strip(),
                    "prediction": prediction,
                    "confidence": confidence,
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                })

            # Result Card
            if prediction == 1:
                bar_pct = int(probability * 100)
                st.markdown(f"""
                <div class='result-phishing'>
                    <div class='result-title'>⚠️ Phishing URL Detected</div>
                    <div class='result-subtitle'>{url_input.strip()}</div>
                    <div class='conf-bar-wrap'><div class='conf-bar-fill-danger' style='width:{bar_pct}%'></div></div>
                    <span style='color:#ef4444;font-family:Space Mono,monospace;font-size:0.85rem;font-weight:700;'>{confidence:.1%} threat confidence</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                bar_pct = int((1 - probability) * 100)
                st.markdown(f"""
                <div class='result-safe'>
                    <div class='result-title'>✅ Legitimate URL</div>
                    <div class='result-subtitle'>{url_input.strip()}</div>
                    <div class='conf-bar-wrap'><div class='conf-bar-fill-safe' style='width:{bar_pct}%'></div></div>
                    <span style='color:#22c55e;font-family:Space Mono,monospace;font-size:0.85rem;font-weight:700;'>{confidence:.1%} safe confidence</span>
                </div>
                """, unsafe_allow_html=True)

            # Risk Flags
            if risk_flags:
                with st.expander(f"🚩 Risk Signals ({len(risk_flags)} detected)", expanded=prediction == 1):
                    for icon, msg in risk_flags:
                        st.markdown(f"<p style='margin:0.3rem 0;font-size:0.85rem;color:#cbd5e1;'>{icon} {msg}</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color:#22c55e;font-size:0.82rem;margin-top:0.5rem;'>✓ No suspicious patterns detected</p>", unsafe_allow_html=True)

            # Feature Breakdown
            with st.expander("🔬 Feature Breakdown"):
                feature_display = {
                    'URL Length': (features['length_url'], features['length_url'] > 75),
                    'Hostname Length': (features['length_hostname'], features['length_hostname'] > 30),
                    'Dots': (features['nb_dots'], features['nb_dots'] > 5),
                    'Hyphens': (features['nb_hyphens'], features['nb_hyphens'] > 3),
                    'Subdomains': (features['nb_subdomains'], features['nb_subdomains'] > 2),
                    'Slashes': (features['nb_slash'], False),
                    '@ Symbols': (features['nb_at'], features['nb_at'] > 0),
                    'Query Params': (features['nb_qm'], False),
                    'Encoded Chars': (features['nb_percent'], features['nb_percent'] > 0),
                    'IP Address': ('Yes' if features['ip'] else 'No', features['ip'] == 1),
                    'HTTPS': ('Yes' if features['https_token'] else 'No', features['https_token'] == 0),
                    'Shortener': ('Yes' if features['shortening_service'] else 'No', features['shortening_service'] == 1),
                    'Digit Ratio': (f"{features['ratio_digits_url']:.2f}", features['ratio_digits_url'] > 0.3),
                    'Suspicious Ext': ('Yes' if features['path_extension'] else 'No', features['path_extension'] == 1),
                }

                badge_html = "<div class='feature-grid'>"
                for label, (val, warn) in feature_display.items():
                    card_cls = "feature-badge feature-badge-warn" if warn else "feature-badge"
                    val_cls = "feature-value-warn" if warn else "feature-value"
                    badge_html += f"""
                    <div class='{card_cls}'>
                        <div class='feature-label'>{label}</div>
                        <div class='{val_cls}'>{val}</div>
                    </div>"""
                badge_html += "</div>"
                st.markdown(badge_html, unsafe_allow_html=True)

with tab2:
    st.markdown("<p style='color:#94a3b8;font-size:0.85rem;'>Enter one URL per line to scan multiple URLs at once.</p>", unsafe_allow_html=True)
    bulk_input = st.text_area(
        "URLs (one per line)",
        placeholder="https://google.com\nhttps://suspicious-site.xyz/login\nhttps://paypal-verification.net",
        height=150,
        label_visibility="collapsed"
    )
    bulk_btn = st.button("SCAN ALL →", key="bulk_btn", use_container_width=False)

    if bulk_btn and bulk_input.strip():
        urls = [u.strip() for u in bulk_input.strip().splitlines() if u.strip()]
        if urls:
            results = []
            progress = st.progress(0)
            for i, raw_url in enumerate(urls):
                url = raw_url.lower()
                if not url.startswith(("http://", "https://")):
                    url = "https://" + url
                feats = extract_features(url)
                df = pd.DataFrame([feats])[SELECTED_FEATURES]
                pred = model.predict(df)[0]
                prob = model.predict_proba(df)[0][1]
                conf = prob if pred == 1 else (1 - prob)
                results.append({
                    "URL": raw_url,
                    "Result": "⚠️ Phishing" if pred == 1 else "✅ Legitimate",
                    "Confidence": f"{conf:.1%}",
                    "Threat Score": f"{prob:.3f}"
                })
                st.session_state.total_scanned += 1
                if pred == 1:
                    st.session_state.total_phishing += 1
                progress.progress((i + 1) / len(urls))

            progress.empty()
            results_df = pd.DataFrame(results)
            st.dataframe(
                results_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "URL": st.column_config.TextColumn("URL", width="large"),
                    "Result": st.column_config.TextColumn("Result", width="medium"),
                    "Confidence": st.column_config.TextColumn("Confidence", width="small"),
                    "Threat Score": st.column_config.TextColumn("Threat Score", width="small"),
                }
            )

            phish_count = sum(1 for r in results if "Phishing" in r["Result"])
            safe_count = len(results) - phish_count
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Total Scanned", len(results))
            with c2:
                st.metric("Threats Found", phish_count)
            with c3:
                st.metric("Safe URLs", safe_count)

# ------------------------------
# Scan History
# ------------------------------
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown("### 🕑 Scan History")

if st.session_state.history:
    for item in st.session_state.history[:10]:
        tag = "<span class='tag-phish'>THREAT</span>" if item['prediction'] == 1 else "<span class='tag-safe'>SAFE</span>"
        st.markdown(f"""
        <div class='hist-row'>
            {tag}
            <span class='hist-url'>{item['url']}</span>
            <span class='hist-conf'>{item['confidence']:.0%} · {item['timestamp']}</span>
        </div>
        """, unsafe_allow_html=True)
    if len(st.session_state.history) > 10:
        st.markdown(f"<p style='color:#475569;font-size:0.75rem;text-align:center;'>Showing 10 of {len(st.session_state.history)} scans</p>", unsafe_allow_html=True)
else:
    st.markdown("<p style='color:#334155;font-size:0.85rem;'>No scans yet — enter a URL above to get started.</p>", unsafe_allow_html=True)