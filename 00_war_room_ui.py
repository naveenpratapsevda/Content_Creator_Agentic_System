import streamlit as st
import time
from datetime import datetime
import openai
import os
import duckduckgo_search
# Try importing Search Tool (Agent's Eyes)
try:
    from duckduckgo_search import DDGS
    SEARCH_AVAILABLE = True
except ImportError:
    SEARCH_AVAILABLE = False

# ═══════════════════════════════════════════════════════════════════════════════
# SOVEREIGN CINEMA ENGINE - WAR ROOM UI v5.0
# Pitch Black + Cyan/Magenta Cyberpunk Aesthetic | Industrial Grade
# ═══════════════════════════════════════════════════════════════════════════════

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Sovereign Cinema Engine",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════════
# 2. CSS INJECTION - THE "HEAVY" INDUSTRIAL THEME
# ═══════════════════════════════════════════════════════════════════════════════

def inject_custom_css():
    st.markdown("""
    <style>
    /* ═══ FONT IMPORT & BASE ═══ */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;800&display=swap');
    
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    /* Main Background - Pitch Black */
    .stApp {
        background-color: #000000;
        color: #E0E0E0;
        font-family: 'JetBrains Mono', monospace;
    }

    /* ═══ SIDEBAR FIXES (CRITICAL) ═══ */
    section[data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 1px solid #222 !important;
        box-shadow: 5px 0 30px rgba(0,0,0,0.8);
    }
    
    /* The Collapsed Button (Arrow) - Make it Visible & Cyan */
    button[kind="header"] {
        color: #00E5FF !important; 
        background: transparent !important;
    }
    [data-testid="collapsedControl"] {
        color: #00E5FF !important;
        display: block !important;
        z-index: 1000000 !important; /* Force it on top */
        background-color: #000 !important;
        border: 1px solid #333;
        border-radius: 5px;
        margin-top: 10px;
        margin-left: 10px;
    }
    
    /* Sidebar Text */
    section[data-testid="stSidebar"] h3 {
        color: #00E5FF !important; /* Cyan Header */
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-size: 0.8rem;
        margin-top: 20px;
    }
    section[data-testid="stSidebar"] p {
        color: #888;
        font-size: 0.9rem;
    }

    /* ═══ INPUT FIELDS - CYAN GLOW ═══ */
    .stTextInput > div > div > input {
        background: #000000 !important;
        color: #00E5FF !important;
        border: 2px solid #333 !important;
        border-radius: 0px !important; /* Square Industrial Look */
        padding: 1.5rem 1rem !important;
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.1rem;
    }
    .stTextInput > div > div > input:focus {
        border-color: #00E5FF !important;
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.3) !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #444 !important;
    }

    /* ═══ BUTTONS - MAGENTA POWER ═══ */
    .stButton > button {
        background: #000 !important;
        color: #FF007F !important; /* Hot Pink */
        border: 2px solid #FF007F !important;
        border-radius: 0px !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        padding: 1rem 2rem !important;
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        background: #FF007F !important;
        color: #000 !important;
        box-shadow: 0 0 30px rgba(255, 0, 127, 0.6) !important;
        transform: translateY(-2px);
    }

    /* Form Submit Button specifically */
    .stForm button[kind="primaryFormSubmit"] {
        width: 100%;
        background: linear-gradient(45deg, #000 0%, #111 100%) !important;
        border: 2px solid #00E5FF !important;
        color: #00E5FF !important;
    }
    .stForm button[kind="primaryFormSubmit"]:hover {
        background: #00E5FF !important;
        color: #000 !important;
        box-shadow: 0 0 40px rgba(0, 229, 255, 0.5) !important;
    }

    /* ═══ CARDS & CONTAINERS ═══ */
    .neon-card {
        background: #080808;
        border: 1px solid #222;
        border-left: 4px solid #00E5FF; /* Cyan Accent */
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    }

    .report-card {
        background: #050505;
        border: 1px solid #222;
        border-top: 4px solid #FF007F; /* Pink Top */
        padding: 2.5rem;
        margin-top: 2rem;
        position: relative;
    }
    
    .report-card::before {
        content: "CONFIDENTIAL";
        position: absolute;
        top: -10px;
        right: 20px;
        background: #000;
        color: #FF007F;
        padding: 0 10px;
        font-size: 0.8rem;
        letter-spacing: 2px;
        font-weight: bold;
    }

    /* ═══ TYPOGRAPHY ═══ */
    h1 {
        font-size: 3.5rem;
        font-weight: 900;
        color: #FFF;
        letter-spacing: -2px;
        margin-bottom: 0;
    }
    .subtitle {
        color: #666;
        font-size: 0.9rem;
        letter-spacing: 4px;
        margin-bottom: 3rem;
        text-transform: uppercase;
    }
    h2, h3 { color: #EEE; }
    
    /* ═══ STATUS & PROGRESS ═══ */
    .stStatus {
        background: #000 !important;
        border: 1px solid #333 !important;
    }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #00E5FF, #FF007F);
    }
    
    /* ═══ ALERTS ═══ */
    .stSuccess {
        background: #000 !important;
        border: 1px solid #00FF00 !important;
        color: #00FF00 !important;
    }
    .stError {
        background: #000 !important;
        border: 1px solid #FF0000 !important;
        color: #FF0000 !important;
    }

    /* Hide Streamlit Bloat */
    #MainMenu, footer, header { visibility: hidden; }
    
    </style>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 3. BACKEND LOGIC (The Brains)
# ═══════════════════════════════════════════════════════════════════════════════

def get_api_key():
    """Ensure API Key is present"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key and 'user_api_key' in st.session_state:
        api_key = st.session_state.user_api_key
    return api_key

def classify_intent(client, text):
    """Decide: Chat vs Research"""
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Classify as 'CHAT' (Casual) or 'HUNT' (Research topic). Output one word."},
                {"role": "user", "content": text}
            ]
        )
        return res.choices[0].message.content.strip().upper()
    except:
        return "HUNT"

def perform_live_search(query):
    """Agent 01: REAL Internet Search (DuckDuckGo)"""
    if not SEARCH_AVAILABLE:
        return "⚠️ Library 'duckduckgo-search' missing. Using fallback.", []
        
    summary = ""
    sources = []
    try:
        # Searching the web...
        results = DDGS().text(query, max_results=5)
        for r in results:
            summary += f"- TITLE: {r['title']}\n  LINK: {r['href']}\n  BODY: {r['body']}\n\n"
            sources.append(r['title'])
    except Exception as e:
        summary = f"Search Error: {str(e)}"
    
    return summary, sources

def generate_strategic_report(client, query, web_data):
    """Agent 01: Deep Analysis"""
    system_prompt = """
    You are the Sovereign Intelligence Core. 
    Analyze the provided RAW WEB DATA for the user's query.
    
    Structure your response in High-End Markdown:
    1.  EXECUTIVE SUMMARY (Bold, 2 sentences)
    2. MARKET INTELLIGENCE (Bullet points)
    3. VIRAL ANGLES (For Content Creation)
    4. RISK ASSESSMENT
    
    Tone: Industrial, Professional, "War Room" style.
    """
    
    try:
        res = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"QUERY: {query}\n\nWEB DATA:\n{web_data}"}
            ],
            temperature=0.6
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"Intelligence Processing Failed: {str(e)}"

def casual_chat(client, text, history):
    """Fast Chat Response"""
    try:
        # Prepare history for context
        msgs = [{"role": "system", "content": "You are Sovereign. Professional, Sharp, Hinglish."}]
        # Add last few messages for context
        for m in history[-5:]:
            if "role" in m and "content" in m:
                msgs.append({"role": m["role"], "content": m["content"]})
        
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=msgs
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"Chat Error: {str(e)}"

# ═══════════════════════════════════════════════════════════════════════════════
# 4. MAIN UI EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    inject_custom_css()
    
    # --- SESSION STATE INIT ---
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "latest_report" not in st.session_state:
        st.session_state.latest_report = None

    # --- SIDEBAR CONTROLS ---
    with st.sidebar:
        st.markdown("### ⚡ SYSTEM STATUS")
        st.markdown("**SOVEREIGN ENGINE v5.0**")
        
        # API Check
        api_key = get_api_key()
        if not api_key:
            st.error("🔴 OFFLINE")
            k = st.text_input("API KEY REQUIRED", type="password")
            if k:
                st.session_state.user_api_key = k
                st.rerun()
            st.stop()
        else:
            st.success("🟢 ONLINE")
            
        st.markdown("---")
        st.markdown("### 👤 OPERATOR")
        st.markdown("**NAVEEN** | ALPHA TIER")
        
        st.markdown("---")
        st.markdown("### 🎯 CONTROLS")
        if st.button("🗑️ WIPE DATA"):
            st.session_state.messages = []
            st.session_state.latest_report = None
            st.rerun()
            
        st.markdown("---")
        st.markdown("### 📊 RESOURCES")
        col1, col2 = st.columns(2)
        col1.metric("CPU", "OPT")
        col2.metric("NET", "LIVE")

    # --- MAIN DISPLAY ---
    st.markdown("<h1>SOVEREIGN</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>INDUSTRIAL CONTENT PRODUCTION CORE</div>", unsafe_allow_html=True)

    # 1. INPUT FORM (Industrial Style)
    with st.form(key='war_room_input', clear_on_submit=True):
        col_in, col_btn = st.columns([5, 1])
        with col_in:
            user_input = st.text_input("COMMAND LINE", placeholder="Enter directive or chat...", label_visibility="collapsed")
        with col_btn:
            submitted = st.form_submit_button("🚀 EXECUTE")

    # 2. LOGIC PROCESSING
    if submitted and user_input:
        client = openai.OpenAI(api_key=api_key)
        
        # Add to history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Classification
        intent = classify_intent(client, user_input)
        
        if intent == "CHAT":
            # Fast Chat
            reply = casual_chat(client, user_input, st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        
        else:
            # Deep Research (HUNT)
            with st.status("🕵️ AGENT 01 ACTIVATED", expanded=True) as status:
                st.write("📡 Handshaking with Global Network...")
                time.sleep(1)
                
                st.write("🔍 Scouring Dark/Clear Web (DuckDuckGo)...")
                web_data, sources = perform_live_search(user_input)
                
                st.write("🧠 Compiling Strategic Intelligence (GPT-4o)...")
                report = generate_strategic_report(client, user_input, web_data)
                
                status.update(label="✅ INTELLIGENCE SECURED", state="complete", expanded=False)
                
                # Save report specially
                st.session_state.latest_report = {
                    "query": user_input,
                    "content": report,
                    "sources": sources,
                    "time": datetime.now().strftime("%H:%M")
                }
                # Also add summary to chat
                st.session_state.messages.append({"role": "assistant", "content": "Intelligence Report Generated. Check Dashboard below."})

    # 3. DISPLAY AREA (The "Stack")
    
    # A. Chat History (Terminal Style)
    if st.session_state.messages:
        st.markdown("<div class='neon-card'>", unsafe_allow_html=True)
        st.markdown("### 💬 COMMS LOG")
        for msg in st.session_state.messages[-4:]: # Show last 4 messages
            if msg['role'] == 'user':
                st.markdown(f"<span style='color:#00E5FF'><b>>> YOU:</b></span> {msg['content']}", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color:#FF007F'><b>>> SYS:</b></span> {msg['content']}", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # B. Research Report (The Heavy Hitter)
    if st.session_state.latest_report:
        rep = st.session_state.latest_report
        
        # Report Container
        st.markdown(f"""
        <div class='report-card'>
            <h2 style='color:#FF007F'>🕵️ INTELLIGENCE REPORT: {rep['query'].upper()}</h2>
            <p style='color:#666'>GENERATED AT {rep['time']} | SOURCE: AGENT 01</p>
            <hr style='border-color:#333'/>
            <div style='line-height: 1.8; font-size: 1.05rem;'>
                {rep['content']}
            </div>
            <br>
            <p style='color:#00E5FF'><b>📚 SOURCES VERIFIED:</b></p>
        """, unsafe_allow_html=True)
        
        # Sources as Tags
        for s in rep['sources']:
            st.markdown(f"- {s}")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # C. Decision Gate (Buttons)
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("✅ APPROVE & SCRIPT"):
                st.success("PROTOCOL INITIATED")
        with c2:
            st.button("🔄 REFINE DATA")
        with c3:
            st.button("❌ DISCARD")

if __name__ == "__main__":
    main()




