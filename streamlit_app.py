import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

# पेज सेटअप
st.set_page_config(page_title="GVB 2026 Reboot", layout="wide")
st.title("☸️ ज्ञान विज्ञान ब्रह्मज्ञान: 2026 Reboot")

# --- अपनी API KEY यहाँ डालें ---
API_KEY = "AIzaSyDAAXpIJYYfsdryNciWHzDrnYg4KQGR8Jc" 

def get_content(url):
    try:
        # ब्राउज़र जैसा व्यवहार करने के लिए Headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # ब्लॉगर के कंटेंट एरिया को ढूँढना
        content_div = soup.find(class_='post-body') or \
                      soup.find('article') or \
                      soup.find(class_='entry-content') or \
                      soup.find(id='post-body')
        
        if content_div:
            # फालतू की चीजें हटाना
            for tag in content_div(['script', 'style', 'iframe', 'ins']):
                tag.decompose()
            return content_div.get_text(separator="\n").strip()
        
        # अगर कुछ न मिले तो पैराग्राफ्स का टेक्स्ट उठाना
        paragraphs = soup.find_all('p')
        if paragraphs:
            return "\n".join([p.get_text() for p in paragraphs])
            
        return None
    except Exception as e:
        return f"Error: {str(e)}"

def ai_generate(old_text):
    if not old_content or len(old_content) < 50:
        return "वेबसाइट से लेख पढ़ा नहीं जा सका। कृपया लिंक चेक करें।"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    
    # आपका विशेष प्रॉम्प्ट
    prompt = f"""
    तुम 'ज्ञान विज्ञान ब्रह्मज्ञान' के मुख्य संपादक हो। 
    नीचे दिए गए पुराने लेख को 2026 के आधुनिक संदर्भ में दोबारा (Rewrite) लिखो।
    निर्देश:
    1. भाषा सरल, प्रभावशाली और वैज्ञानिक-आध्यात्मिक हो।
    2. 'Trilokinath' स्टाइल में एक AI इमेज जेनरेट करने का प्रॉम्प्ट दो।
    3. सोशल मीडिया (Instagram/Telegram) के लिए एक छोटा कैप्शन और हैशटैग दो।
    
    पुराना लेख:
    {old_text[:4000]}
    """
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        
        # Error check for Gemini API
        if 'candidates' in data and len(data['candidates']) > 0:
            return data['candidates'][0]['content']['parts'][0]['text']
        elif 'error' in data:
            return f"API Error: {data['error']['message']}"
        else:
            return "AI ने जवाब प्रोसेस नहीं किया। कृपया दोबारा कोशिश करें।"
    except Exception as e:
        return f"Failed to connect: {str(e)}"

# --- डेटा लोड करना ---
file_found = False
for f in os.listdir():
    if f.endswith('.csv'):
        df = pd.read_csv(f)
        file_found = f
        break

if file_found:
    total = len(df)
    st.sidebar.success(f"कुल {total} लेख लोड हुए")
    
    # पोस्ट सिलेक्शन
    post_idx = st.number_input(f"लेख नंबर चुनें (0 से {total-1})", 0, total-1, 0)
    
    # लिंक निकालने का लॉजिक (Auto-Column Detect)
    try:
        row = df.iloc[post_idx]
        target_url = next((val for val in row if str(val).startswith('http')), None)
    except:
        target_url = None

    if st.button("🚀 2026 Reboot शुरू करें"):
        if target_url:
            st.info(f"🔗 प्रोसेसिंग लिंक: {target_url}")
            with st.spinner("पुरानी फाइलों से ज्ञान निकाला जा रहा है..."):
                old_content = get_content(target_url)
                
                if old_content and not old_content.startswith("Error"):
                    rebooted_result = ai_generate(old_content)
                    st.markdown("---")
                    st.subheader("✨ आपका नया लेख (2026 अवतार)")
                    st.write(rebooted_result)
                else:
                    st.error(f"कंटेंट नहीं मिला: {old_content}")
        else:
            st.error("इस रो (Row) में कोई लिंक नहीं मिला।")
else:
    st.warning("⚠️ GitHub पर 'Bolginventory.csv' फाइल नहीं मिली!")
