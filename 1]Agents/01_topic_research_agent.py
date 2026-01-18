import os
import json
from datetime import datetime
from openai import OpenAI
from duckduckgo_search import DDGS  # Ye hai Agent ki aankhein

# ════════════════════════════════════════════════════════════════════════════
# AGENT 01: THE RESEARCHER
# ════════════════════════════════════════════════════════════════════════════

class SovereignAgent:
    def __init__(self):
        # OpenAI Client Setup
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("⚠️ OpenAI API Key missing! Export kariye terminal mein.")
        
        self.client = OpenAI(api_key=api_key)
        self.ddgs = DDGS() # Search Engine
        
        # Models
        self.FAST_MODEL = "gpt-4o-mini" # For chat & quick decisions
        self.SMART_MODEL = "gpt-4o"     # For deep analysis

    def classify_intent(self, user_input):
        """
        Decide karega: Kya ye normal baat hai (CHAT) ya kaam ki baat (HUNT)?
        """
        try:
            response = self.client.chat.completions.create(
                model=self.FAST_MODEL,
                messages=[
                    {"role": "system", "content": "You are a classifier. If user input is a casual greeting or question, output 'CHAT'. If it is a topic for research/creation, output 'HUNT'. Output ONLY one word."},
                    {"role": "user", "content": user_input}
                ],
                temperature=0
            )
            return response.choices[0].message.content.strip().upper()
        except Exception as e:
            return "HUNT" # Agar fail hua, toh default Hunt samjho

    def chat_mode(self, user_input):
        """
        User ke saath casual baat cheet (Cheap Model)
        """
        response = self.client.chat.completions.create(
            model=self.FAST_MODEL,
            messages=[
                {"role": "system", "content": "You are Naveen's 'Sovereign AI'. You are loyal, sharp, and speak in professional Hinglish. Keep replies short and punchy."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content

    def hunt_mode(self, topic):
        """
        ASLI KAAM: Internet search + AI Analysis
        """
        print(f"🕵️ Agent 01 searching for: {topic}...")
        
        # 1. Search the Web (Real-time)
        search_results = []
        try:
            # DuckDuckGo se top 5 results nikalo
            results = self.ddgs.text(topic, max_results=5)
            for r in results:
                search_results.append(f"Title: {r['title']}\nLink: {r['href']}\nSnippet: {r['body']}")
        except Exception as e:
            return f"❌ Search Error: {str(e)}"

        raw_data = "\n\n".join(search_results)
        
        # 2. Distill Intelligence (GPT-4o)
        print("🧠 Distilling Intelligence...")
        
        prompt = f"""
        You are the Chief Intelligence Officer. Analyze these raw search results for the topic: '{topic}'.
        
        RAW DATA:
        {raw_data}
        
        Output a 'Sovereign Intelligence Report' in Markdown format:
        1. **Executive Summary**: 2 lines max.
        2. **Key Findings**: 3-4 bullet points of the most important facts.
        3. **Viral Angles**: 2 ideas on how to frame this for content/video.
        4. **Source Credibility**: Which source looked most promising?
        """
        
        response = self.client.chat.completions.create(
            model=self.SMART_MODEL,
            messages=[
                {"role": "system", "content": "You are an elite research analyst."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content

# ════════════════════════════════════════════════════════════════════════════
# TESTING AREA (Jab aap is file ko direct run karoge)
# ════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # Agent ko initialize karo
    agent = SovereignAgent()
    
    print("\n🦅 SOVEREIGN AGENT 01 ONLINE\n")
    
    while True:
        user_in = input(">> You: ")
        if user_in.lower() in ['exit', 'quit']:
            break
            
        # Step 1: Intent check
        intent = agent.classify_intent(user_in)
        print(f"[System Intent: {intent}]")
        
        if intent == "CHAT":
            reply = agent.chat_mode(user_in)
            print(f"🦅 Agent: {reply}\n")
        else:
            print("🚀 Initiating Deep Research...")
            report = agent.hunt_mode(user_in)
            print("\n" + "="*40)
            print(report)
            print("="*40 + "\n")