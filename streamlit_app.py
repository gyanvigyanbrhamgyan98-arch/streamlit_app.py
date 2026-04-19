import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

st.set_page_config(page_title="GVB 2026 Reboot", layout="wide")
st.title("☸️ ज्ञान विज्ञान ब्रह्मज्ञान: 2026 Reboot")

# --- अपनी API KEY यहाँ डालें ---
API_KEY = "AIzaSyDAAXpIJYYfsdryNciWHzDrnYg4KQGR8Jc" 

def get_content(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        article = soup.find(class_='post-body') or soup.find('article') or soup.find(class_='entry-content')
        if article:
            return article.get_text(separator="\n").strip()
        p_text = "\n".join([p.get_text() for p in soup.find_all('p')])
        return p_text if len(p_text) > 100 else None
    except:
        return None

# --- यह है वो हिस्सा जो आपको अपडेट करना था ---
def ai_generate(old_text):
    if not old_text or len(old_text) < 50:
        return "पुराना लेख पढ़ने में समस्या आई।"

    # v1 (Stable) URL
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    prompt = f"""
    तुम 'ज्ञान विज्ञान ब्रह्मज्ञान' के संपादक हो। 
    इस पुराने लेख को 2026 के लिए पूरी तरह 'री-राइट' (Rewrite) करो। 
    इसे आध्यात्मिक, वैज्ञानिक और प्रभावशाली बनाओ। 
    अंत में एक इमेज प्रॉम्प्ट और सोशल मीडिया कैप्शन दो।
    लेख: {old_text[:3500]}
    """
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=payload, timeout=25)
        data = response.json()
        
        if 'candidates' in data and len(data['candidates']) > 0:
            return data['candidates'][0]['content']['parts'][0]['text']
        elif 'error' in data:
            return f"API एरर: {data['error']['message']}"
        else:
            return f"जवाब नहीं मिला। डेटा चेक करें: {str(data)[:100]}"
    except Exception as e:
        return f"कनेक्शन एरर: {str(e)}"

# --- डेटा लोडिंग और बटन ---
for f in os.listdir():
    if f.endswith('.csv'):
        df = pd.read_csv(f)
        total = len(df)
        st.sidebar.success(f"कुल {total} लेख मिले")
        idx = st.number_input("लेख नंबर चुनें", 0, total-1, 0)
        
        row = df.iloc[idx]
        target_url = next((val for val in row if str(val).startswith('http')), None)

        if st.button("🚀 2026 Reboot शुरू करें"):
            if target_url:
                with st.spinner("पुराना लेख पढ़कर री-राइट किया जा रहा है..."):
                    content = get_content(target_url)
                    if content:
                        result = ai_generate(content)
                        st.markdown("---")
                        st.subheader("✨ नया लेख (Rebooted Version):")
                        st.write(result)
                    else:
                        st.error("वेबसाइट से लेख नहीं मिल सका।")
            else:
                st.error("लिंक नहीं मिला।")
        break
