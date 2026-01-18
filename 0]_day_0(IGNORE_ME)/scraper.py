import modal

# 1. Image with OpenAI support
image = (
    modal.Image.debian_slim()
    .pip_install("crawl4ai", "playwright", "openai")
    .run_commands("playwright install --with-deps chromium")
)

app = modal.App("content-empire", image=image)

# 2. The Scraper (Our Sensor)
@app.function()
async def get_raw_data(url: str):
    from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
    async with AsyncWebCrawler() as crawler:
        config = CrawlerRunConfig(word_count_threshold=200)
        result = await crawler.arun(url=url, config=config)
        return result.markdown.raw_markdown[:3000] # Get more context for the AI

# 3. The AI Brain (Our Narrative Architect)
# Humne 'secrets' add kiya hai taaki API key safe rahe
@app.function(secrets=[modal.Secret.from_name("my-openai-secret")])
def generate_youtube_script(research_material: str):
    from openai import OpenAI
    client = OpenAI()
    
    # SYSTEM PROMPT: Setting the personality
    system_instruction = "You are a cynical, high-IQ health researcher who turns complex data into viral Hinglish YouTube Shorts. You NEVER hallucinate facts."
    
    # USER PROMPT: Strict instructions
    user_prompt = f"""
    STRICT RESEARCH MATERIAL: {research_material}
    
    TASK:
    1. Verify if the research is about 'Intermittent Fasting'. If not, stop.
    2. Create a 60-sec script. 
    3. Use 'Red-Teaming': Mention one common fasting myth and debunk it using the data.
    4. Tone: Hard-hitting, no fluff.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o", # Using the more powerful model for better logic
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2 # Lower temperature = less 'creativity', more 'accuracy'
    )
    return response.choices[0].message.content
# @app.function(secrets=[modal.Secret.from_name("my-openai-secret")])
# def generate_youtube_script(research_material: str):
#     from openai import OpenAI
#     client = OpenAI()
    
#     prompt = f"""
#     You are a viral YouTube script writer for an Indian audience.
#     Analyze this foreign health research: {research_material}
    
#     Create a 60-second YouTube Short script in 'Hinglish'.
#     Structure:
#     1. Hook: Start with a shocking fact or myth.
#     2. Body: Explain the 'Alpha' (the new knowledge).
#     3. Call to Action: Ask them to subscribe for more 'Sovereign' health tips.
    
#     Make it punchy, cynical, and high-energy.
#     """
    
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": prompt}]
#     )
#     return response.choices[0].message.content

# 4. The Orchestrator (The Boss)
@app.local_entrypoint()
def main():
    target_url = "https://www.healthline.com/nutrition/intermittent-fasting-guide"
    
    print("🚀 Step 1: Mining Global Alpha...")
    research = get_raw_data.remote(target_url)
    
    print("🧠 Step 2: Processing with AI Brain...")
    script = generate_youtube_script.remote(research)
    
    print("\n--- YOUR VIRAL YOUTUBE SCRIPT ---")
    print(script)




# import modal

# # Step 1: The "Fortress" Environment
# # Humne 'apt_install' aur '--with-deps' add kiya hai taaki Linux libraries mil jayein.
# image = (
#     modal.Image.debian_slim()
#     .pip_install("crawl4ai", "playwright")
#     .run_commands("playwright install --with-deps chromium") 
# )

# app = modal.App("signal-miner", image=image)

# # Step 2: The Async Cloud Function
# # @app.function()
# # async def get_global_insight(url: str):
# #     from crawl4ai import AsyncWebCrawler 
    
# #     async with AsyncWebCrawler() as crawler:
# #         print(f"Sensing signals from: {url}")
# #         result = await crawler.arun(url=url)
# #         return result.markdown[:1000]

# @app.function()
# async def get_global_insight(url: str):
#     from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
#     from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
    
#     async with AsyncWebCrawler() as crawler:
#         # We add a 'Config' to filter out the noise
#         config = CrawlerRunConfig(
#             word_count_threshold=200, # Ignore tiny blocks of text (like menus)
#             exclude_external_links=True,
#             remove_overlay_elements=True, # Remove pop-ups
#             process_iframes=False
#         )
        
#         print(f"Sensing Article Content from: {url}")
#         result = await crawler.arun(url=url, config=config)
        
        
#         # This will return the actual article text without the menu 'Noise'
#         # return result.markdown_v2.raw_markdown[:2000]
#         clean_text = result.markdown.raw_markdown
#         return clean_text[:2000] # Sending first 2000 characters for testing

# # Step 3: The Remote Control
# @app.local_entrypoint()
# def main():
#     target_url = "https://www.healthline.com/nutrition/how-to-start-working-out" 
#     insight = get_global_insight.remote(target_url)
    
#     print("\n--- GLOBAL SIGNAL EXTRACTED ---")
#     print(insight)