import requests
import os
from dotenv import load_dotenv
load_dotenv()


def cartesia_text_to_speech(text):
    url = os.getenv("CARTESIA_API_URL")
    
    headers = {
        "Cartesia-Version": "2024-06-10",
        "X-API-Key": os.getenv("CARTESIA_API_KEY", ""),
        "Content-Type": "application/json"
    }
    
    payload = {
        "model_id": "sonic-2",
        "transcript": text,
        "voice": {
            "mode": "id",
            "id": "bf0a246a-8642-498a-9950-80c35e9276b5"
        },
        "output_format": {
            "container": "wav",
            "encoding": "pcm_f32le",
            "sample_rate": 44100
        },
        "language": "en"
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        output_file = "output.wav"
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"Audio saved as {output_file}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

# Example usage:
cartesia_text_to_speech("Hello, My name is Akshat Jain & I am a AI engineer at Coforge.")
