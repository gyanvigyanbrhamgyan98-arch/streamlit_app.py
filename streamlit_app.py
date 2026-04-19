import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

st.set_page_config(page_title="GVB 2026 Reboot", layout="wide")
st.title("☸️ ज्ञान विज्ञान ब्रह्मज्ञान: 2026 Reboot")

# --- अपनी असली API KEY यहाँ डालें ---
API_KEY = "AIzaSyDAAXpIJYYfsdryNciWHzDrnYg4KQGR8Jc" 

def get_content(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        article = soup.find(class_='post-body') or soup.find('article') or soup.find(class_='entry-content')
        if article:
            return article.get_text(separator="\n").strip()
        return soup.get_text()[:2000] # अगर कुछ न मिले तो पूरी साइट का टेक्स्ट
    except:
        return "वेबसाइट पढ़ने में दिक्कत आ रही है।"

def ai_generate(old_text):
    # सबसे ज्यादा चलने वाला स्टेबल URL
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    prompt = f"इस लेख को 2026 के लिए दोबारा लिखो: {old_text[:3000]}"
    try:
        r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=20)
        data = r.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except:
        return "AI अभी व्यस्त है, पर पुराना लेख नीचे मौजूद है।"

# फाइल लोड करना
for f in os.listdir():
    if f.endswith('.csv'):
        df = pd.read_csv(f)
        total = len(df)
        st.sidebar.success(f"कुल {total} लेख मिले")
        idx = st.number_input("लेख नंबर चुनें", 0, total-1, 0)
        
        # लिंक ढूंढना
        row = df.iloc[idx]
        target_url = next((val for val in row if str(val).startswith('http')), "Link Not Found")

        if st.button("🚀 प्रोसेस शुरू करें"):
            st.markdown(f"🔗 **लिंक:** [{target_url}]({target_url})")
            
            with st.spinner("काम चल रहा है..."):
                text = get_content(target_url)
                
                # यहाँ हमने 'री-राइट' का काम शुरू किया
                rebooted = ai_generate(text)
                
                st.markdown("---")
                st.subheader("✨ 2026 Reboot Version:")
                st.write(rebooted)
                
                # साथ में पुराना लेख भी दिखा देते हैं ताकि आप देख सकें कि क्या बदला
                with st.expander("पुराना लेख (Original Text) देखें"):
                    st.write(text)
        break
