import torch
from diffusers import StableDiffusionPipeline
from PIL import Image, ImageDraw
import json
import os
from prompt_generator import extract_objects

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
    
    # Check if the root elements had direct objects (the parser handles this)
    # The new prompt_generator normalized logic might add "normalized" flag
    # Let's standardize the extraction first
    objects = []
    for obj_data in data.get("objects", []):
        if "label" not in obj_data: continue
        
        if "bbox" in obj_data:
            objects.append(obj_data)
        elif "x" in obj_data and "y" in obj_data and "width" in obj_data and "height" in obj_data:
            objects.append({
                "label": obj_data.get("label"), 
                "bbox": [obj_data["x"], obj_data["y"], obj_data["width"], obj_data["height"]],
                "normalized": isinstance(obj_data["x"], float) and obj_data["x"] <= 1.0
            })
            
    if not objects:
        objects = extract_objects(data)
        
    import random
    
    # Pre-defined nice colors for common objects
    color_map = {
        "bed": (100, 150, 200),
        "window": (180, 220, 250),
        "lamp": (255, 230, 150),
        "door": (160, 120, 80),
        "table": (180, 140, 100),
        "sofa": (200, 150, 150),
        "chair": (150, 200, 150),
        "plant": (100, 200, 100),
        "tv": (50, 50, 50),
        "cabinet": (200, 180, 150),
        "painting": (220, 180, 200)
    }
    
    # Track used random colors to avoid duplicates
    used_colors = {}
    
    # Sort objects by area (descending) so large background objects are drawn first
    # and don't cover up small foreground objects
    def get_area(obj):
        bbox = obj.get("bbox", [0, 0, 0, 0])
        if len(bbox) == 4:
            return bbox[2] * bbox[3] # width * height
        return 0
        
    sorted_objects = sorted(objects, key=get_area, reverse=True)
    
    for obj in sorted_objects:
        label = obj.get("label", "unknown").lower()
        bbox = obj.get("bbox", [0, 0, 0, 0])
        x, y, w, h = bbox
        
        is_normalized = obj.get("normalized", False)
        # Or auto-detect if coordinates are obviously fractional
        if not is_normalized and max(w, h, x, y) <= 1.0:
            is_normalized = True
            
        if is_normalized:
            # Scale fractional coordinates [0.0, 1.0] to image size
            nx, ny = x * size[0], y * size[1]
            nw, nh = w * size[0], h * size[1]
        else:
            # Scale coordinates if they are for a 1440x2560 screen
            # Simple normalization to image size 
            scale_x = size[0] / 1440.0
            scale_y = size[1] / 2560.0
            
            nx, ny = x * scale_x, y * scale_y
            nw, nh = w * scale_x, h * scale_y
        
        # Get color for label
        base_label = label.split()[-1] # e.g. "large oak bed" -> "bed"
        if base_label in color_map:
            fill_color = color_map[base_label]
        elif label in used_colors:
            fill_color = used_colors[label]
        else:
            # Generate a distinct random pastel color
            fill_color = (
                random.randint(100, 255),
                random.randint(100, 255),
                random.randint(100, 255)
            )
            used_colors[label] = fill_color
            
        # Draw solid rectangle
        draw.rectangle([nx, ny, nx + nw, ny + nh], fill=fill_color, outline="black", width=2)
        # Draw label
        draw.text((nx + 5, ny + 5), label, fill="black")
        
    return img

import requests
import io
from huggingface_hub import InferenceClient

def generate_image_api(prompt, api_key, image=None, strength=0.7, model_id="runwayml/stable-diffusion-v1-5", output_path="outputs/generated_image.png"):
    """
    Generates an image from a prompt using Hugging Face Inference API.
    If image is provided, performs image_to_image generation.
    """
    client = InferenceClient(model=model_id, token=api_key)

    try:
        if image is not None:
            # Img2Img generation using image_to_image endpoint with strength parameter
            # Need to convert PIL image to RGB and then to bytes
            if image.mode != "RGB":
                image = image.convert("RGB")
            
            print(f"Calling Hugging Face API image-to-image for model {model_id}...")
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="PNG")
            image_bytes = image_bytes.getvalue()
            
            res_image = client.image_to_image(image=image_bytes, prompt=prompt)
            final_image = res_image
        else:
            # Baseline Text-to-Image generation
            print(f"Calling Hugging Face API text-to-image for model {model_id}...")
            final_image = client.text_to_image(prompt)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        final_image.save(output_path)
        
        return final_image
    except Exception as e:
        import traceback
        error_msg = f"Error in generate_image_api (model: {model_id}): {str(e)}"
        print(error_msg)
        print(traceback.format_exc())
        raise Exception(error_msg) from e

def generate_image(prompt, image=None, strength=0.7, model_id="runwayml/stable-diffusion-v1-5", device=None, output_path="outputs/generated_image.png"):
    # (Existing local function preserved for Colab/Local GPU users)
    # Note: Requires diffusers and torch
    from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline
    import torch
    
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
    print(f"Loading model {model_id} on {device}...")
    
    try:
        if image is not None:
            pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
                model_id, 
                torch_dtype=torch.float16 if device == "cuda" else torch.float32
            )
            pipe = pipe.to(device)
            # Img2Img requires an initial image
            if image.mode != "RGB":
                image = image.convert("RGB")
            # Strength controls how much to transform the image
            # lower means more like original image (layout sketch)
            final_image = pipe(prompt=prompt, image=image, strength=strength).images[0]
        else:
            pipe = StableDiffusionPipeline.from_pretrained(
                model_id, 
                torch_dtype=torch.float16 if device == "cuda" else torch.float32
            )
            pipe = pipe.to(device)
            final_image = pipe(prompt).images[0]
            
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        final_image.save(output_path)
        return final_image
    except Exception as e:
        print(f"Error in generate_image: {e}")
        raise e
