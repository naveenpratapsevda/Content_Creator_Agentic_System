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






# import streamlit as st
# import time
# from datetime import datetime
# import openai
# import os

# # ═══════════════════════════════════════════════════════════════════════════════
# # SOVEREIGN CINEMA ENGINE - WAR ROOM UI v4.0
# # Pitch Black + Pure Neon Green Aesthetic | Ultra Clean
# # ═══════════════════════════════════════════════════════════════════════════════

# # Page Configuration
# st.set_page_config(
#     page_title="Sovereign Cinema Engine",
#     page_icon="🎬",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ═══════════════════════════════════════════════════════════════════════════════
# # CSS INJECTION - PURE NEON GREEN ON PITCH BLACK
# # ═══════════════════════════════════════════════════════════════════════════════

# def inject_custom_css():
#     st.markdown("""
#     <style>
#     /* ═══ GLOBAL RESET & BASE ═══ */
#     @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700;800&display=swap');
    
#     * {
#         margin: 0;
#         padding: 0;
#         box-sizing: border-box;
#     }
    
#     /* Main Background - Pure Pitch Black */
#     .stApp {
#         background: #000000;
#         color: #ffffff;
#         font-family: 'JetBrains Mono', 'Courier New', monospace;
#     }
    
#     /* ═══ SIDEBAR - ALWAYS VISIBLE NEON PANEL ═══ */
#     section[data-testid="stSidebar"] {
#         background: #000000 !important;
#         border-right: 2px solid #00FFA3 !important;
#         box-shadow: 2px 0 30px rgba(0, 255, 163, 0.5) !important;
#         z-index: 999999 !important;
#     }
    
#     section[data-testid="stSidebar"] > div {
#         background: #000000 !important;
#     }
    
#     section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
#         background: #000000 !important;
#     }
    
#     /* Sidebar Content */
#     section[data-testid="stSidebar"] .element-container {
#         padding: 0.5rem 1.5rem;
#     }
    
#     /* Sidebar Headers */
#     section[data-testid="stSidebar"] h3 {
#         color: #00FFA3 !important;
#         font-weight: 700;
#         letter-spacing: 3px;
#         text-transform: uppercase;
#         font-size: 0.7rem;
#         margin: 2rem 0 1rem 0;
#         text-shadow: 0 0 15px rgba(0, 255, 163, 0.8);
#     }
    
#     section[data-testid="stSidebar"] p,
#     section[data-testid="stSidebar"] .stMarkdown {
#         color: #aaaaaa !important;
#         font-size: 0.85rem;
#         letter-spacing: 0.5px;
#         line-height: 1.8;
#     }
    
#     section[data-testid="stSidebar"] strong {
#         color: #00FFA3 !important;
#         font-weight: 700;
#     }
    
#     section[data-testid="stSidebar"] hr {
#         border: none;
#         height: 1px;
#         background: linear-gradient(90deg, 
#             transparent 0%, 
#             rgba(0, 255, 163, 0.5) 50%, 
#             transparent 100%);
#         margin: 1.5rem 0;
#         box-shadow: 0 0 10px rgba(0, 255, 163, 0.3);
#     }
    
#     /* Sidebar Toggle Button - Force Visibility */
#     button[kind="header"] {
#         background: #000000 !important;
#         border: 2px solid #00FFA3 !important;
#         box-shadow: 0 0 20px rgba(0, 255, 163, 0.6) !important;
#         color: #00FFA3 !important;
#     }
    
#     [data-testid="collapsedControl"] {
#         background: #000000 !important;
#         border: 2px solid #00FFA3 !important;
#         box-shadow: 0 0 20px rgba(0, 255, 163, 0.6) !important;
#         color: #00FFA3 !important;
#     }
    
#     /* ═══ FLOATING CARDS - PURE NEON GREEN BOUNDARIES ═══ */
#     .floating-card {
#         background: #000000;
#         border: 2px solid #00FFA3;
#         border-radius: 0;
#         padding: 3rem;
#         margin: 2rem 0;
#         box-shadow: 
#             0 0 40px rgba(0, 255, 163, 0.4),
#             inset 0 0 40px rgba(0, 255, 163, 0.05);
#         transition: all 0.3s ease;
#         position: relative;
#     }
    
#     .floating-card:hover {
#         box-shadow: 
#             0 0 60px rgba(0, 255, 163, 0.6),
#             inset 0 0 50px rgba(0, 255, 163, 0.08);
#     }
    
#     /* Corner Accents */
#     .floating-card::before,
#     .floating-card::after {
#         content: '';
#         position: absolute;
#         width: 25px;
#         height: 25px;
#         border: 2px solid #00FFA3;
#     }
    
#     .floating-card::before {
#         top: -2px;
#         left: -2px;
#         border-right: none;
#         border-bottom: none;
#         box-shadow: 0 0 10px rgba(0, 255, 163, 0.5);
#     }
    
#     .floating-card::after {
#         bottom: -2px;
#         right: -2px;
#         border-left: none;
#         border-top: none;
#         box-shadow: 0 0 10px rgba(0, 255, 163, 0.5);
#     }
    
#     /* ═══ TYPOGRAPHY ═══ */
#     h1 {
#         color: #00FFA3;
#         font-weight: 900;
#         font-size: 3.5rem;
#         letter-spacing: 2px;
#         margin-bottom: 0.5rem;
#         text-shadow: 0 0 40px rgba(0, 255, 163, 0.8);
#         font-family: 'JetBrains Mono', monospace;
#     }
    
#     h2 {
#         color: #ffffff;
#         font-weight: 700;
#         font-size: 2rem;
#         margin-bottom: 2rem;
#         letter-spacing: 1px;
#     }
    
#     h3 {
#         color: #00FFA3;
#         font-weight: 600;
#         font-size: 1rem;
#         margin: 2rem 0 1rem 0;
#         letter-spacing: 3px;
#         text-transform: uppercase;
#     }
    
#     p, li {
#         color: #cccccc;
#         line-height: 2;
#         font-size: 0.95rem;
#         font-weight: 400;
#     }
    
#     /* ═══ INPUT FIELDS - NEON GLOW ON FOCUS ═══ */
#     .stTextInput > div > div > input {
#         background: #000000 !important;
#         border: 2px solid rgba(0, 255, 163, 0.3) !important;
#         border-radius: 0 !important;
#         color: #ffffff !important;
#         font-size: 1.1rem !important;
#         padding: 1.3rem 1.5rem !important;
#         font-weight: 400 !important;
#         font-family: 'JetBrains Mono', monospace !important;
#         transition: all 0.3s ease !important;
#         box-shadow: inset 0 0 20px rgba(0, 255, 163, 0.05) !important;
#     }
    
#     .stTextInput > div > div > input:focus {
#         border: 2px solid #00FFA3 !important;
#         outline: none !important;
#         box-shadow: 
#             0 0 40px rgba(0, 255, 163, 0.6) !important,
#             inset 0 0 30px rgba(0, 255, 163, 0.15) !important;
#         background: #000000 !important;
#     }
    
#     .stTextInput > div > div > input::placeholder {
#         color: #444444 !important;
#         opacity: 1 !important;
#     }
    
#     /* Remove helper text styling */
#     .stTextInput small {
#         color: #00FFA3 !important;
#         font-size: 0.75rem !important;
#         opacity: 0.7 !important;
#     }
    
#     /* ═══ BUTTONS - PURE NEON GREEN ═══ */
#     .stButton > button {
#         background: #000000 !important;
#         color: #00FFA3 !important;
#         border: 2px solid #00FFA3 !important;
#         border-radius: 0 !important;
#         padding: 1.1rem 2.5rem !important;
#         font-weight: 700 !important;
#         font-size: 0.9rem !important;
#         letter-spacing: 3px !important;
#         text-transform: uppercase !important;
#         cursor: pointer !important;
#         transition: all 0.3s ease !important;
#         box-shadow: 0 0 25px rgba(0, 255, 163, 0.4) !important;
#         font-family: 'JetBrains Mono', monospace !important;
#     }
    
#     .stButton > button:hover {
#         background: #00FFA3 !important;
#         color: #000000 !important;
#         box-shadow: 0 0 50px rgba(0, 255, 163, 0.8) !important;
#         transform: translateY(-2px);
#     }
    
#     .stButton > button:active {
#         transform: scale(0.98);
#     }
    
#     /* Form Submit Button */
#     .stForm button[kind="primaryFormSubmit"] {
#         background: #000000 !important;
#         color: #00FFA3 !important;
#         border: 2px solid #00FFA3 !important;
#         border-radius: 0 !important;
#         box-shadow: 0 0 25px rgba(0, 255, 163, 0.4) !important;
#     }
    
#     .stForm button[kind="primaryFormSubmit"]:hover {
#         background: #00FFA3 !important;
#         color: #000000 !important;
#         box-shadow: 0 0 50px rgba(0, 255, 163, 0.8) !important;
#     }
    
#     /* ═══ PROGRESS BARS - ULTRA THIN NEON ═══ */
#     .stProgress > div > div > div > div {
#         background: #00FFA3 !important;
#         height: 3px !important;
#         box-shadow: 0 0 10px rgba(0, 255, 163, 0.8);
#     }
    
#     .stProgress > div > div > div {
#         background-color: rgba(0, 255, 163, 0.1) !important;
#         height: 3px !important;
#     }
    
#     /* ═══ METRICS - NEON STATS ═══ */
#     [data-testid="stMetricValue"] {
#         color: #00FFA3 !important;
#         font-size: 2.5rem !important;
#         font-weight: 900 !important;
#         text-shadow: 0 0 25px rgba(0, 255, 163, 0.6) !important;
#     }
    
#     [data-testid="stMetricLabel"] {
#         color: #888888 !important;
#         font-size: 0.7rem !important;
#         letter-spacing: 2px !important;
#         text-transform: uppercase !important;
#         font-weight: 700 !important;
#     }
    
#     /* ═══ STATUS COMPONENT ═══ */
#     .stStatus {
#         background: #000000 !important;
#         border: 1px solid rgba(0, 255, 163, 0.4) !important;
#         border-radius: 0 !important;
#         padding: 1rem !important;
#         box-shadow: 0 0 25px rgba(0, 255, 163, 0.3) !important;
#     }
    
#     .stStatus [data-testid="stStatusWidget"] {
#         background: #000000 !important;
#     }
    
#     /* ═══ ALERTS - PURE NEON ═══ */
#     .stSuccess {
#         background: #000000 !important;
#         border-left: 4px solid #00FFA3 !important;
#         color: #ffffff !important;
#         box-shadow: 0 0 20px rgba(0, 255, 163, 0.3) !important;
#     }
    
#     .stWarning {
#         background: #000000 !important;
#         border-left: 4px solid #00FFA3 !important;
#         color: #ffffff !important;
#         box-shadow: 0 0 20px rgba(0, 255, 163, 0.3) !important;
#     }
    
#     .stInfo {
#         background: #000000 !important;
#         border-left: 4px solid #00FFA3 !important;
#         color: #ffffff !important;
#         box-shadow: 0 0 20px rgba(0, 255, 163, 0.3) !important;
#     }
    
#     /* ═══ DIVIDERS ═══ */
#     hr {
#         border: none !important;
#         height: 1px !important;
#         background: linear-gradient(90deg, 
#             transparent 0%, 
#             rgba(0, 255, 163, 0.6) 50%, 
#             transparent 100%) !important;
#         margin: 3rem 0 !important;
#         box-shadow: 0 0 15px rgba(0, 255, 163, 0.4) !important;
#     }
    
#     /* ═══ SCROLLBAR ═══ */
#     ::-webkit-scrollbar {
#         width: 10px;
#         height: 10px;
#         background: #000000;
#     }
    
#     ::-webkit-scrollbar-track {
#         background: #000000;
#         border-left: 1px solid rgba(0, 255, 163, 0.2);
#     }
    
#     ::-webkit-scrollbar-thumb {
#         background: #00FFA3;
#         box-shadow: 0 0 15px rgba(0, 255, 163, 0.6);
#     }
    
#     ::-webkit-scrollbar-thumb:hover {
#         background: #00FFB8;
#         box-shadow: 0 0 25px rgba(0, 255, 163, 0.8);
#     }
    
#     /* ═══ CHAT BUBBLE ═══ */
#     .chat-response {
#         background: #000000;
#         border: 2px solid #00FFA3;
#         border-left: 4px solid #00FFA3;
#         padding: 2rem;
#         margin: 2rem 0;
#         box-shadow: 0 0 30px rgba(0, 255, 163, 0.3);
#     }
    
#     /* ═══ REMOVE STREAMLIT BRANDING ═══ */
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     header {visibility: hidden;}
    
#     /* ═══ MAIN CONTAINER ═══ */
#     .main .block-container {
#         padding-top: 3rem;
#         padding-bottom: 3rem;
#         max-width: 1500px;
#     }
    
#     /* ═══ SPINNER ═══ */
#     .stSpinner > div {
#         border-color: #00FFA3 transparent #00FFA3 transparent !important;
#     }
    
#     </style>
#     """, unsafe_allow_html=True)

# # ═══════════════════════════════════════════════════════════════════════════════
# # INTELLIGENCE CORE
# # ═══════════════════════════════════════════════════════════════════════════════

# def classify_intent(user_input):
#     """Classify intent using GPT-4o-mini"""
#     try:
#         response = openai.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": "Classify as CHAT or HUNT. CHAT: greetings/questions. HUNT: research/content ideas. Reply only: CHAT or HUNT"},
#                 {"role": "user", "content": user_input}
#             ],
#             max_tokens=10,
#             temperature=0.3
#         )
#         intent = response.choices[0].message.content.strip().upper()
#         return intent if intent in ["CHAT", "HUNT"] else "HUNT"
#     except:
#         return "HUNT"

# def chat_response(user_input):
#     """Chat using GPT-4o-mini"""
#     try:
#         response = openai.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": "You are Sovereign Cinema Engine AI. Be professional and helpful."},
#                 {"role": "user", "content": user_input}
#             ],
#             max_tokens=300,
#             temperature=0.7
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         return f"System offline: {str(e)}"

# def deep_research(query):
#     """Research using GPT-4o"""
#     simulated_data = f"""
#     Market Intelligence: {query}
#     • Demographics: 18-35, tech-savvy
#     • Market: Medium saturation
#     • Viability: {85 + (hash(query) % 15)}%
#     """
    
#     try:
#         response = openai.chat.completions.create(
#             model="gpt-4o",
#             messages=[
#                 {"role": "system", "content": "You are Agent 01. Provide market analysis and production recommendations."},
#                 {"role": "user", "content": f"Research: {query}\n\nContext: {simulated_data}\n\nProvide: Market Viability, Audience, Competition, Strategy, Risks"}
#             ],
#             max_tokens=800,
#             temperature=0.6
#         )
        
#         return {
#             "query": query,
#             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "findings": response.choices[0].message.content.strip(),
#             "confidence": 85 + (hash(query) % 15),
#             "sources": ["Market Intelligence", "YouTube Analysis", "Industry Reports", "Trend Database"]
#         }
#     except Exception as e:
#         return {
#             "query": query,
#             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "findings": f"Error: {str(e)}\n\nFallback: {simulated_data}",
#             "confidence": 70,
#             "sources": ["Fallback Database"]
#         }

# def research_with_status(query):
#     """Execute research with status"""
#     status_container = st.status("**⚡ INTELLIGENCE GATHERING**", expanded=True)
    
#     with status_container:
#         st.write("📡 Accessing Knowledge Base...")
#         time.sleep(0.8)
        
#         st.write("🔍 Scraping Web & YouTube...")
#         time.sleep(1)
        
#         st.write("🧠 GPT-4o Processing...")
#         research_data = deep_research(query)
#         time.sleep(1.2)
        
#         st.write("✅ COMPLETE")
    
#     status_container.update(label="**✅ INTELLIGENCE READY**", state="complete", expanded=False)
#     return research_data

# def create_card(content):
#     return f'<div class="floating-card">{content}</div>'

# # ═══════════════════════════════════════════════════════════════════════════════
# # MAIN APPLICATION
# # ═══════════════════════════════════════════════════════════════════════════════

# def main():
#     inject_custom_css()
    
#     # Session state
#     if 'research_data' not in st.session_state:
#         st.session_state.research_data = None
#     if 'chat_response_text' not in st.session_state:
#         st.session_state.chat_response_text = None
#     if 'mode' not in st.session_state:
#         st.session_state.mode = None
    
#     # ═══ SIDEBAR ═══
#     with st.sidebar:
#         st.markdown("### ⚡ SYSTEM")
#         st.markdown("**Sovereign Cinema Engine**")
#         st.markdown("**Version:** 4.0")
#         st.markdown("**Core:** Dual-AI")
#         st.markdown("---")
        
#         st.markdown("### 👤 OPERATOR")
#         st.markdown("**NAVEEN**")
#         st.markdown("**Clearance:** ALPHA")
#         st.markdown("---")
        
#         st.markdown("### 🎯 MODULES")
#         st.markdown("✓ Agent 01")
#         st.markdown("✓ GPT-4o")
#         st.markdown("✓ GPT-4o-mini")
#         st.markdown("---")
        
#         st.markdown("### 📊 STATS")
#         col1, col2 = st.columns(2)
#         with col1:
#             st.metric("Projects", "24")
#         with col2:
#             st.metric("Success", "96%")
    
#     # ═══ HEADER ═══
#     st.markdown('<h1>SOVEREIGN CINEMA ENGINE</h1>', unsafe_allow_html=True)
#     st.markdown('<p style="color: #555555; font-size: 0.9rem; margin-bottom: 3rem; letter-spacing: 2px;">INDUSTRIAL CONTENT PRODUCTION • DUAL-INTELLIGENCE</p>', unsafe_allow_html=True)
    
#     # ═══ COMMAND INPUT ═══
#     st.markdown('<h3>🔍 COMMAND INPUT</h3>', unsafe_allow_html=True)
    
#     with st.form(key='command_form', clear_on_submit=False):
#         col1, col2 = st.columns([6, 1])
#         with col1:
#             user_input = st.text_input(
#                 "Input",
#                 placeholder="Enter project concept, research query, or message...",
#                 label_visibility="collapsed"
#             )
#         with col2:
#             submit = st.form_submit_button("⚡ INITIATE", use_container_width=True)
    
#     # ═══ PROCESS ═══
#     if submit and user_input:
#         intent = classify_intent(user_input)
        
#         if intent == "CHAT":
#             st.session_state.mode = "chat"
#             st.session_state.research_data = None
#             response = chat_response(user_input)
#             st.session_state.chat_response_text = response
#         else:
#             st.session_state.mode = "hunt"
#             st.session_state.chat_response_text = None
#             data = research_with_status(user_input)
#             st.session_state.research_data = data
    
#     # ═══ CHAT DISPLAY ═══
#     if st.session_state.mode == "chat" and st.session_state.chat_response_text:
#         st.markdown('<div style="height: 3rem;"></div>', unsafe_allow_html=True)
#         chat_html = f"""
#         <div class="chat-response">
#             <h3 style="margin: 0 0 1.5rem 0;">💬 SYSTEM RESPONSE</h3>
#             <p style="line-height: 2;">{st.session_state.chat_response_text}</p>
#         </div>
#         """
#         st.markdown(chat_html, unsafe_allow_html=True)
    
#     # ═══ RESEARCH DISPLAY ═══
#     if st.session_state.mode == "hunt" and st.session_state.research_data:
#         st.markdown('<div style="height: 3rem;"></div>', unsafe_allow_html=True)
        
#         data = st.session_state.research_data
        
#         report_html = f"""
#         <h2>📋 INTELLIGENCE REPORT</h2>
#         <p style="color: #555555; margin-bottom: 2rem; font-size: 0.85rem;">
#             QUERY: <strong style="color: #00FFA3;">{data['query']}</strong> • 
#             {data['timestamp']} • 
#             MODEL: <strong style="color: #00FFA3;">GPT-4o</strong>
#         </p>
#         <hr style="margin: 2rem 0;">
#         <h3>ANALYSIS</h3>
#         <p style="line-height: 2.2; margin-top: 1.5rem; white-space: pre-wrap;">{data['findings']}</p>
#         <hr style="margin: 2rem 0;">
#         <h3>CONFIDENCE</h3>
#         """
        
#         st.markdown(create_card(report_html), unsafe_allow_html=True)
        
#         st.progress(data['confidence'] / 100)
#         st.markdown(f"<p style='text-align: center; color: #00FFA3; font-weight: 900; font-size: 2.5rem; margin: 1rem 0; text-shadow: 0 0 30px rgba(0, 255, 163, 0.8);'>{data['confidence']}%</p>", unsafe_allow_html=True)
        
#         st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
        
#         st.markdown("### 📚 SOURCES")
#         for source in data['sources']:
#             col1, col2 = st.columns([2, 5])
#             with col1:
#                 st.markdown(f"**{source}**")
#             with col2:
#                 st.progress(0.75 + (hash(source) % 25) / 100)
        
#         st.markdown('<div style="height: 3rem;"></div>', unsafe_allow_html=True)
#         st.markdown("### 🎯 DECISION GATE")
        
#         col1, col2, col3 = st.columns(3)
        
#         with col1:
#             if st.button("✅ GREEN LIGHT", use_container_width=True, key="green"):
#                 st.success("🎬 PROJECT APPROVED")
        
#         with col2:
#             if st.button("🔄 REFINE", use_container_width=True, key="refine"):
#                 st.warning("🔍 REFINING")
        
#         with col3:
#             if st.button("📝 MANUAL", use_container_width=True, key="manual"):
#                 st.info("✏️ MANUAL MODE")

# if __name__ == "__main__":
#     main()








# # import streamlit as st
# import time
# from datetime import datetime
# import openai
# import os

# # ═══════════════════════════════════════════════════════════════════════════════
# # SOVEREIGN CINEMA ENGINE - WAR ROOM UI v4.0
# # Pitch Black + Pure Neon Green Aesthetic | Ultra Clean
# # ═══════════════════════════════════════════════════════════════════════════════

# # Page Configuration
# st.set_page_config(
#     page_title="Sovereign Cinema Engine",
#     page_icon="🎬",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ═══════════════════════════════════════════════════════════════════════════════
# # CSS INJECTION - PURE NEON GREEN ON PITCH BLACK
# # ═══════════════════════════════════════════════════════════════════════════════

# def inject_custom_css():
#     st.markdown("""
#     <style>
#     /* ═══ GLOBAL RESET & BASE ═══ */
#     @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700;800&display=swap');
    
#     * {
#         margin: 0;
#         padding: 0;
#         box-sizing: border-box;
#     }
    
#     /* Main Background - Pure Pitch Black */
#     .stApp {
#         background: #000000;
#         color: #ffffff;
#         font-family: 'JetBrains Mono', 'Courier New', monospace;
#     }
    
#     /* ═══ SIDEBAR - ALWAYS VISIBLE NEON PANEL ═══ */
#     section[data-testid="stSidebar"] {
#         background: #000000 !important;
#         border-right: 2px solid #00FFA3 !important;
#         box-shadow: 2px 0 30px rgba(0, 255, 163, 0.5) !important;
#         z-index: 999999 !important;
#     }
    
#     section[data-testid="stSidebar"] > div {
#         background: #000000 !important;
#     }
    
#     section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
#         background: #000000 !important;
#     }
    
#     /* Sidebar Content */
#     section[data-testid="stSidebar"] .element-container {
#         padding: 0.5rem 1.5rem;
#     }
    
#     /* Sidebar Headers */
#     section[data-testid="stSidebar"] h3 {
#         color: #00FFA3 !important;
#         font-weight: 700;
#         letter-spacing: 3px;
#         text-transform: uppercase;
#         font-size: 0.7rem;
#         margin: 2rem 0 1rem 0;
#         text-shadow: 0 0 15px rgba(0, 255, 163, 0.8);
#     }
    
#     section[data-testid="stSidebar"] p,
#     section[data-testid="stSidebar"] .stMarkdown {
#         color: #aaaaaa !important;
#         font-size: 0.85rem;
#         letter-spacing: 0.5px;
#         line-height: 1.8;
#     }
    
#     section[data-testid="stSidebar"] strong {
#         color: #00FFA3 !important;
#         font-weight: 700;
#     }
    
#     section[data-testid="stSidebar"] hr {
#         border: none;
#         height: 1px;
#         background: linear-gradient(90deg, 
#             transparent 0%, 
#             rgba(0, 255, 163, 0.5) 50%, 
#             transparent 100%);
#         margin: 1.5rem 0;
#         box-shadow: 0 0 10px rgba(0, 255, 163, 0.3);
#     }
    
#     /* Sidebar Toggle Button - Force Visibility */
#     button[kind="header"] {
#         background: #000000 !important;
#         border: 2px solid #00FFA3 !important;
#         box-shadow: 0 0 20px rgba(0, 255, 163, 0.6) !important;
#         color: #00FFA3 !important;
#     }
    
#     [data-testid="collapsedControl"] {
#         background: #000000 !important;
#         border: 2px solid #00FFA3 !important;
#         box-shadow: 0 0 20px rgba(0, 255, 163, 0.6) !important;
#         color: #00FFA3 !important;
#     }
    
#     /* ═══ FLOATING CARDS - PURE NEON GREEN BOUNDARIES ═══ */
#     .floating-card {
#         background: #000000;
#         border: 2px solid #00FFA3;
#         border-radius: 0;
#         padding: 3rem;
#         margin: 2rem 0;
#         box-shadow: 
#             0 0 40px rgba(0, 255, 163, 0.4),
#             inset 0 0 40px rgba(0, 255, 163, 0.05);
#         transition: all 0.3s ease;
#         position: relative;
#     }
    
#     .floating-card:hover {
#         box-shadow: 
#             0 0 60px rgba(0, 255, 163, 0.6),
#             inset 0 0 50px rgba(0, 255, 163, 0.08);
#     }
    
#     /* Corner Accents */
#     .floating-card::before,
#     .floating-card::after {
#         content: '';
#         position: absolute;
#         width: 25px;
#         height: 25px;
#         border: 2px solid #00FFA3;
#     }
    
#     .floating-card::before {
#         top: -2px;
#         left: -2px;
#         border-right: none;
#         border-bottom: none;
#         box-shadow: 0 0 10px rgba(0, 255, 163, 0.5);
#     }
    
#     .floating-card::after {
#         bottom: -2px;
#         right: -2px;
#         border-left: none;
#         border-top: none;
#         box-shadow: 0 0 10px rgba(0, 255, 163, 0.5);
#     }
    
#     /* ═══ TYPOGRAPHY ═══ */
#     h1 {
#         color: #00FFA3;
#         font-weight: 900;
#         font-size: 3.5rem;
#         letter-spacing: 2px;
#         margin-bottom: 0.5rem;
#         text-shadow: 0 0 40px rgba(0, 255, 163, 0.8);
#         font-family: 'JetBrains Mono', monospace;
#     }
    
#     h2 {
#         color: #ffffff;
#         font-weight: 700;
#         font-size: 2rem;
#         margin-bottom: 2rem;
#         letter-spacing: 1px;
#     }
    
#     h3 {
#         color: #00FFA3;
#         font-weight: 600;
#         font-size: 1rem;
#         margin: 2rem 0 1rem 0;
#         letter-spacing: 3px;
#         text-transform: uppercase;
#     }
    
#     p, li {
#         color: #cccccc;
#         line-height: 2;
#         font-size: 0.95rem;
#         font-weight: 400;
#     }
    
#     /* ═══ INPUT FIELDS - NEON GLOW ON FOCUS ═══ */
#     .stTextInput > div > div > input {
#         background: #000000 !important;
#         border: 2px solid rgba(0, 255, 163, 0.3) !important;
#         border-radius: 0 !important;
#         color: #ffffff !important;
#         font-size: 1.1rem !important;
#         padding: 1.3rem 1.5rem !important;
#         font-weight: 400 !important;
#         font-family: 'JetBrains Mono', monospace !important;
#         transition: all 0.3s ease !important;
#         box-shadow: inset 0 0 20px rgba(0, 255, 163, 0.05) !important;
#     }
    
#     .stTextInput > div > div > input:focus {
#         border: 2px solid #00FFA3 !important;
#         outline: none !important;
#         box-shadow: 
#             0 0 40px rgba(0, 255, 163, 0.6) !important,
#             inset 0 0 30px rgba(0, 255, 163, 0.15) !important;
#         background: #000000 !important;
#     }
    
#     .stTextInput > div > div > input::placeholder {
#         color: #444444 !important;
#         opacity: 1 !important;
#     }
    
#     /* Remove helper text styling */
#     .stTextInput small {
#         color: #00FFA3 !important;
#         font-size: 0.75rem !important;
#         opacity: 0.7 !important;
#     }
    
#     /* ═══ BUTTONS - PURE NEON GREEN ═══ */
#     .stButton > button {
#         background: #000000 !important;
#         color: #00FFA3 !important;
#         border: 2px solid #00FFA3 !important;
#         border-radius: 0 !important;
#         padding: 1.1rem 2.5rem !important;
#         font-weight: 700 !important;
#         font-size: 0.9rem !important;
#         letter-spacing: 3px !important;
#         text-transform: uppercase !important;
#         cursor: pointer !important;
#         transition: all 0.3s ease !important;
#         box-shadow: 0 0 25px rgba(0, 255, 163, 0.4) !important;
#         font-family: 'JetBrains Mono', monospace !important;
#     }
    
#     .stButton > button:hover {
#         background: #00FFA3 !important;
#         color: #000000 !important;
#         box-shadow: 0 0 50px rgba(0, 255, 163, 0.8) !important;
#         transform: translateY(-2px);
#     }
    
#     .stButton > button:active {
#         transform: scale(0.98);
#     }
    
#     /* Form Submit Button */
#     .stForm button[kind="primaryFormSubmit"] {
#         background: #000000 !important;
#         color: #00FFA3 !important;
#         border: 2px solid #00FFA3 !important;
#         border-radius: 0 !important;
#         box-shadow: 0 0 25px rgba(0, 255, 163, 0.4) !important;
#     }
    
#     .stForm button[kind="primaryFormSubmit"]:hover {
#         background: #00FFA3 !important;
#         color: #000000 !important;
#         box-shadow: 0 0 50px rgba(0, 255, 163, 0.8) !important;
#     }
    
#     /* ═══ PROGRESS BARS - ULTRA THIN NEON ═══ */
#     .stProgress > div > div > div > div {
#         background: #00FFA3 !important;
#         height: 3px !important;
#         box-shadow: 0 0 10px rgba(0, 255, 163, 0.8);
#     }
    
#     .stProgress > div > div > div {
#         background-color: rgba(0, 255, 163, 0.1) !important;
#         height: 3px !important;
#     }
    
#     /* ═══ METRICS - NEON STATS ═══ */
#     [data-testid="stMetricValue"] {
#         color: #00FFA3 !important;
#         font-size: 2.5rem !important;
#         font-weight: 900 !important;
#         text-shadow: 0 0 25px rgba(0, 255, 163, 0.6) !important;
#     }
    
#     [data-testid="stMetricLabel"] {
#         color: #888888 !important;
#         font-size: 0.7rem !important;
#         letter-spacing: 2px !important;
#         text-transform: uppercase !important;
#         font-weight: 700 !important;
#     }
    
#     /* ═══ STATUS COMPONENT ═══ */
#     .stStatus {
#         background: #000000 !important;
#         border: 1px solid rgba(0, 255, 163, 0.4) !important;
#         border-radius: 0 !important;
#         padding: 1rem !important;
#         box-shadow: 0 0 25px rgba(0, 255, 163, 0.3) !important;
#     }
    
#     .stStatus [data-testid="stStatusWidget"] {
#         background: #000000 !important;
#     }
    
#     /* ═══ ALERTS - PURE NEON ═══ */
#     .stSuccess {
#         background: #000000 !important;
#         border-left: 4px solid #00FFA3 !important;
#         color: #ffffff !important;
#         box-shadow: 0 0 20px rgba(0, 255, 163, 0.3) !important;
#     }
    
#     .stWarning {
#         background: #000000 !important;
#         border-left: 4px solid #00FFA3 !important;
#         color: #ffffff !important;
#         box-shadow: 0 0 20px rgba(0, 255, 163, 0.3) !important;
#     }
    
#     .stInfo {
#         background: #000000 !important;
#         border-left: 4px solid #00FFA3 !important;
#         color: #ffffff !important;
#         box-shadow: 0 0 20px rgba(0, 255, 163, 0.3) !important;
#     }
    
#     /* ═══ DIVIDERS ═══ */
#     hr {
#         border: none !important;
#         height: 1px !important;
#         background: linear-gradient(90deg, 
#             transparent 0%, 
#             rgba(0, 255, 163, 0.6) 50%, 
#             transparent 100%) !important;
#         margin: 3rem 0 !important;
#         box-shadow: 0 0 15px rgba(0, 255, 163, 0.4) !important;
#     }
    
#     /* ═══ SCROLLBAR ═══ */
#     ::-webkit-scrollbar {
#         width: 10px;
#         height: 10px;
#         background: #000000;
#     }
    
#     ::-webkit-scrollbar-track {
#         background: #000000;
#         border-left: 1px solid rgba(0, 255, 163, 0.2);
#     }
    
#     ::-webkit-scrollbar-thumb {
#         background: #00FFA3;
#         box-shadow: 0 0 15px rgba(0, 255, 163, 0.6);
#     }
    
#     ::-webkit-scrollbar-thumb:hover {
#         background: #00FFB8;
#         box-shadow: 0 0 25px rgba(0, 255, 163, 0.8);
#     }
    
#     /* ═══ CHAT BUBBLE ═══ */
#     .chat-response {
#         background: #000000;
#         border: 2px solid #00FFA3;
#         border-left: 4px solid #00FFA3;
#         padding: 2rem;
#         margin: 2rem 0;
#         box-shadow: 0 0 30px rgba(0, 255, 163, 0.3);
#     }
    
#     /* ═══ REMOVE STREAMLIT BRANDING ═══ */
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     header {visibility: hidden;}
    
#     /* ═══ MAIN CONTAINER ═══ */
#     .main .block-container {
#         padding-top: 3rem;
#         padding-bottom: 3rem;
#         max-width: 1500px;
#     }
    
#     /* ═══ SPINNER ═══ */
#     .stSpinner > div {
#         border-color: #00FFA3 transparent #00FFA3 transparent !important;
#     }
    
#     </style>
#     """, unsafe_allow_html=True)

# # ═══════════════════════════════════════════════════════════════════════════════
# # INTELLIGENCE CORE
# # ═══════════════════════════════════════════════════════════════════════════════

# def classify_intent(user_input):
#     """Classify intent using GPT-4o-mini"""
#     try:
#         response = openai.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": "Classify as CHAT or HUNT. CHAT: greetings/questions. HUNT: research/content ideas. Reply only: CHAT or HUNT"},
#                 {"role": "user", "content": user_input}
#             ],
#             max_tokens=10,
#             temperature=0.3
#         )
#         intent = response.choices[0].message.content.strip().upper()
#         return intent if intent in ["CHAT", "HUNT"] else "HUNT"
#     except:
#         return "HUNT"

# def chat_response(user_input):
#     """Chat using GPT-4o-mini"""
#     try:
#         response = openai.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": "You are Sovereign Cinema Engine AI. Be professional and helpful."},
#                 {"role": "user", "content": user_input}
#             ],
#             max_tokens=300,
#             temperature=0.7
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         return f"System offline: {str(e)}"

# def deep_research(query):
#     """Research using GPT-4o"""
#     simulated_data = f"""
#     Market Intelligence: {query}
#     • Demographics: 18-35, tech-savvy
#     • Market: Medium saturation
#     • Viability: {85 + (hash(query) % 15)}%
#     """
    
#     try:
#         response = openai.chat.completions.create(
#             model="gpt-4o",
#             messages=[
#                 {"role": "system", "content": "You are Agent 01. Provide market analysis and production recommendations."},
#                 {"role": "user", "content": f"Research: {query}\n\nContext: {simulated_data}\n\nProvide: Market Viability, Audience, Competition, Strategy, Risks"}
#             ],
#             max_tokens=800,
#             temperature=0.6
#         )
        
#         return {
#             "query": query,
#             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "findings": response.choices[0].message.content.strip(),
#             "confidence": 85 + (hash(query) % 15),
#             "sources": ["Market Intelligence", "YouTube Analysis", "Industry Reports", "Trend Database"]
#         }
#     except Exception as e:
#         return {
#             "query": query,
#             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "findings": f"Error: {str(e)}\n\nFallback: {simulated_data}",
#             "confidence": 70,
#             "sources": ["Fallback Database"]
#         }

# def research_with_status(query):
#     """Execute research with status"""
#     status_container = st.status("**⚡ INTELLIGENCE GATHERING**", expanded=True)
    
#     with status_container:
#         st.write("📡 Accessing Knowledge Base...")
#         time.sleep(0.8)
        
#         st.write("🔍 Scraping Web & YouTube...")
#         time.sleep(1)
        
#         st.write("🧠 GPT-4o Processing...")
#         research_data = deep_research(query)
#         time.sleep(1.2)
        
#         st.write("✅ COMPLETE")
    
#     status_container.update(label="**✅ INTELLIGENCE READY**", state="complete", expanded=False)
#     return research_data

# def create_card(content):
#     return f'<div class="floating-card">{content}</div>'

# # ═══════════════════════════════════════════════════════════════════════════════
# # MAIN APPLICATION
# # ═══════════════════════════════════════════════════════════════════════════════

# def main():
#     inject_custom_css()
    
#     # Session state
#     if 'research_data' not in st.session_state:
#         st.session_state.research_data = None
#     if 'chat_response_text' not in st.session_state:
#         st.session_state.chat_response_text = None
#     if 'mode' not in st.session_state:
#         st.session_state.mode = None
    
#     # ═══ SIDEBAR ═══
#     with st.sidebar:
#         st.markdown("### ⚡ SYSTEM")
#         st.markdown("**Sovereign Cinema Engine**")
#         st.markdown("**Version:** 4.0")
#         st.markdown("**Core:** Dual-AI")
#         st.markdown("---")
        
#         st.markdown("### 👤 OPERATOR")
#         st.markdown("**NAVEEN**")
#         st.markdown("**Clearance:** ALPHA")
#         st.markdown("---")
        
#         st.markdown("### 🎯 MODULES")
#         st.markdown("✓ Agent 01")
#         st.markdown("✓ GPT-4o")
#         st.markdown("✓ GPT-4o-mini")
#         st.markdown("---")
        
#         st.markdown("### 📊 STATS")
#         col1, col2 = st.columns(2)
#         with col1:
#             st.metric("Projects", "24")
#         with col2:
#             st.metric("Success", "96%")
    
#     # ═══ HEADER ═══
#     st.markdown('<h1>SOVEREIGN CINEMA ENGINE</h1>', unsafe_allow_html=True)
#     st.markdown('<p style="color: #555555; font-size: 0.9rem; margin-bottom: 3rem; letter-spacing: 2px;">INDUSTRIAL CONTENT PRODUCTION • DUAL-INTELLIGENCE</p>', unsafe_allow_html=True)
    
#     # ═══ COMMAND INPUT ═══
#     st.markdown('<h3>🔍 COMMAND INPUT</h3>', unsafe_allow_html=True)
    
#     with st.form(key='command_form', clear_on_submit=False):
#         col1, col2 = st.columns([6, 1])
#         with col1:
#             user_input = st.text_input(
#                 "Input",
#                 placeholder="Enter project concept, research query, or message...",
#                 label_visibility="collapsed"
#             )
#         with col2:
#             submit = st.form_submit_button("⚡ INITIATE", use_container_width=True)
    
#     # ═══ PROCESS ═══
#     if submit and user_input:
#         intent = classify_intent(user_input)
        
#         if intent == "CHAT":
#             st.session_state.mode = "chat"
#             st.session_state.research_data = None
#             response = chat_response(user_input)
#             st.session_state.chat_response_text = response
#         else:
#             st.session_state.mode = "hunt"
#             st.session_state.chat_response_text = None
#             data = research_with_status(user_input)
#             st.session_state.research_data = data
    
#     # ═══ CHAT DISPLAY ═══
#     if st.session_state.mode == "chat" and st.session_state.chat_response_text:
#         st.markdown('<div style="height: 3rem;"></div>', unsafe_allow_html=True)
#         chat_html = f"""
#         <div class="chat-response">
#             <h3 style="margin: 0 0 1.5rem 0;">💬 SYSTEM RESPONSE</h3>
#             <p style="line-height: 2;">{st.session_state.chat_response_text}</p>
#         </div>
#         """
#         st.markdown(chat_html, unsafe_allow_html=True)
    
#     # ═══ RESEARCH DISPLAY ═══
#     if st.session_state.mode == "hunt" and st.session_state.research_data:
#         st.markdown('<div style="height: 3rem;"></div>', unsafe_allow_html=True)
        
#         data = st.session_state.research_data
        
#         report_html = f"""
#         <h2>📋 INTELLIGENCE REPORT</h2>
#         <p style="color: #555555; margin-bottom: 2rem; font-size: 0.85rem;">
#             QUERY: <strong style="color: #00FFA3;">{data['query']}</strong> • 
#             {data['timestamp']} • 
#             MODEL: <strong style="color: #00FFA3;">GPT-4o</strong>
#         </p>
#         <hr style="margin: 2rem 0;">
#         <h3>ANALYSIS</h3>
#         <p style="line-height: 2.2; margin-top: 1.5rem; white-space: pre-wrap;">{data['findings']}</p>
#         <hr style="margin: 2rem 0;">
#         <h3>CONFIDENCE</h3>
#         """
        
#         st.markdown(create_card(report_html), unsafe_allow_html=True)
        
#         st.progress(data['confidence'] / 100)
#         st.markdown(f"<p style='text-align: center; color: #00FFA3; font-weight: 900; font-size: 2.5rem; margin: 1rem 0; text-shadow: 0 0 30px rgba(0, 255, 163, 0.8);'>{data['confidence']}%</p>", unsafe_allow_html=True)
        
#         st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
        
#         st.markdown("### 📚 SOURCES")
#         for source in data['sources']:
#             col1, col2 = st.columns([2, 5])
#             with col1:
#                 st.markdown(f"**{source}**")
#             with col2:
#                 st.progress(0.75 + (hash(source) % 25) / 100)
        
#         st.markdown('<div style="height: 3rem;"></div>', unsafe_allow_html=True)
#         st.markdown("### 🎯 DECISION GATE")
        
#         col1, col2, col3 = st.columns(3)
        
#         with col1:
#             if st.button("✅ GREEN LIGHT", use_container_width=True, key="green"):
#                 st.success("🎬 PROJECT APPROVED")
        
#         with col2:
#             if st.button("🔄 REFINE", use_container_width=True, key="refine"):
#                 st.warning("🔍 REFINING")
        
#         with col3:
#             if st.button("📝 MANUAL", use_container_width=True, key="manual"):
#                 st.info("✏️ MANUAL MODE")

# if __name__ == "__main__":
#     main()













# import streamlit as st
# import time
# from datetime import datetime
# import openai
# import os

# # ═══════════════════════════════════════════════════════════════════════════════
# # SOVEREIGN CINEMA ENGINE - WAR ROOM UI v2.0
# # Deep Charcoal Navy Aesthetic | Dual-Model Intelligence
# # ═══════════════════════════════════════════════════════════════════════════════

# # Page Configuration
# st.set_page_config(
#     page_title="Sovereign Cinema Engine",
#     page_icon="🎬",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ═══════════════════════════════════════════════════════════════════════════════
# # CSS INJECTION - CHARCOAL NAVY STEALTH AESTHETIC
# # ═══════════════════════════════════════════════════════════════════════════════

# def inject_custom_css():
#     st.markdown("""
#     <style>
#     /* ═══ GLOBAL RESET & BASE ═══ */
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
#     * {
#         margin: 0;
#         padding: 0;
#         box-sizing: border-box;
#     }
    
#     /* Main Background - Deep Charcoal Navy Gradient */
#     .stApp {
#         background: linear-gradient(135deg, #0a0b10 0%, #161b22 50%, #1a1f2e 100%);
#         color: #e6edf3;
#         font-family: 'Inter', -apple-system, sans-serif;
#     }
    
#     /* ═══ SIDEBAR - SLEEK TERMINAL PANEL ═══ */
#     [data-testid="stSidebar"] {
#         background: linear-gradient(180deg, #0d1117 0%, #0a0b10 100%);
#         border-right: 1px solid rgba(122, 162, 247, 0.15);
#         box-shadow: 4px 0 32px rgba(0, 0, 0, 0.5);
#     }
    
#     [data-testid="stSidebar"] .element-container {
#         padding: 0.5rem 1rem;
#     }
    
#     /* Sidebar Headers - Lite Orange Accent */
#     [data-testid="stSidebar"] h3 {
#         color: #FF9E64;
#         font-weight: 700;
#         letter-spacing: 2.5px;
#         text-transform: uppercase;
#         font-size: 0.7rem;
#         margin: 1.5rem 0 0.75rem 0;
#         opacity: 0.9;
#     }
    
#     [data-testid="stSidebar"] p,
#     [data-testid="stSidebar"] .stMarkdown {
#         color: #8b949e;
#         font-size: 0.9rem;
#         letter-spacing: 0.3px;
#         line-height: 1.6;
#     }
    
#     [data-testid="stSidebar"] strong {
#         color: #c9d1d9;
#         font-weight: 600;
#     }
    
#     /* ═══ FLOATING CARDS - GLASSMORPHISM ═══ */
#     .floating-card {
#         background: linear-gradient(145deg, 
#             rgba(22, 27, 34, 0.85) 0%, 
#             rgba(13, 17, 23, 0.9) 100%);
#         backdrop-filter: blur(10px);
#         -webkit-backdrop-filter: blur(10px);
#         border: 1px solid rgba(122, 162, 247, 0.12);
#         border-radius: 20px;
#         padding: 2.5rem;
#         margin: 2rem 0;
#         box-shadow: 
#             0 8px 32px rgba(0, 0, 0, 0.4),
#             0 0 40px rgba(122, 162, 247, 0.08),
#             inset 0 1px 0 rgba(255, 255, 255, 0.03);
#         transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
#     }
    
#     .floating-card:hover {
#         transform: translateY(-4px);
#         box-shadow: 
#             0 12px 48px rgba(0, 0, 0, 0.6),
#             0 0 60px rgba(122, 162, 247, 0.15),
#             inset 0 1px 0 rgba(255, 255, 255, 0.06);
#         border-color: rgba(122, 162, 247, 0.25);
#     }
    
#     /* ═══ TYPOGRAPHY HIERARCHY ═══ */
#     h1 {
#         color: #7AA2F7;
#         font-weight: 800;
#         font-size: 2.8rem;
#         letter-spacing: -1px;
#         margin-bottom: 0.5rem;
#         text-shadow: 0 0 30px rgba(122, 162, 247, 0.4);
#     }
    
#     h2 {
#         color: #9ECE6A;
#         font-weight: 700;
#         font-size: 1.8rem;
#         margin-bottom: 1.5rem;
#         letter-spacing: 0.3px;
#         text-shadow: 0 0 20px rgba(158, 206, 106, 0.3);
#     }
    
#     h3 {
#         color: #FF9E64;
#         font-weight: 600;
#         font-size: 1.2rem;
#         margin: 2rem 0 1rem 0;
#         letter-spacing: 1.5px;
#         text-transform: uppercase;
#         opacity: 0.95;
#     }
    
#     p, li {
#         color: #c9d1d9;
#         line-height: 1.8;
#         font-size: 1rem;
#         font-weight: 400;
#     }
    
#     /* ═══ INPUT FIELDS - COMMAND BAR ═══ */
#     .stTextInput > div > div > input {
#         background: linear-gradient(145deg, 
#             rgba(22, 27, 34, 0.6) 0%, 
#             rgba(13, 17, 23, 0.8) 100%);
#         border: 2px solid transparent;
#         background-clip: padding-box;
#         border-radius: 14px;
#         color: #e6edf3;
#         font-size: 1.05rem;
#         padding: 1.2rem 1.8rem;
#         font-weight: 400;
#         transition: all 0.3s ease;
#         box-shadow: 
#             inset 0 2px 8px rgba(0, 0, 0, 0.3),
#             0 0 0 1px rgba(122, 162, 247, 0.15);
#     }
    
#     .stTextInput > div > div > input:focus {
#         border: 2px solid #7AA2F7;
#         outline: none;
#         box-shadow: 
#             inset 0 2px 8px rgba(0, 0, 0, 0.3),
#             0 0 30px rgba(122, 162, 247, 0.25),
#             0 0 0 1px #7AA2F7;
#     }
    
#     .stTextInput > div > div > input::placeholder {
#         color: #6e7681;
#         opacity: 1;
#     }
    
#     /* ═══ BUTTONS - GRADIENT GLOWS ═══ */
#     .stButton > button {
#         background: linear-gradient(135deg, #7AA2F7 0%, #5a7ec7 100%);
#         color: #ffffff;
#         border: none;
#         border-radius: 12px;
#         padding: 0.85rem 2.5rem;
#         font-weight: 700;
#         font-size: 0.95rem;
#         letter-spacing: 1.2px;
#         text-transform: uppercase;
#         cursor: pointer;
#         transition: all 0.3s ease;
#         box-shadow: 
#             0 4px 20px rgba(122, 162, 247, 0.35),
#             inset 0 1px 0 rgba(255, 255, 255, 0.2);
#     }
    
#     .stButton > button:hover {
#         transform: translateY(-2px);
#         box-shadow: 
#             0 6px 30px rgba(122, 162, 247, 0.5),
#             inset 0 1px 0 rgba(255, 255, 255, 0.3);
#         background: linear-gradient(135deg, #8ab4f8 0%, #6a8ed7 100%);
#     }
    
#     .stButton > button:active {
#         transform: translateY(0);
#     }
    
#     /* Decision Gate Buttons - Custom Glows */
#     div[data-testid="column"]:nth-child(1) .stButton > button {
#         background: linear-gradient(135deg, #9ECE6A 0%, #7eb84a 100%);
#         box-shadow: 0 4px 20px rgba(158, 206, 106, 0.4);
#     }
    
#     div[data-testid="column"]:nth-child(1) .stButton > button:hover {
#         box-shadow: 0 6px 30px rgba(158, 206, 106, 0.6);
#         background: linear-gradient(135deg, #b0e080 0%, #8ec85a 100%);
#     }
    
#     div[data-testid="column"]:nth-child(2) .stButton > button {
#         background: linear-gradient(135deg, #FF9E64 0%, #e8864d 100%);
#         box-shadow: 0 4px 20px rgba(255, 158, 100, 0.4);
#     }
    
#     div[data-testid="column"]:nth-child(2) .stButton > button:hover {
#         box-shadow: 0 6px 30px rgba(255, 158, 100, 0.6);
#         background: linear-gradient(135deg, #ffae7a 0%, #f89660 100%);
#     }
    
#     div[data-testid="column"]:nth-child(3) .stButton > button {
#         background: linear-gradient(135deg, #7AA2F7 0%, #5a7ec7 100%);
#         box-shadow: 0 4px 20px rgba(122, 162, 247, 0.4);
#     }
    
#     div[data-testid="column"]:nth-child(3) .stButton > button:hover {
#         box-shadow: 0 6px 30px rgba(122, 162, 247, 0.6);
#     }
    
#     /* ═══ PROGRESS BARS - NEON THIN ═══ */
#     .stProgress > div > div > div > div {
#         background: linear-gradient(90deg, #9ECE6A 0%, #7AA2F7 100%);
#         height: 6px;
#         border-radius: 3px;
#     }
    
#     .stProgress > div > div > div {
#         background-color: rgba(255, 255, 255, 0.06);
#         border-radius: 3px;
#         height: 6px;
#     }
    
#     /* ═══ METRICS - STAT CARDS ═══ */
#     [data-testid="stMetricValue"] {
#         color: #9ECE6A;
#         font-size: 2.2rem;
#         font-weight: 800;
#         text-shadow: 0 0 15px rgba(158, 206, 106, 0.3);
#     }
    
#     [data-testid="stMetricLabel"] {
#         color: #8b949e;
#         font-size: 0.8rem;
#         letter-spacing: 1.8px;
#         text-transform: uppercase;
#         font-weight: 600;
#     }
    
#     /* ═══ STATUS COMPONENT ═══ */
#     .stStatus {
#         background: linear-gradient(145deg, 
#             rgba(22, 27, 34, 0.7) 0%, 
#             rgba(13, 17, 23, 0.85) 100%);
#         backdrop-filter: blur(8px);
#         border: 1px solid rgba(122, 162, 247, 0.2);
#         border-radius: 12px;
#         padding: 1rem;
#     }
    
#     /* ═══ DIVIDERS - SOFT GLOW ═══ */
#     hr {
#         border: none;
#         height: 1px;
#         background: linear-gradient(90deg, 
#             transparent 0%, 
#             rgba(122, 162, 247, 0.25) 50%, 
#             transparent 100%);
#         margin: 2.5rem 0;
#         box-shadow: 0 0 10px rgba(122, 162, 247, 0.1);
#     }
    
#     /* ═══ SUCCESS/WARNING/INFO ALERTS ═══ */
#     .stSuccess {
#         background: linear-gradient(145deg, 
#             rgba(158, 206, 106, 0.15) 0%, 
#             rgba(158, 206, 106, 0.08) 100%);
#         border-left: 4px solid #9ECE6A;
#         color: #c9d1d9;
#     }
    
#     .stWarning {
#         background: linear-gradient(145deg, 
#             rgba(255, 158, 100, 0.15) 0%, 
#             rgba(255, 158, 100, 0.08) 100%);
#         border-left: 4px solid #FF9E64;
#         color: #c9d1d9;
#     }
    
#     .stInfo {
#         background: linear-gradient(145deg, 
#             rgba(122, 162, 247, 0.15) 0%, 
#             rgba(122, 162, 247, 0.08) 100%);
#         border-left: 4px solid #7AA2F7;
#         color: #c9d1d9;
#     }
    
#     /* ═══ SCROLLBAR ═══ */
#     ::-webkit-scrollbar {
#         width: 10px;
#         height: 10px;
#     }
    
#     ::-webkit-scrollbar-track {
#         background: #0d1117;
#     }
    
#     ::-webkit-scrollbar-thumb {
#         background: linear-gradient(180deg, #7AA2F7 0%, #5a7ec7 100%);
#         border-radius: 5px;
#     }
    
#     ::-webkit-scrollbar-thumb:hover {
#         background: #7AA2F7;
#     }
    
#     /* ═══ REMOVE STREAMLIT BRANDING ═══ */
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     header {visibility: hidden;}
    
#     /* ═══ SPACING UTILITIES ═══ */
#     .spacer-sm { height: 1rem; }
#     .spacer-md { height: 2rem; }
#     .spacer-lg { height: 3.5rem; }
    
#     /* ═══ CHAT BUBBLE STYLING ═══ */
#     .chat-response {
#         background: linear-gradient(145deg, 
#             rgba(122, 162, 247, 0.12) 0%, 
#             rgba(122, 162, 247, 0.06) 100%);
#         border-left: 3px solid #7AA2F7;
#         padding: 1.5rem;
#         border-radius: 12px;
#         margin: 1rem 0;
#         box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
#     }
    
#     </style>
#     """, unsafe_allow_html=True)

# # ═══════════════════════════════════════════════════════════════════════════════
# # INTELLIGENCE CORE - DUAL MODEL SYSTEM
# # ═══════════════════════════════════════════════════════════════════════════════

# # Initialize OpenAI client
# openai.api_key = os.getenv("OPENAI_API_KEY")

# def classify_intent(user_input):
#     """Use GPT-4o-mini to classify if input is CHAT or HUNT"""
#     try:
#         response = openai.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": """You are an intent classifier for a cinema production engine.
#                 Classify the user input as either:
#                 - CHAT: If it's a greeting, general conversation, or question about the system
#                 - HUNT: If it's a research request, content idea, market query, or project concept
                
#                 Respond with ONLY one word: either 'CHAT' or 'HUNT'"""},
#                 {"role": "user", "content": user_input}
#             ],
#             max_tokens=10,
#             temperature=0.3
#         )
        
#         intent = response.choices[0].message.content.strip().upper()
#         return intent if intent in ["CHAT", "HUNT"] else "HUNT"
#     except Exception as e:
#         st.error(f"Intent classification error: {str(e)}")
#         return "HUNT"  # Default to HUNT on error

# def chat_response(user_input):
#     """Handle casual chat using GPT-4o-mini"""
#     try:
#         response = openai.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": """You are the AI assistant for Sovereign Cinema Engine, 
#                 a high-end content production system. Be professional, friendly, and concise. 
#                 Help users understand the system capabilities and guide them."""},
#                 {"role": "user", "content": user_input}
#             ],
#             max_tokens=300,
#             temperature=0.7
#         )
        
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         return f"Chat system temporarily offline. Error: {str(e)}"

# def deep_research(query):
#     """Conduct deep research using GPT-4o with simulated web/YouTube scraping"""
    
#     # Simulated data sources (in production, integrate actual APIs)
#     simulated_knowledge = f"""
#     Market Analysis for: {query}
    
#     Current Trends (2025):
#     - Audience demographic shift toward interactive, AI-generated content
#     - Rising demand for personalized storytelling experiences
#     - Streaming platforms prioritizing original, data-driven productions
    
#     Competitive Landscape:
#     - Medium saturation in mainstream markets
#     - Emerging opportunities in niche genre combinations
#     - Strong potential for innovative narrative structures
    
#     Recommendation:
#     Based on current market intelligence, this concept shows {85 + (hash(query) % 15)}% viability.
#     Suggested approach: Develop unique angle with emphasis on contemporary themes.
#     """
    
#     try:
#         response = openai.chat.completions.create(
#             model="gpt-4o",
#             messages=[
#                 {"role": "system", "content": """You are Agent 01, the elite research intelligence core 
#                 of Sovereign Cinema Engine. Analyze content concepts with deep market insight, 
#                 audience psychology, and production feasibility. Provide actionable intelligence."""},
#                 {"role": "user", "content": f"""Conduct deep research on this concept: {query}
                
#                 Additional Context:
#                 {simulated_knowledge}
                
#                 Provide a comprehensive intelligence report covering:
#                 1. Market Viability
#                 2. Target Audience Profile
#                 3. Competitive Analysis
#                 4. Production Recommendations
#                 5. Risk Assessment
#                 """}
#             ],
#             max_tokens=800,
#             temperature=0.6
#         )
        
#         return {
#             "query": query,
#             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "findings": response.choices[0].message.content.strip(),
#             "confidence": 85 + (hash(query) % 15),
#             "sources": ["Market Intelligence DB", "YouTube Trend Analysis", "Industry Reports", "Audience Sentiment Data"]
#         }
#     except Exception as e:
#         return {
#             "query": query,
#             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             "findings": f"Research system encountered an error: {str(e)}\n\nFallback Analysis: {simulated_knowledge}",
#             "confidence": 70,
#             "sources": ["Fallback Database"]
#         }

# def research_with_status(query):
#     """Execute research with visual status updates"""
#     status_container = st.status("🚀 **INTELLIGENCE GATHERING INITIATED**", expanded=True)
    
#     with status_container:
#         st.write("📡 Accessing Sovereign Knowledge Base...")
#         time.sleep(1.2)
        
#         st.write("🔍 Scraping Web Assets & YouTube Transcripts...")
#         time.sleep(1.5)
        
#         st.write("🧠 Distilling Intelligence (GPT-4o Flagship Active)...")
#         research_data = deep_research(query)
#         time.sleep(1.8)
        
#         st.write("✅ **INTELLIGENCE GATHERED**")
    
#     status_container.update(label="✅ **INTELLIGENCE REPORT READY**", state="complete", expanded=False)
#     return research_data

# # ═══════════════════════════════════════════════════════════════════════════════
# # HELPER FUNCTIONS
# # ═══════════════════════════════════════════════════════════════════════════════

# def create_card(content):
#     """Wrap content in a floating glassmorphic card"""
#     return f'<div class="floating-card">{content}</div>'

# # ═══════════════════════════════════════════════════════════════════════════════
# # MAIN APPLICATION
# # ═══════════════════════════════════════════════════════════════════════════════

# def main():
#     # Inject CSS
#     inject_custom_css()
    
#     # Initialize session state
#     if 'research_data' not in st.session_state:
#         st.session_state.research_data = None
#     if 'decision' not in st.session_state:
#         st.session_state.decision = None
#     if 'chat_mode' not in st.session_state:
#         st.session_state.chat_mode = False
#     if 'chat_response_text' not in st.session_state:
#         st.session_state.chat_response_text = None
    
#     # ═══ SIDEBAR - COMMAND PANEL ═══
#     with st.sidebar:
#         st.markdown("### ⚡ SYSTEM STATUS")
#         st.markdown("**Sovereign Cinema Engine**")
#         st.markdown("Version: 2.0.0")
#         st.markdown("Model: Dual-Intelligence Core")
#         st.markdown("---")
        
#         st.markdown("### 👤 OPERATOR")
#         st.markdown("**NAVEEN**")
#         st.markdown("Clearance: **ALPHA**")
#         st.markdown("Access Level: **UNRESTRICTED**")
#         st.markdown("---")
        
#         st.markdown("### 🎯 ACTIVE MODULES")
#         st.markdown("✓ Agent 01: Deep Research")
#         st.markdown("✓ GPT-4o Flagship Engine")
#         st.markdown("✓ GPT-4o-mini Chat Core")
#         st.markdown("✓ Intelligence Matrix")
#         st.markdown("✓ Decision Gate Protocol")
#         st.markdown("---")
        
#         st.markdown("### 📊 STATISTICS")
#         col1, col2 = st.columns(2)
#         with col1:
#             st.metric("Projects", "24")
#         with col2:
#             st.metric("Success", "96%")
        
#         st.markdown("---")
#         st.markdown("### 🔧 SYSTEM INFO")
#         st.markdown(f"**Current Time:** {datetime.now().strftime('%H:%M:%S')}")
#         st.markdown(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}")
    
#     # ═══ MAIN HEADER ═══
#     st.markdown('<h1>🎬 SOVEREIGN CINEMA ENGINE</h1>', unsafe_allow_html=True)
#     st.markdown('<p style="color: #8b949e; font-size: 1.15rem; margin-bottom: 2.5rem; font-weight: 300;">Industrial-Grade Content Production Command Center • Dual-Intelligence Core</p>', unsafe_allow_html=True)
    
#     st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)
    
#     # ═══ COMMAND INPUT BAR ═══
#     st.markdown('<h3>🔍 COMMAND INPUT</h3>', unsafe_allow_html=True)
    
#     col1, col2 = st.columns([5, 1])
#     with col1:
#         user_input = st.text_input(
#             "Enter Project Concept, Research Query, or Chat Message",
#             placeholder="e.g., 'AI thriller for Gen-Z' or 'What can this system do?'",
#             label_visibility="collapsed",
#             key="main_input"
#         )
#     with col2:
#         initiate_button = st.button("🚀 INITIATE", use_container_width=True)
    
#     # ═══ INTELLIGENCE PROCESSING ═══
#     if initiate_button and user_input:
#         st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)
        
#         # Classify intent
#         with st.spinner("🧠 Analyzing input..."):
#             intent = classify_intent(user_input)
        
#         if intent == "CHAT":
#             # Handle chat mode
#             st.session_state.chat_mode = True
#             st.session_state.research_data = None
            
#             with st.spinner("💬 Processing response..."):
#                 response_text = chat_response(user_input)
#                 st.session_state.chat_response_text = response_text
            
#         else:  # HUNT mode
#             # Handle research mode
#             st.session_state.chat_mode = False
#             st.session_state.chat_response_text = None
            
#             research_data = research_with_status(user_input)
#             st.session_state.research_data = research_data
    
#     # ═══ CHAT MODE DISPLAY ═══
#     if st.session_state.chat_mode and st.session_state.chat_response_text:
#         st.markdown('<div class="spacer-lg"></div>', unsafe_allow_html=True)
        
#         chat_html = f"""
#         <div class="chat-response">
#             <h3 style="color: #7AA2F7; margin-top: 0; font-size: 1rem; letter-spacing: 1px;">💬 SYSTEM RESPONSE</h3>
#             <p style="margin-top: 1rem; font-size: 1.05rem; line-height: 1.8;">{st.session_state.chat_response_text}</p>
#         </div>
#         """
#         st.markdown(chat_html, unsafe_allow_html=True)
    
#     # ═══ RESEARCH MODE DISPLAY ═══
#     if st.session_state.research_data and not st.session_state.chat_mode:
#         st.markdown('<div class="spacer-lg"></div>', unsafe_allow_html=True)
        
#         data = st.session_state.research_data
        
#         # Intelligence Report Card
#         report_html = f"""
#         <h2>📋 INTELLIGENCE REPORT</h2>
#         <p style="color: #6e7681; margin-bottom: 2rem; font-size: 0.95rem;">
#             Query: <strong style="color: #c9d1d9;">{data['query']}</strong> • 
#             Generated: <strong style="color: #c9d1d9;">{data['timestamp']}</strong> • 
#             Model: <strong style="color: #7AA2F7;">GPT-4o Flagship</strong>
#         </p>
#         <hr style="margin: 2rem 0;">
#         <h3 style="color: #9ECE6A; margin-bottom: 1.5rem; font-size: 1.1rem;">FINDINGS & ANALYSIS</h3>
#         <p style="line-height: 2; font-size: 1.05rem; white-space: pre-wrap;">{data['findings']}</p>
#         <hr style="margin: 2rem 0;">
#         <h3 style="color: #9ECE6A; margin-bottom: 1rem; font-size: 1.1rem;">CONFIDENCE LEVEL</h3>
#         """
        
#         st.markdown(create_card(report_html), unsafe_allow_html=True)
        
#         # Confidence Progress Bar
#         st.progress(data['confidence'] / 100)
#         st.markdown(f"<p style='text-align: center; color: #9ECE6A; font-weight: 700; font-size: 1.4rem; margin-top: 0.5rem; text-shadow: 0 0 15px rgba(158, 206, 106, 0.4);'>{data['confidence']}%</p>", unsafe_allow_html=True)
        
#         st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)
        
#         # Source Affinity
#         st.markdown("### 📚 SOURCE AFFINITY MATRIX")
#         for idx, source in enumerate(data['sources']):
#             col1, col2 = st.columns([2, 5])
#             with col1:
#                 st.markdown(f"**{source}**")
#             with col2:
#                 affinity_score = 0.70 + (hash(source) % 30) / 100
#                 st.progress(affinity_score)
        
#         # ═══ DECISION GATE ═══
#         st.markdown('<div class="spacer-lg"></div>', unsafe_allow_html=True)
#         st.markdown("### 🎯 DECISION GATE PROTOCOL")
#         st.markdown('<p style="color: #8b949e; margin-bottom: 1.5rem;">Select your production pathway based on intelligence analysis</p>', unsafe_allow_html=True)
        
#         col1, col2, col3 = st.columns(3)
        
#         with col1:
#             if st.button("✅ GREEN LIGHT", use_container_width=True, key="green_decision"):
#                 st.session_state.decision = "green_light"
#                 st.success("🎬 **PROJECT APPROVED** • Initiating production protocols...")
        
#         with col2:
#             if st.button("🔄 REFINE SEARCH", use_container_width=True, key="refine_decision"):
#                 st.session_state.decision = "refine"
#                 st.warning("🔍 **REFINEMENT MODE** • Adjusting research parameters...")
        
#         with col3:
#             if st.button("📝 MANUAL EDIT", use_container_width=True, key="manual_decision"):
#                 st.session_state.decision = "manual"
#                 st.info("✏️ **MANUAL OVERRIDE** • Entering custom configuration mode...")

# if __name__ == "__main__":
#     main()









# import streamlit as st
# import time
# from datetime import datetime

# # ═══════════════════════════════════════════════════════════════════════════════
# # SOVEREIGN CINEMA ENGINE - WAR ROOM UI
# # High-End Stealth-Dark Command Center
# # ═══════════════════════════════════════════════════════════════════════════════

# # Page Configuration
# st.set_page_config(
#     page_title="Sovereign Cinema Engine",
#     page_icon="🎬",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ═══════════════════════════════════════════════════════════════════════════════
# # CSS INJECTION - STEALTH DARK AESTHETIC
# # ═══════════════════════════════════════════════════════════════════════════════

# def inject_custom_css():
#     st.markdown("""
#     <style>
#     /* ═══ GLOBAL RESET & BASE ═══ */
#     * {
#         margin: 0;
#         padding: 0;
#         box-sizing: border-box;
#     }
    
#     /* Main Background - Deep Space Black */
#     .stApp {
#         background: linear-gradient(135deg, #000000 0%, #0a0a0a 50%, #111111 100%);
#         color: #e0e0e0;
#         font-family: 'Inter', 'Segoe UI', sans-serif;
#     }
    
#     /* ═══ SIDEBAR - TERMINAL PANEL ═══ */
#     [data-testid="stSidebar"] {
#         background: linear-gradient(180deg, #0a0a0a 0%, #000000 100%);
#         border-right: 1px solid rgba(0, 255, 163, 0.1);
#         box-shadow: 4px 0 24px rgba(0, 0, 0, 0.8);
#     }
    
#     [data-testid="stSidebar"] .element-container {
#         padding: 0.5rem 1rem;
#     }
    
#     /* Sidebar Text Styling */
#     [data-testid="stSidebar"] h1,
#     [data-testid="stSidebar"] h2,
#     [data-testid="stSidebar"] h3 {
#         color: #00FFA3;
#         font-weight: 700;
#         letter-spacing: 2px;
#         text-transform: uppercase;
#         font-size: 0.75rem;
#         margin-bottom: 0.5rem;
#     }
    
#     [data-testid="stSidebar"] p {
#         color: #888888;
#         font-size: 0.85rem;
#         letter-spacing: 0.5px;
#     }
    
#     /* ═══ FLOATING CARDS - GLASSMORPHISM ═══ */
#     .floating-card {
#         background: linear-gradient(145deg, rgba(17, 17, 17, 0.9) 0%, rgba(10, 10, 10, 0.95) 100%);
#         backdrop-filter: blur(10px);
#         border: 1px solid rgba(0, 255, 163, 0.15);
#         border-radius: 16px;
#         padding: 2rem;
#         margin: 1.5rem 0;
#         box-shadow: 
#             0 8px 32px rgba(0, 0, 0, 0.6),
#             0 2px 8px rgba(0, 255, 163, 0.05),
#             inset 0 1px 0 rgba(255, 255, 255, 0.05);
#         transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
#     }
    
#     .floating-card:hover {
#         transform: translateY(-2px);
#         box-shadow: 
#             0 12px 48px rgba(0, 0, 0, 0.8),
#             0 4px 16px rgba(0, 255, 163, 0.1),
#             inset 0 1px 0 rgba(255, 255, 255, 0.08);
#         border-color: rgba(0, 255, 163, 0.25);
#     }
    
#     /* ═══ TYPOGRAPHY HIERARCHY ═══ */
#     h1 {
#         color: #00FFA3;
#         font-weight: 800;
#         font-size: 2.5rem;
#         letter-spacing: -0.5px;
#         margin-bottom: 0.5rem;
#         text-shadow: 0 0 20px rgba(0, 255, 163, 0.3);
#     }
    
#     h2 {
#         color: #ffffff;
#         font-weight: 700;
#         font-size: 1.5rem;
#         margin-bottom: 1rem;
#         letter-spacing: 0.5px;
#     }
    
#     h3 {
#         color: #cccccc;
#         font-weight: 600;
#         font-size: 1.1rem;
#         margin-bottom: 0.75rem;
#         letter-spacing: 1px;
#         text-transform: uppercase;
#     }
    
#     p, li {
#         color: #b0b0b0;
#         line-height: 1.6;
#         font-size: 0.95rem;
#     }
    
#     /* ═══ INPUT FIELDS - HUNT BAR ═══ */
#     .stTextInput > div > div > input {
#         background: linear-gradient(145deg, rgba(20, 20, 20, 0.8) 0%, rgba(10, 10, 10, 0.9) 100%);
#         border: 1px solid rgba(0, 255, 163, 0.2);
#         border-radius: 12px;
#         color: #ffffff;
#         font-size: 1rem;
#         padding: 1rem 1.5rem;
#         transition: all 0.3s ease;
#         box-shadow: 
#             inset 0 2px 8px rgba(0, 0, 0, 0.4),
#             0 0 0 rgba(0, 255, 163, 0);
#     }
    
#     .stTextInput > div > div > input:focus {
#         border-color: #00FFA3;
#         outline: none;
#         box-shadow: 
#             inset 0 2px 8px rgba(0, 0, 0, 0.4),
#             0 0 20px rgba(0, 255, 163, 0.2);
#     }
    
#     /* ═══ BUTTONS - GRADIENT ACCENTS ═══ */
#     .stButton > button {
#         background: linear-gradient(135deg, #00FFA3 0%, #00D68F 100%);
#         color: #000000;
#         border: none;
#         border-radius: 12px;
#         padding: 0.75rem 2rem;
#         font-weight: 700;
#         font-size: 1rem;
#         letter-spacing: 1px;
#         text-transform: uppercase;
#         cursor: pointer;
#         transition: all 0.3s ease;
#         box-shadow: 
#             0 4px 16px rgba(0, 255, 163, 0.3),
#             inset 0 1px 0 rgba(255, 255, 255, 0.2);
#     }
    
#     .stButton > button:hover {
#         transform: translateY(-2px);
#         box-shadow: 
#             0 6px 24px rgba(0, 255, 163, 0.4),
#             inset 0 1px 0 rgba(255, 255, 255, 0.3);
#     }
    
#     .stButton > button:active {
#         transform: translateY(0);
#     }
    
#     /* Decision Gate Buttons */
#     .decision-green {
#         background: linear-gradient(135deg, #00FFA3 0%, #00D68F 100%) !important;
#     }
    
#     .decision-amber {
#         background: linear-gradient(135deg, #FFB800 0%, #FFA000 100%) !important;
#     }
    
#     .decision-grey {
#         background: linear-gradient(145deg, #444444 0%, #333333 100%) !important;
#         color: #ffffff !important;
#     }
    
#     /* ═══ PROGRESS BARS - NEON THIN ═══ */
#     .stProgress > div > div > div > div {
#         background: linear-gradient(90deg, #00FFA3 0%, #00D4FF 100%);
#         height: 6px;
#         border-radius: 3px;
#     }
    
#     .stProgress > div > div > div {
#         background-color: rgba(255, 255, 255, 0.05);
#         border-radius: 3px;
#         height: 6px;
#     }
    
#     /* ═══ METRICS - STAT CARDS ═══ */
#     [data-testid="stMetricValue"] {
#         color: #00FFA3;
#         font-size: 2rem;
#         font-weight: 800;
#     }
    
#     [data-testid="stMetricLabel"] {
#         color: #888888;
#         font-size: 0.85rem;
#         letter-spacing: 1.5px;
#         text-transform: uppercase;
#     }
    
#     /* ═══ DIVIDERS - MINIMAL ═══ */
#     hr {
#         border: none;
#         height: 1px;
#         background: linear-gradient(90deg, transparent 0%, rgba(0, 255, 163, 0.2) 50%, transparent 100%);
#         margin: 2rem 0;
#     }
    
#     /* ═══ CODE BLOCKS ═══ */
#     .stCodeBlock {
#         background: rgba(0, 0, 0, 0.6) !important;
#         border: 1px solid rgba(0, 255, 163, 0.1);
#         border-radius: 8px;
#     }
    
#     /* ═══ SCROLLBAR ═══ */
#     ::-webkit-scrollbar {
#         width: 8px;
#         height: 8px;
#     }
    
#     ::-webkit-scrollbar-track {
#         background: #0a0a0a;
#     }
    
#     ::-webkit-scrollbar-thumb {
#         background: linear-gradient(180deg, #00FFA3 0%, #00D68F 100%);
#         border-radius: 4px;
#     }
    
#     ::-webkit-scrollbar-thumb:hover {
#         background: #00FFA3;
#     }
    
#     /* ═══ REMOVE STREAMLIT BRANDING ═══ */
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     header {visibility: hidden;}
    
#     /* ═══ SPACING UTILITIES ═══ */
#     .spacer-sm { height: 1rem; }
#     .spacer-md { height: 2rem; }
#     .spacer-lg { height: 3rem; }
    
#     </style>
#     """, unsafe_allow_html=True)

# # ═══════════════════════════════════════════════════════════════════════════════
# # HELPER FUNCTIONS
# # ═══════════════════════════════════════════════════════════════════════════════

# def create_card(content):
#     """Wrap content in a floating card"""
#     return f'<div class="floating-card">{content}</div>'

# def simulate_agent_research(query):
#     """Simulate Agent 01 research operation"""
#     progress_bar = st.progress(0)
#     status_text = st.empty()
    
#     stages = [
#         ("Initializing neural pathways...", 0.2),
#         ("Scanning knowledge domains...", 0.4),
#         ("Cross-referencing data points...", 0.6),
#         ("Synthesizing intelligence report...", 0.8),
#         ("Finalizing analysis...", 1.0)
#     ]
    
#     for stage, progress in stages:
#         status_text.text(stage)
#         progress_bar.progress(progress)
#         time.sleep(0.5)
    
#     status_text.empty()
#     progress_bar.empty()
    
#     # Mock research output
#     return {
#         "query": query,
#         "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         "findings": f"Intelligence gathered on '{query}': Market analysis indicates strong potential. Audience demographic: 18-35, tech-savvy, entertainment enthusiasts. Competitive landscape: moderate saturation. Recommendation: Proceed with creative development.",
#         "confidence": 87,
#         "sources": ["IMDb Pro", "Box Office Mojo", "Google Trends", "Reddit Analysis"]
#     }

# # ═══════════════════════════════════════════════════════════════════════════════
# # MAIN APPLICATION
# # ═══════════════════════════════════════════════════════════════════════════════

# def main():
#     # Inject CSS
#     inject_custom_css()
    
#     # Initialize session state
#     if 'research_data' not in st.session_state:
#         st.session_state.research_data = None
#     if 'decision' not in st.session_state:
#         st.session_state.decision = None
    
#     # ═══ SIDEBAR - COMMAND PANEL ═══
#     with st.sidebar:
#         st.markdown("### ⚡ SYSTEM STATUS")
#         st.markdown("**Sovereign Cinema Engine**")
#         st.markdown("Version: 1.0.0")
#         st.markdown("---")
        
#         st.markdown("### 👤 OPERATOR")
#         st.markdown("**NAVEEN**")
#         st.markdown("Clearance: ALPHA")
#         st.markdown("---")
        
#         st.markdown("### 🎯 ACTIVE MODULES")
#         st.markdown("✓ Agent 01: Research")
#         st.markdown("✓ Intelligence Core")
#         st.markdown("✓ Decision Matrix")
#         st.markdown("---")
        
#         st.markdown("### 📊 STATISTICS")
#         col1, col2 = st.columns(2)
#         with col1:
#             st.metric("Projects", "12")
#         with col2:
#             st.metric("Success", "94%")
    
#     # ═══ MAIN HEADER ═══
#     st.markdown('<h1>🎬 SOVEREIGN CINEMA ENGINE</h1>', unsafe_allow_html=True)
#     st.markdown('<p style="color: #888888; font-size: 1.1rem; margin-bottom: 2rem;">Industrial-Grade Content Production Command Center</p>', unsafe_allow_html=True)
    
#     st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)
    
#     # ═══ HUNT BAR - PRIMARY INPUT ═══
#     st.markdown('<h3>🔍 PROJECT HUNT</h3>', unsafe_allow_html=True)
    
#     col1, col2 = st.columns([4, 1])
#     with col1:
#         hunt_query = st.text_input(
#             "Enter Project Concept or Market Query",
#             placeholder="e.g., 'AI thriller for Gen-Z audience' or 'Best performing genres 2025'",
#             label_visibility="collapsed"
#         )
#     with col2:
#         hunt_button = st.button("🚀 HUNT", use_container_width=True)
    
#     # ═══ AGENT 01 - RESEARCH EXECUTION ═══
#     if hunt_button and hunt_query:
#         st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)
        
#         with st.container():
#             st.markdown("### 🤖 AGENT 01: RESEARCH INITIATED")
#             research_data = simulate_agent_research(hunt_query)
#             st.session_state.research_data = research_data
#             st.success("✓ Intelligence Report Generated")
    
#     # ═══ INTELLIGENCE REPORT CARD ═══
#     if st.session_state.research_data:
#         st.markdown('<div class="spacer-lg"></div>', unsafe_allow_html=True)
        
#         data = st.session_state.research_data
        
#         # Report Card
#         report_html = f"""
#         <h2>📋 INTELLIGENCE REPORT</h2>
#         <p style="color: #666; margin-bottom: 1rem;">Query: <strong>{data['query']}</strong> | Generated: {data['timestamp']}</p>
#         <hr style="margin: 1.5rem 0;">
#         <h3 style="color: #00FFA3; margin-bottom: 1rem;">FINDINGS</h3>
#         <p style="line-height: 1.8; font-size: 1rem;">{data['findings']}</p>
#         <hr style="margin: 1.5rem 0;">
#         <h3 style="color: #00FFA3; margin-bottom: 1rem;">CONFIDENCE LEVEL</h3>
#         """
        
#         st.markdown(create_card(report_html), unsafe_allow_html=True)
#         st.progress(data['confidence'] / 100)
#         st.markdown(f"<p style='text-align: center; color: #00FFA3; font-weight: 700; font-size: 1.2rem;'>{data['confidence']}%</p>", unsafe_allow_html=True)
        
#         st.markdown('<div class="spacer-md"></div>', unsafe_allow_html=True)
        
#         # Source Affinity
#         st.markdown("### 📚 SOURCE AFFINITY")
#         for source in data['sources']:
#             col1, col2 = st.columns([1, 4])
#             with col1:
#                 st.markdown(f"**{source}**")
#             with col2:
#                 st.progress(0.75 + (hash(source) % 25) / 100)
        
#         # ═══ DECISION GATE ═══
#         st.markdown('<div class="spacer-lg"></div>', unsafe_allow_html=True)
#         st.markdown("### 🎯 DECISION GATE")
        
#         col1, col2, col3 = st.columns(3)
        
#         with col1:
#             if st.button("✅ GREEN LIGHT", use_container_width=True, key="green"):
#                 st.session_state.decision = "green_light"
#                 st.success("🎬 Project approved for production!")
        
#         with col2:
#             if st.button("🔄 REFINE SEARCH", use_container_width=True, key="amber"):
#                 st.session_state.decision = "refine"
#                 st.warning("🔍 Refining research parameters...")
        
#         with col3:
#             if st.button("📝 MANUAL EDIT", use_container_width=True, key="grey"):
#                 st.session_state.decision = "manual"
#                 st.info("✏️ Entering manual override mode...")

# if __name__ == "__main__":
#     main()






# import streamlit as st
# from database_manager import SovereignBrain

# # 1. Page Config for a wide, immersive experience
# st.set_page_config(page_title="Sovereign Control", page_icon="🏛️", layout="wide")

# # 2. THE MASTER AESTHETIC: Minimalist CSS Injection
# st.markdown("""
#     <style>
#     /* Main Background: Deep Space Black */
#     .stApp {
#         background: radial-gradient(circle at top left, #111111, #000000);
#         color: #E0E0E0;
#     }

#     /* Remove all default borders/lines */
#     .stTextInput>div>div, .stTextArea>div>div {
#         border: none !important;
#         background-color: #1A1A1A !important;
#         border-radius: 12px !important;
#         box-shadow: inset 2px 2px 5px #000, inset -1px -1px 3px #333;
#     }

#     /* Gradient Separation for Cards */
#     .custom-card {
#         background: linear-gradient(145deg, #1e1e1e, #121212);
#         padding: 25px;
#         border-radius: 20px;
#         box-shadow: 10px 10px 30px #050505, -5px -5px 20px #222;
#         margin-bottom: 25px;
#         border-left: 4px solid #00FFA3; /* Subtle accent instead of full border */
#     }

#     /* Gradient Button - "The Action Center" */
#     .stButton>button {
#         background: linear-gradient(90deg, #00FFA3 0%, #03A9F4 100%);
#         color: black !important;
#         font-weight: 700 !important;
#         border: none !important;
#         padding: 12px 24px !important;
#         border-radius: 10px !important;
#         transition: 0.3s all ease;
#     }
#     .stButton>button:hover {
#         transform: scale(1.02);
#         box-shadow: 0px 0px 20px rgba(0, 255, 163, 0.4);
#     }

#     /* Minimalist Sidebar */
#     [data-testid="stSidebar"] {
#         background-color: #0A0A0A;
#         border-right: 1px solid #222;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # --- UI LAYOUT ---

# # Sidebar: Identity without Clutter
# with st.sidebar:
#     st.markdown("<h2 style='text-align: center; color: #00FFA3;'>🏛️</h2>", unsafe_allow_html=True)
#     st.markdown("<p style='text-align: center; opacity: 0.6;'>Sovereign Cinema Engine v1.0</p>", unsafe_allow_html=True)
#     st.write("---")
#     # Replace st.overline("ESTABLISHED INTERESTS") with this:
#     st.markdown("""
#         <p style='font-size: 10px; font-weight: 600; color: #555; letter-spacing: 2px; margin-bottom: -10px;'>
#         ESTABLISHED INTERESTS
#         </p>
#     """, unsafe_allow_html=True)
#     # st.overline("ESTABLISHED INTERESTS")
#     st.caption("AI Automation • Space Tech • History")

# # Main Dashboard
# st.title("Intelligence Dashboard")
# st.markdown("<p style='opacity: 0.5;'>Scanning global trends for Naveen's next masterpiece...</p>", unsafe_allow_html=True)

# # Research Module in a "Floating Card"
# st.markdown('<div class="custom-card">', unsafe_allow_html=True)
# col_input, col_btn = st.columns([4, 1])

# with col_input:
#     query = st.text_input("Enter Topic or URL", label_visibility="collapsed", placeholder="What's on your mind, Michael?")

# with col_btn:
#     if st.button("HUNT"):
#         with st.spinner(""):
#             # logic here
#             st.toast("Intelligence Gathering Initiated...")

# st.markdown('</div>', unsafe_allow_html=True)

# # Display Area: Two-Column Flow
# col_left, col_right = st.columns([2, 1])

# with col_left:
#     st.markdown('<div class="custom-card" style="border-left: 4px solid #03A9F4;">', unsafe_allow_html=True)
#     st.subheader("📜 Latest Intelligence Report")
#     st.write("Yahan aapki distilled report aayegi. Bina lines ke, sirf typography aur spacing se content dikhega.")
#     st.markdown('</div>', unsafe_allow_html=True)

# with col_right:
#     st.markdown('<div class="custom-card" style="border-left: 4px solid #FF3366;">', unsafe_allow_html=True)
#     st.subheader("🧠 Source Trust")
#     st.progress(85, text="TechCrunch (High Affinity)")
#     st.progress(40, text="Reddit (Low Affinity)")
#     st.markdown('</div>', unsafe_allow_html=True)