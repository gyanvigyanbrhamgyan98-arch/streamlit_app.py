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
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 1. सबसे पहले मुख्य लेख ढूँढें
        article = soup.find(class_='post-body') or soup.find('article') or soup.find(class_='entry-content')
        
        if article:
            return article.get_text(separator="\n").strip()
        
        # 2. अगर मुख्य लेख न मिले, तो सारे पैराग्राफ्स का टेक्स्ट उठा लें
        p_text = "\n".join([p.get_text() for p in soup.find_all('p')])
        if len(p_text) > 100:
            return p_text
            
        return None
    except Exception as e:
        return None

def ai_generate(old_text):
    # मॉडल का सबसे स्टेबल URL
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    prompt = f"""
    तुम 'ज्ञान विज्ञान ब्रह्मज्ञान' के संपादक हो। 
    नीचे दिए गए पुराने लेख को 2026 के हिसाब से पूरी तरह दोबारा (Rewrite) लिखो।
    इसे वैज्ञानिक और आध्यात्मिक रूप से गहरा बनाओ। 
    अंत में 'Trilokinath' स्टाइल इमेज प्रॉम्प्ट और सोशल मीडिया कैप्शन भी दो।
    
    लेख: {old_text[:3500]}
    """
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        if 'candidates' in data:
            return data['candidates'][0]['content']['parts'][0]['text']
        return "AI जवाब नहीं दे पाया। कृपया दोबारा बटन दबाएँ।"
    except:
        return "AI सर्वर से संपर्क नहीं हो सका।"

# --- डेटा लोड करना ---
for f in os.listdir():
    if f.endswith('.csv'):
        df = pd.read_csv(f)
        total = len(df)
        st.sidebar.success(f"कुल {total} लेख मिले")
        
        idx = st.number_input("लेख नंबर चुनें", 0, total-1, 0)
        
        # लिंक ढूंढना
        row = df.iloc[idx]
        target_url = next((val for val in row if str(val).startswith('http')), None)

        if st.button("🚀 2026 Reboot शुरू करें"):
            if target_url:
                st.info(f"🔗 लिंक मिला: {target_url}")
                with st.spinner("पुराना लेख पढ़कर उसे दोबारा लिखा जा रहा है..."):
                    content = get_content(target_url)
                    
                    if content:
                        # अब यहाँ असली री-राइट होगा
                        result = ai_generate(content)
                        st.markdown("---")
                        st.subheader("✨ नया लेख (Rebooted Version):")
                        st.write(result)
                    else:
                        st.error("वेबसाइट से लेख नहीं मिल सका। शायद लिंक गलत है।")
            else:
                st.error("इस नंबर पर कोई लिंक नहीं मिला।")
        break
