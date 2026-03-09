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

### Local Setup (CPU/Local GPU)

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the Streamlit App**:
   ```bash
   streamlit run frontend/app.py
   ```

### Google Colab (GPU Acceleration)

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
