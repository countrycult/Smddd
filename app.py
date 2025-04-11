
import streamlit as st
import pandas as pd
import re
from textblob import TextBlob

@st.cache_data
def load_icd_data():
    return pd.read_csv("icd_codes.csv")

icd_data = load_icd_data()
medical_terms = icd_data['Term'].str.lower().tolist()

st.title("Medical Term Highlighter + Spelling Checker")
user_input = st.text_area("Enter medical text", height=200)

corrected_text = str(TextBlob(user_input).correct())

if user_input and corrected_text.lower() != user_input.lower():
    st.warning(f"Did you mean: `{corrected_text}`?")

def highlight_terms(text, terms):
    for term in sorted(terms, key=len, reverse=True):
        pattern = r'\\b' + re.escape(term) + r'\\b'
        text = re.sub(pattern, f"<mark>{term}</mark>", text, flags=re.IGNORECASE)
    return text

if user_input:
    highlighted = highlight_terms(user_input, medical_terms)
    st.markdown("### Highlighted Text", unsafe_allow_html=True)
    st.markdown(highlighted, unsafe_allow_html=True)

    matched = [term for term in medical_terms if re.search(r'\\b' + re.escape(term) + r'\\b', user_input, re.IGNORECASE)]
    if matched:
        st.success("Matched Terms:")
        st.write(matched)
    else:
        st.info("No medical terms matched.")
