import streamlit as st
import pandas as pd
import joblib
from urllib.parse import urlparse
import ipaddress
import re

# ---- Load model + scaler ----
model = joblib.load("phishing_model.pkl")
scaler = joblib.load("scaler.pkl")

# ---- Same feature extraction as training ----
SUSPICIOUS_WORDS = re.compile(
    r"(login|signin|verify|verification|secure|account|update|"
    r"confirm|password|bank|payment|wallet|billing|authenticate)",
    re.IGNORECASE
)

def extract_features(url):
    url = str(url)
    try:
        parsed = urlparse(
            url if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", url)
            else "//" + url
        )
    except:
        parsed = urlparse("//")

    hostname = parsed.hostname or ""
    path = parsed.path or ""
    query = parsed.query or ""

    try:
        ipaddress.ip_address(hostname)
        has_ip = 1
    except:
        has_ip = 0

    host_parts = [part for part in hostname.split(".") if part]
    subdomain_count = 0 if has_ip else max(0, len(host_parts) - 2)

    digit_count = sum(c.isdigit() for c in url)
    special_char_count = sum(not c.isalnum() for c in url)
    digit_ratio = digit_count / len(url) if len(url) > 0 else 0

    return {
        "url_length": len(url),
        "hostname_length": len(hostname),
        "path_length": len(path),
        "query_length": len(query),
        "digit_count": digit_count,
        "digit_ratio": digit_ratio,
        "special_char_count": special_char_count,
        "dot_count": url.count("."),
        "slash_count": url.count("/"),
        "hyphen_count": url.count("-"),
        "at_count": url.count("@"),
        "question_count": url.count("?"),
        "ampersand_count": url.count("&"),
        "equals_count": url.count("="),
        "percent_count": url.count("%"),
        "underscore_count": url.count("_"),
        "subdomain_count": subdomain_count,
        "has_https": int(parsed.scheme.lower() == "https"),
        "has_ip": has_ip,
        "has_www": int(hostname.lower().startswith("www.")),
        "suspicious_keyword": int(bool(SUSPICIOUS_WORDS.search(url))),
    }

# ---- Streamlit UI ----
st.set_page_config(page_title="Phishing URL Detector", page_icon="🔐")

st.title("🔐 Phishing URL Detector")
st.write("Enter a URL below to check whether it looks benign or malicious.")

url_input = st.text_input("URL", placeholder="https://example.com/login")

if st.button("Analyze"):
    if not url_input.strip():
        st.warning("Please enter a URL.")
    else:
        feats = extract_features(url_input)
        feats_df = pd.DataFrame([feats])

        # scale (Logistic Regression needs scaled input)
        feats_scaled = scaler.transform(feats_df)

        pred = model.predict(feats_scaled)[0]
        proba = model.predict_proba(feats_scaled)[0][1]

        if pred == 1:
            st.error(f"🔴 MALICIOUS  —  risk probability: {proba*100:.2f}%")
        else:
            st.success(f"🟢 BENIGN  —  risk probability: {proba*100:.2f}%")

        with st.expander("See extracted features"):
            st.dataframe(feats_df.T.rename(columns={0: "value"}))