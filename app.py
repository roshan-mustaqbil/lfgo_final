import streamlit as st
import requests
import os
from dotenv import load_dotenv
from PIL import Image
import io

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")

API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": f"Bearer {API_KEY}"}

# Function to query the image generation API
def query(prompt):
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    if response.status_code == 200:
        return response.content
    else:
        st.error("Error generating image: " + response.text)
        return None

# Streamlit UI
st.set_page_config(page_title="AI Text to Image Generator", layout="centered")
st.title("AI Text to Image Generator")

# Input for the prompt
prompt = st.text_input("Enter your prompt here...")

if st.button("Generate Images"):
    if prompt:
        images = []
        for _ in range(3):  # Generate 3 images
            image_bytes = query(prompt)
            if image_bytes:
                image = Image.open(io.BytesIO(image_bytes))
                images.append(image)

        # Display images in a grid
        if images:
            cols = st.columns(3)
            for i, img in enumerate(images):
                with cols[i]:
                    st.image(img, use_column_width=True, caption="Generated Image", output_format="PNG")
    else:
        st.warning("Please enter a prompt.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Your Name")
