import streamlit as st
import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

# सीधे यहाँ अपनी असली चाबी पेस्ट करें
API_KEY = "AIzaSyDAAXpIJYYfsdryNciWHzDrnYg4KQGR8Jc"

st.set_page_config(page_title="GVB 2026 Reboot", layout="wide")
st.title("☸️ ज्ञान विज्ञान ब्रह्मज्ञान")


# 2. LOAD DATA (Auto-Detect File)
file_found = False
for f in os.listdir():
    if f.endswith('.csv'):
        df = pd.read_csv(f)
        file_found = f
        break

if file_found:
    total = len(df)
    st.sidebar.success(f"✅ फाइल मिली: {file_found}")
    st.sidebar.info(f"कुल पोस्ट: {total}")
    
    # पोस्ट चुनने का स्लाइडर
    idx = st.number_input("पोस्ट नंबर (0 से {0})".format(total-1), 0, total-1, 0)
    
    # लिंक ढूँढने की कोशिश (चाहे नाम कुछ भी हो)
    try:
        target_url = df.iloc[idx, 0] # पहले कॉलम को ही लिंक मान लो
        if not str(target_url).startswith('http'):
            target_url = df.iloc[idx, 1] # अगर पहले में नहीं तो दूसरे में देखो
    except:
        st.error("फाइल के अंदर लिंक नहीं मिल रहा है।")
        st.stop()

    if st.button("🚀 रीबूट शुरू करें"):
        st.write(f"🔗 **प्रोसेसिंग लिंक:** {target_url}")
        
        with st.spinner("AI आपकी पुरानी यादों को पढ़ रहा है..."):
            try:
                # स्क्रैपिंग
                res = requests.get(target_url, timeout=10)
                soup = BeautifulSoup(res.text, 'html.parser')
                text = soup.get_text()[:4000] # शुरुआती 4000 अक्षर

                # AI Generation
                gen_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
                prompt = f"तुम 'ज्ञान विज्ञान ब्रह्मज्ञान' के संपादक हो। इस लेख को 2026 के लिए अपडेट करो, सोशल मीडिया कैप्शन और इमेज प्रॉम्प्ट लिखो: {text}"
                
                r = requests.post(gen_url, json={"contents": [{"parts": [{"text": prompt}]}]})
                result = r.json()['candidates'][0]['content']['parts'][0]['text']
                
                st.success("✨ काम पूरा हुआ!")
                st.markdown("---")
                st.write(result)
            except Exception as e:
                st.error(f"कुछ गड़बड़ हुई: {e}")
else:
    st.warning("⚠️ GitHub पर कोई भी .csv फाइल नहीं मिली। कृपया Bolginventory.csv अपलोड करें।")
