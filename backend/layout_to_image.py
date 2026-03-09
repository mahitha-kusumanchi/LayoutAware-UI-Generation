import torch
from diffusers import StableDiffusionPipeline
from PIL import Image, ImageDraw
import json
import os

def visualize_layout(layout_json, size=(512, 512)):
    """
    Draws bounding boxes from layout JSON onto a blank image.
    """
    if isinstance(layout_json, str):
        data = json.loads(layout_json)
    else:
        data = layout_json
        
    img = Image.new('RGB', size, color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    objects = data.get("objects", [])
    for obj in objects:
        label = obj.get("label", "unknown")
        bbox = obj.get("bbox", [0, 0, 0, 0])
        x, y, w, h = bbox
        
        # Draw rectangle
        draw.rectangle([x, y, x + w, y + h], outline="red", width=3)
        # Draw label
        draw.text((x, y - 10), label, fill="red")
        
    return img

import requests
import io

def generate_image_api(prompt, api_key, model_id="runwayml/stable-diffusion-v1-5", output_path="outputs/generated_image.png"):
    """
    Generates an image from a prompt using Hugging Face Inference API.
    """
    API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {"Authorization": f"Bearer {api_key}"}

    print(f"Calling Hugging Face API for model {model_id}...")
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        
        if response.status_code != 200:
            raise Exception(f"API Error: {response.text}")
            
        image_bytes = response.content
        image = Image.open(io.BytesIO(image_bytes))
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        image.save(output_path)
        
        return image
    except Exception as e:
        print(f"Error in generate_image_api: {e}")
        raise e

def generate_image(prompt, model_id="runwayml/stable-diffusion-v1-5", device=None, output_path="outputs/generated_image.png"):
    # (Existing local function preserved for Colab/Local GPU users)
    # Note: Requires diffusers and torch
    from diffusers import StableDiffusionPipeline
    import torch
    
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
    print(f"Loading model {model_id} on {device}...")
    
    try:
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id, 
            torch_dtype=torch.float16 if device == "cuda" else torch.float32
        )
        pipe = pipe.to(device)
        image = pipe(prompt).images[0]
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        image.save(output_path)
        return image
    except Exception as e:
        print(f"Error in generate_image: {e}")
        raise e
