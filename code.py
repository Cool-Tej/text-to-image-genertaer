import requests
import os
from dotenv import load_dotenv
import time
load_dotenv()
API_KEY = os.getenv("MONSTER_API_KEY")  

def generate_image(prompt, model="sdxl-base", negative_prompt="", steps=30):
    """
    Generate an image using Monster API.
    
    Args:
        prompt (str): Text description of the image.
        model (str): Model ID (e.g., "sdxl-base", "sd-v1.5").
        negative_prompt (str): What to exclude from the image.
        steps (int): Number of diffusion steps (quality vs. speed tradeoff).
    
    Returns:
        str: URL of the generated image.
    """
    url = "https://api.monsterapi.ai/v1/generate/txt2img"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "steps": steps,
        "width": 512,
        "height": 512
    }
    
    # Send request
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # Raise error if API call fails
    
    # Get process ID
    process_id = response.json().get("process_id")
    print(f"Generation started. Process ID: {process_id}")
    
    # Poll for result (Monster API is async)
    result_url = f"https://api.monsterapi.ai/v1/status/{process_id}"
    while True:
        time.sleep(5)  
        status_response = requests.get(result_url, headers=headers)
        status_data = status_response.json()
        
        if status_data.get("status") == "COMPLETED":
            return status_data["result"]["output"][0]  # Image URL
        elif status_data.get("status") == "FAILED":
            raise Exception("Image generation failed.")

# Example usage
if __name__ == "__main__":
    prompt = "A futuristic cityscape at sunset, cyberpunk style, 4K detailed"
    negative_prompt = "blurry, low quality"
    
    try:
        image_url = generate_image(prompt, negative_prompt=negative_prompt)
        print(f"Image generated! Download URL: {image_url}")
    except Exception as e:
        print(f"Error: {e}")
