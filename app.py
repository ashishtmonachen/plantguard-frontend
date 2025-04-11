#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import requests
from PIL import Image

# Set up the Streamlit page
st.set_page_config(page_title="PlantGuard AI", layout="centered")
st.title("🌿 PlantGuard AI")
st.subheader("Upload a leaf image to detect plant disease")

# File uploader
uploaded_file = st.file_uploader("Choose a leaf image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Reset file pointer before sending to backend
    uploaded_file.seek(0)

    if st.button("🔍 Predict Disease"):
        with st.spinner("Analyzing the image..."):
            try:
                # Send the image to the backend
                files = {
                    "image": (uploaded_file.name, uploaded_file, uploaded_file.type)
                }
                response = requests.post(
                    "https://plantguard-backend.onrender.com/predict",
                    files=files
                )

                if response.status_code == 200:
                    result = response.json()
                    st.success(f"Prediction: **{result['label'].replace('_', ' ').title()}**")
                    st.write(f"Confidence: `{result['confidence']}%`")
                    st.info(f"Suggested Remedy: {result['remedy']}")
                else:
                    st.error("❌ Failed to get a response from the server.")
                    st.text(f"Status Code: {response.status_code}")
                    st.text(response.text)

            except Exception as e:
                st.error(f"An error occurred: {e}")
