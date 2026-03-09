import torch
from diffusers import StableDiffusionPipeline
from PIL import Image

def generate_image(prompt, model_id="runwayml/stable-diffusion-v1-5", device=None):
    """
    Generates an image from a prompt using Stable Diffusion.
    """
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
    print(f"Loading model {model_id} on {device}...")
    
    # Using float16 for GPU to save memory, float32 for CPU
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id, 
        torch_dtype=torch.float16 if device == "cuda" else torch.float32
    )
    pipe = pipe.to(device)
    
    print(f"Generating image for prompt: '{prompt}'")
    image = pipe(prompt).images[0]
    
    return image

if __name__ == "__main__":
    # Test logic (using CPU for local testing if no CUDA)
    # Warning: Standard SD takes time on CPU
    try:
        test_image = generate_image("a simple cat", model_id="hf-internal-testing/tiny-stable-diffusion-torch")
        test_image.save("test_output.png")
        print("Test image saved as test_output.png")
    except Exception as e:
        print(f"Image generation failed: {e}")
