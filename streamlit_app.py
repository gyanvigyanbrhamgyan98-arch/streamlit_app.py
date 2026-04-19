# streamlit_app.py
​An AI-powered content automation tool for 'Gyan Vigyan Brahmgyan' (GVB). It reboots 10 years of archival blog posts into 2026-ready articles, social media kits, and AI image prompts using Gemini API and Streamlit.
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

# पेज की बनावट (UI)
st.set_page_config(page_title="GVB Asset Manager", page_icon="☸️")

st.title("☸️ ज्ञान विज्ञान ब्रह्मज्ञान")
st.subheader("2026 Reboot & Marketing Engine")

# Gemini API Key सुरक्षित रूप से लेना
# (Streamlit के "Secrets" में इसे डालना होगा)
API_KEY = st.secrets.get("GEMINI_API_KEY")

def get_content(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        body = soup.find(class_='post-body')
        return body.get_text() if body else None
    except:
        return None

def ai_generate(old_text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    prompt = f"तुम 'ज्ञान विज्ञान ब्रह्मज्ञान' के मुख्य संपादक हो। इस पुराने लेख को 2026 के लिए अपडेट करो, फेसबुक/इंस्टा कैप्शन लिखो और इमेज प्रॉम्प्ट दो: {old_text[:3500]}"
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    r = requests.post(url, json=payload)
    return r.json()['candidates'][0]['content']['parts'][0]['text']

# डेटा लोड करना
if os.path.exists('inventory_gyanvigyan.csv'):
    df = pd.read_csv('inventory_gyanvigyan.csv')
    
    # इनपुट बॉक्स
    post_idx = st.number_input("पोस्ट नंबर डालें (0 से " + str(len(df)-1) + ")", min_value=0, max_value=len(df)-1, step=1)
    
    if st.button("Generate Reboot Kit"):
        target_url = df.iloc[post_idx]['Post_Link']
        st.info(f"पढ़ा जा रहा है: {target_url}")
        
        content = get_content(target_url)
        
        if content:
            with st.spinner("AI जादू कर रहा है..."):
                result = ai_generate(content)
                st.success("तैयार है!")
                st.markdown("---")
                st.markdown(result)
        else:
            st.error("पोस्ट का कंटेंट नहीं मिल सका।")
else:
    st.error("inventory_gyanvigyan.csv फाइल नहीं मिली। कृपया इसे अपलोड करें।")
