import os
import sys
from huggingface_hub import InferenceClient

def test_hf_api(api_key, model_id="runwayml/stable-diffusion-v1-5"):
    client = InferenceClient(model=model_id, token=api_key)
    prompt = "A high-quality 3D render of a futuristic smartphone UI layout"
    
    print(f"Testing model: {model_id}")
    try:
        image = client.text_to_image(prompt)
        image.save("hf_test_output.png")
        print("Success! Image saved to hf_test_output.png")
    except Exception as e:
        print(f"Failed with error: {e}")
        if "404" in str(e) or "Not Found" in str(e):
            print("\nSuggestion: The model might not be available as a serverless Inference API.")
            print("Try checking https://huggingface.co/" + model_id)
            print("Look for 'Inference API' in the right sidebar.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python hf_test.py <YOUR_HF_TOKEN> [model_id]")
    else:
        token = sys.argv[1]
        model = sys.argv[2] if len(sys.argv) > 2 else "runwayml/stable-diffusion-v1-5"
        test_hf_api(token, model)
