import modal
import os

# 1. Setup Environment
image = (
    modal.Image.debian_slim()
    .pip_install("youtube-transcript-api>=1.2.0", "openai", "elevenlabs")
)
app = modal.App("sovereign-content-factory", image=image)

# --- CLOUD AGENTS ---


def get_transcript(video_id: str):
    from youtube_transcript_api import YouTubeTranscriptApi
    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)
        return " ".join([t.text for t in transcript])
    except Exception as e:
        return f"Error: {e}"

@app.function(secrets=[modal.Secret.from_name("my-openai-secret")])
def analyze_intelligence(transcript: str):
    from openai import OpenAI
    client = OpenAI()
    prompt = f"Analyze this transcript. Provide CATEGORY, 2-sentence SUMMARY, and key ALPHA points:\n\n{transcript[:6000]}"
    res = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
    return res.choices[0].message.content


@app.function(secrets=[modal.Secret.from_name("my-openai-secret")])
def generate_refined_script(context: str, prev_script: str = "", feedback: str = ""):
    from openai import OpenAI
    client = OpenAI()
    
    system_msg = "You are a world-class Hinglish YouTube script writer. You refine scripts based on research and user feedback."
    
    if not prev_script:
        user_msg = f"RESEARCH MATERIAL: {context}\n\nTASK: Create a 60s viral Hinglish script."
    else:
        user_msg = f"RESEARCH: {context}\n\nPREVIOUS DRAFT: {prev_script}\n\nUSER FEEDBACK: {feedback}\n\nTASK: Improve the previous draft based on the feedback."

    res = client.chat.completions.create(
        model="gpt-4o", 
        messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": user_msg}],
        temperature=0.7
    )
    return res.choices[0].message.content

@app.function(secrets=[modal.Secret.from_name("my-openai-secret")])
def generate_director_storyboard(script_text: str):
    from openai import OpenAI
    client = OpenAI()
    
    prompt = f"""
    You are a world-class YouTube Director and Cinematographer. 
    Analyze the following script and provide a scene-by-scene B-Roll storyboard.
    For each scene, provide:
    1. TIMING (e.g., 0-5s)
    2. VISUAL DESCRIPTION (Detailed prompt for stock footage or AI video generation)
    3. ON-SCREEN TEXT (Any captions that should appear)

    SCRIPT:
    {script_text}
    """
    
    res = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content

@app.function(secrets=[modal.Secret.from_name("my-openai-secret")])
def generate_image(prompt: str):
    from openai import OpenAI
    import requests
    client = OpenAI()
    
    print(f"🎨 Generating image for: {prompt[:50]}...")
    
    # DALL-E 3 use kar rahe hain for high quality
    response = client.images.generate(
        model="dall-e-3",
        prompt=f"Cinematic, high-quality, professional photography, 4k: {prompt}",
        size="1024x1024", # 1792x1024 landscape ke liye best hai
        quality="hd",
        n=1,
    )
    
    image_url = response.data[0].url
    # Image data download karke return karenge
    return requests.get(image_url).content

@app.function(secrets=[modal.Secret.from_name("my-openai-secret")])
def parse_prompts_from_storyboard(storyboard_text: str):
    from openai import OpenAI
    import json
    client = OpenAI()
    
    prompt = f"""
    Extract only the 'VISUAL DESCRIPTION' parts from this storyboard and return them as a JSON object with a "prompts" key containing an array of strings.
    Each prompt should be a standalone descriptive sentence for an image generator.
    
    Return format must be exactly:
    {{
        "prompts": ["description 1", "description 2", "description 3", ...]
    }}
    
    STORYBOARD:
    {storyboard_text}
    """
    
    res = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    try:
        response_json = json.loads(res.choices[0].message.content)
        # Try to get prompts from the response
        if "prompts" in response_json:
            return response_json["prompts"]
        # Fallback: if the response is just an array, use it directly
        elif isinstance(response_json, list):
            return response_json
        # Fallback: check for other possible keys
        else:
            # Print what we got for debugging
            print(f"⚠️ Unexpected JSON structure: {list(response_json.keys())}")
            # Try common alternative keys
            for key in ["visual_descriptions", "descriptions", "images", "scenes"]:
                if key in response_json:
                    return response_json[key]
            raise KeyError(f"Could not find 'prompts' key in response. Available keys: {list(response_json.keys())}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON response: {e}\nResponse: {res.choices[0].message.content}")

# --- HELPERS ---
def extract_id(url_or_id):
    if "v=" in url_or_id:
        return url_or_id.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url_or_id:
        return url_or_id.split("youtu.be/")[1].split("?")[0]
    return url_or_id

# def generate_voiceover(script_text: str, filename: str):
#     from elevenlabs.client import ElevenLabs
#     # Load .env file only when running locally
#     try:
#         from dotenv import load_dotenv
#         load_dotenv()
#     except ImportError:
#         pass  # dotenv not needed in Modal container
    
#     # Get API key from .env file
#     api_key = os.getenv("ELEVENLABS_API_KEY")
#     if not api_key:
#         raise ValueError("ELEVENLABS_API_KEY not found in .env file. Please add ELEVENLABS_API_KEY=your-key to your .env file")
    
#     client = ElevenLabs(api_key=api_key)
    
#     print(f"🎙 Generating Desi Accent Audio via ElevenLabs...")
    
#     # Use text_to_speech.convert() method
#     # Adam voice ID: pNInz6obpgDQGcFmaJgB
#     audio = client.text_to_speech.convert(
#         voice_id="pNInz6obpgDQGcFmaJgB",  # Adam voice
#         text=script_text,
#         model_id="eleven_multilingual_v2"
#     )
    
#     # Save audio bytes to file
#     with open(filename, "wb") as f:
#         for chunk in audio:
#             f.write(chunk)
    
#     print(f"✅ Audio saved locally: {filename}")
# def generate_voiceover(script_text: str, filename: str):
#     from elevenlabs import generate, save, set_api_key
#     import os
    
#     # Apni ElevenLabs API Key yahan dalo ya environment variable se lo
#     # set_api_key("YOUR_ELEVENLABS_API_KEY") 
    
#     print(f"🎙 Generating Desi Accent Audio via ElevenLabs (Local IP)...")
    
#     # 'multilingual_v2' is the key for natural Hindi/Hinglish accent
#     audio = generate(
#         text=script_text,
#         voice="Adam", # "Adam" or "Antoni" are great for this vibe
#         model="eleven_multilingual_v2" 
#     )
    
#     save(audio, filename)
#     print(f"✅ Audio saved locally: {filename}")
@app.function(secrets=[modal.Secret.from_name("my-openai-secret")])
def generate_voiceover(script_text: str):
    from openai import OpenAI
    
    client = OpenAI()
    print("🎙 Generating high-quality audio via OpenAI TTS...")

    # Using the 'tts-1' model for low latency (high speed)
    # Voice 'shimmer' is great for energetic content
    # Other options: 'onyx' (authoritative/deep), 'nova' (high-energy)
    response = client.audio.speech.create(
        model="tts-1",
        voice="shimmer", 
        input=script_text
    )
    
    # Returning the raw audio bytes
    return response.content
# --- LOCAL ENTRYPOINT ---
@app.local_entrypoint()
def main(target: str = "https://www.youtube.com/watch?v=Si7gpFVpbXc&list=LL&index=4"): # 'target' ab CLI argument ban gaya hai
    
    video_id = extract_id(target)
    print(f"🎬 Processing Video ID: {video_id}")
    
    # Step 1: Intelligence
    print("\n⚙️  Mining Intelligence...")
    raw_text = get_transcript(video_id)
    
    if "Error" in raw_text:
        print(f"❌ {raw_text}")
        return
    
    report = analyze_intelligence.remote(raw_text)
    print(f"\n--- 📊 VIDEO INTELLIGENCE ---\n{report}")

    # Step 2: Iterative Scripting (Hamesha loop chalayenge)
    folder_name = f"history_{video_id}"
    if not os.path.exists(folder_name): os.makedirs(folder_name)
    
    current_script = ""
    user_feedback = ""
    version = 1
    
    while True:
        print(f"\n✍️  Drafting Version {version}...")
        current_script = generate_refined_script.remote(report, current_script, user_feedback)
        
        # Save locally
        with open(f"{folder_name}/v{version}.txt", "w") as f:
            f.write(current_script)
        
        print(f"\n--- 📝 SCRIPT v{version} ---\n{current_script}")
        print(f"📁 (Auto-saved to {folder_name}/v{version}.txt)")
        
        # Feedback loop (Sirf yahan input use karenge, main process ke baad)
        review = input("\n🤔 Satisfied? (y = Approve / n = Provide Feedback): ").lower()
        
        if review == 'y':
            print(f"✅ Final Script Approved!")
            voice_choice = input("\n🔊 Generate AI Voiceover for this script? (y/n): ").lower()
            if voice_choice == 'y':
                print("⏳ Cooking your audio on the cloud...")
                
                # 1. Cloud function call (.remote use karein)
                audio_bytes = generate_voiceover.remote(current_script)
                
                # 2. Local save
                audio_filename = f"{folder_name}/voiceover_v{version}.mp3"
                with open(audio_filename, "wb") as f:
                    f.write(audio_bytes)
                    
                print(f"✅ OpenAI Audio saved: {audio_filename}")
            # # NEW STEP: Voiceover
            # voice_choice = input("\n🔊 Generate AI Voiceover for this script? (y/n): ").lower()
            # if voice_choice == 'y':
            #     audio_filename = f"{folder_name}/voiceover_v{version}.mp3"
            #     generate_voiceover(current_script, audio_filename)
            #     print(f"🎵 Audio saved successfully at: {audio_filename}")
            break

            
        else:
            user_feedback = input("💡 What should I change?: ")
            version += 1

    # . audio generation ke baad ...
    print("\n🎬 Director is storyboarding the visuals...")
    storyboard = generate_director_storyboard.remote(current_script)
    
    # Save Storyboard
    with open(f"{folder_name}/storyboard_v{version}.txt", "w") as f:
        f.write(storyboard)
    
    print(f"\n--- 🎞 VISUAL STORYBOARD ---\n{storyboard}")
    print(f"📁 Storyboard saved to {folder_name}/storyboard_v{version}.txt")

# ... Storyboard generation ke baad ...
    generate_pics = input("\n🖼 Generate AI images for all scenes? (y/n): ").lower()
    if generate_pics == 'y':
        print("🧠 Extracting prompts...")
        prompt_list = parse_prompts_from_storyboard.remote(storyboard)
        
        # Create a folder for images
        img_folder = f"{folder_name}/scenes"
        if not os.path.exists(img_folder): os.makedirs(img_folder)
        
        for i, p in enumerate(prompt_list):
            img_bytes = generate_image.remote(p)
            with open(f"{img_folder}/scene_{i+1}.png", "wb") as f:
                f.write(img_bytes)
            print(f"✅ Saved scene_{i+1}.png")


    print("\n👋 Mission Complete. All versions saved.")



