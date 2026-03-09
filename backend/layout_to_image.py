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

def generate_image(prompt, model_id="runwayml/stable-diffusion-v1-5", device=None, output_path="outputs/generated_image.png"):
    """
    Generates an image from a prompt using Stable Diffusion.
    """
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
    print(f"Loading model {model_id} on {device}...")
    
    try:
        # Using float16 for GPU to save memory, float32 for CPU
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id, 
            torch_dtype=torch.float16 if device == "cuda" else torch.float32
        )
        pipe = pipe.to(device)
        
        print(f"Generating image for prompt: '{prompt}'")
        image = pipe(prompt).images[0]
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        image.save(output_path)
        
        return image
    except Exception as e:
        print(f"Error in generate_image: {e}")
        raise e
