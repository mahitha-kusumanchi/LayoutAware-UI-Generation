# 🎨 LayoutGen: Layout-Aware AI Image Generation

LayoutGen is a full-stack AI application that transforms JSON layout descriptions into beautiful images using Stable Diffusion. It bridges the gap between structured spatial data and creative image synthesis.

## 🏗️ Architecture

- **Frontend**: Streamlit-based UI for layout upload, visualization, and result display.
- **Backend**:
    - `prompt_generator.py`: Converts bounding boxes (x, y, w, h) into natural language prompts.
    - `layout_to_image.py`: Handles local layout visualization (PIL) and Stable Diffusion generation (Diffusers).
- **GPU Support**: Includes a Google Colab notebook for users without local GPU hardware.

## 📂 Project Structure

```text
layoutgen/
├── frontend/
│   └── app.py              # Streamlit User Interface
├── backend/
│   ├── prompt_generator.py # Layout-to-Text logic
│   ├── layout_to_image.py  # Visualization & Local Generation
│   └── sample_layout.json  # Example input format
├── notebooks/
│   └── layoutgen_colab.ipynb # Google Colab GPU Notebook
├── outputs/                # Local storage for results
└── requirements.txt        # Dependencies
```

## 🚀 Getting Started

### Lightweight API Mode (No Heavy Install)

This project now supports **Hugging Face Inference API**, which avoids downloading massive AI models (GBs) to your computer.
1. **Get a Token**: 
   - Create a free account at [huggingface.co](https://huggingface.co).
   - Go to [Settings > Access Tokens](https://huggingface.co/settings/tokens) and create a new token.
   - **Crucial**: Select **"Read"** as the token type (or "Fine-grained" with `Inference: Read` permissions). You do not need write access.
2. **Install Minimal Dependencies**:
   ```bash
   pip install streamlit requests pillow huggingface_hub
   ```
3. **Run the App**:
   ```bash
   streamlit run frontend/app.py
   ```
4. **Choose API Mode**: Select "Hugging Face API" in the sidebar, pick a model (e.g. `runwayml/stable-diffusion-v1-5`), and enter your token.

### Local Setup (CPU/Local GPU/Colab)

If you prefer to run everything locally (requires GBs of downloads):
1. **Install Full Dependencies**:
   (Standard installation including `torch`, `diffusers`).
2. **Run the Streamlit App**:
   ```bash
   streamlit run frontend/app.py
   ```

If you don't have a local GPU, follow these steps:
1. Upload `notebooks/layoutgen_colab.ipynb` to [Google Colab](https://colab.research.google.com/).
2. Change runtime type to **GPU**.
3. Use the Streamlit app to generate a prompt from your layout.
4. Paste the prompt into the Colab notebook to generate the image.

## 📄 JSON Input Format

Example `layout.json`:
```json
{
    "title": "A serene living room",
    "objects": [
        {
            "label": "blue sofa",
            "bbox": [100, 300, 400, 200]
        }
    ]
}
```

## 🛠️ Requirements
- Python 3.8+
- PyTorch
- Diffusers
- Streamlit
- Pillow
