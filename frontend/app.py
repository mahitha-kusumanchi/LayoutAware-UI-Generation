import streamlit as st
import json
import sys
import os

# Add backend to path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from prompt_generator import generate_prompt
from layout_to_image import generate_image, visualize_layout
from PIL import Image
import io

st.set_page_config(page_title="LayoutGen - AI Image Generator", layout="wide")

st.title("🎨 LayoutGen: From Layout to Image")
st.markdown("""
Transform your JSON layouts into beautiful images using Stable Diffusion. Now with layout visualization!
""")

# Sidebar for configuration
st.sidebar.header("Configuration")
model_id = st.sidebar.text_input("Model ID", "runwayml/stable-diffusion-v1-5")
device = st.sidebar.selectbox("Device", ["cpu", "cuda"] if "cuda" in st.sidebar.text_input("Raw Device (hidden)", "") else ["cpu"])

# Main interface
col1, col2 = st.columns([1, 1])

with col1:
    st.header("1. Input Layout")
    uploaded_file = st.file_uploader("Upload a JSON layout file", type=["json"])
    
    if uploaded_file is not None:
        try:
            layout_data = json.load(uploaded_file)
            st.subheader("Layout Preview (JSON)")
            st.json(layout_data)
            
            # Layout Visualization
            st.subheader("Layout Visualization")
            vis_img = visualize_layout(layout_data)
            st.image(vis_img, caption="Bounding Box Visualization", use_container_width=True)
            
            # Generate Prompt
            prompt = generate_prompt(layout_data)
            st.info(f"**Generated Prompt:**\n{prompt}")
            
            if st.button("🚀 Generate Image"):
                with st.spinner("Generating image... This may take a moment."):
                    try:
                        # Call image generator
                        img = generate_image(prompt, model_id=model_id, device=device)
                        st.session_state['generated_image'] = img
                        st.success("Image generated successfully!")
                    except Exception as e:
                        st.error(f"Error generating image: {e}")
                        
        except Exception as e:
            st.error(f"Error parsing JSON: {e}")

with col2:
    st.header("2. Generated Output")
    if 'generated_image' in st.session_state:
        st.image(st.session_state['generated_image'], caption="Final Stable Diffusion Result", use_container_width=True)
        
        # Download button
        buf = io.BytesIO()
        st.session_state['generated_image'].save(buf, format="PNG")
        byte_im = buf.getvalue()
        st.download_button(
            label="💾 Download Image",
            data=byte_im,
            file_name="generated_layout.png",
            mime="image/png"
        )
    else:
        st.info("Upload a layout and click 'Generate Image' to see the result.")
