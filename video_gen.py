import os
import requests
from openai import OpenAI
from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_script(topic: str) -> dict:
    """Uses OpenAI to generate a short 30-second script for a TikTok/Reel."""
    print(f"Generating script for topic: {topic}")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a viral TikTok scriptwriter. Write a 30 second educational script."},
            {"role": "user", "content": f"Topic: {topic}. Output ONLY valid JSON: {{'title': '...', 'scenes': [{'image_prompt': '...', 'narration': '...', 'duration': 5}]}}"}
        ],
        response_format={"type": "json_object"}
    )
    import json
    return json.loads(response.choices[0].message.content)

def generate_audio(text: str, filename: str):
    """Uses OpenAI TTS to generate voiceover."""
    print(f"Generating audio: {filename}")
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    response.stream_to_file(filename)
    return filename

def generate_image(prompt: str, filename: str):
    """Uses DALL-E 3 to generate scene images."""
    print(f"Generating image: {filename}")
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt + " vertical format, highly detailed, photorealistic",
        size="1024x1792",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    img_data = requests.get(image_url).content
    with open(filename, 'wb') as handler:
        handler.write(img_data)
    return filename

def build_video(script_data: dict, output_filename: str):
    """Assembles the video using MoviePy."""
    print("Building video...")
    clips = []
    
    for i, scene in enumerate(script_data["scenes"]):
        img_file = f"scene_{i}.png"
        audio_file = f"scene_{i}.mp3"
        
        # 1. Generate Assets
        generate_image(scene["image_prompt"], img_file)
        generate_audio(scene["narration"], audio_file)
        
        # 2. Create MoviePy Clips
        audio_clip = AudioFileClip(audio_file)
        # Duration is determined by the audio length
        duration = audio_clip.duration
        
        image_clip = ImageClip(img_file).set_duration(duration)
        
        # Add subtitles (basic implementation)
        txt_clip = TextClip(scene["narration"], fontsize=50, color='white', 
                            method='caption', size=(900, None), align='center')
        txt_clip = txt_clip.set_pos(('center', 'bottom')).set_duration(duration)
        
        video = CompositeVideoClip([image_clip, txt_clip]).set_audio(audio_clip)
        clips.append(video)
        
    final_video = concatenate_videoclips(clips)
    final_video.write_videofile(output_filename, fps=24, codec="libx264", audio_codec="aac")
    print(f"Video saved as {output_filename}")

if __name__ == "__main__":
    topic = "How AI is changing Data Engineering"
    script = generate_script(topic)
    build_video(script, "ai_data_engineering_short.mp4")
