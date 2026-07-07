import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from PIL import Image
from io import BytesIO

from generator import generate_image
from editor import edit_image
from prompt_engine import enhance_prompt

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Image Generator & Editor",
    page_icon="🎨",
    layout="wide"
)

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown(
    "<h1 style='text-align:center;'>🎨 AI Image Generator & Editor</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; color:gray;'>"
    "Runs fully locally · Stable Diffusion v1.5 · InstructPix2Pix · No API key needed"
    "</p>",
    unsafe_allow_html=True
)
st.markdown("---")

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Info")
    st.success("✅ **No API key required** — models run locally on your machine.")
    st.markdown("**Models used**")
    st.markdown("🖼 **Generate:** `runwayml/stable-diffusion-v1-5`")
    st.markdown("✏️ **Edit:** `timbrooks/instruct-pix2pix`")
    st.markdown("---")
    st.warning(
        "⏬ **First run downloads models** (~4GB generate, ~3GB edit). "
        "Subsequent runs load from cache instantly."
    )
    st.info(
        "🐢 **CPU mode** is slow (~2–5 min/image). "
        "A GPU (CUDA) makes generation ~10x faster."
    )

# ── MODE SELECTION ─────────────────────────────────────────────────────────────
mode = st.radio(
    "Choose Mode",
    ["🖼 Generate Image", "✏️ Edit Image"],
    horizontal=True
)

# ══════════════════════════════════════════════════════════════════════════════
# GENERATE MODE
# ══════════════════════════════════════════════════════════════════════════════
if mode == "🖼 Generate Image":
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📝 Prompt Panel")
        prompt = st.text_area(
            "Describe your image",
            placeholder="e.g. futuristic city at night with neon lights",
            height=150
        )
        size_choice = st.selectbox(
            "Image Size",
            ["512x512", "768x512", "512x768", "640x640"],
            help="512×512 is fastest. Larger sizes need more RAM/time."
        )
        st.caption("💡 Style keywords like *anime*, *painting*, *realistic* auto-enhance your prompt.")
        generate_btn = st.button("✨ Generate Image", type="primary", use_container_width=True)

    with col2:
        st.subheader("🖼 Output Preview")
        if generate_btn:
            if not prompt.strip():
                st.error("⚠️ Please enter a prompt.")
            else:
                try:
                    with st.spinner("⏳ Generating… (first run loads model, may take a few minutes)"):
                        final_prompt = enhance_prompt(prompt)
                        st.info(f"✨ **Enhanced Prompt:** {final_prompt}")
                        img = generate_image(prompt=final_prompt, size=size_choice)
                        st.image(img, use_container_width=True, caption="Generated Image")
                        buf = BytesIO()
                        img.save(buf, format="PNG")
                        buf.seek(0)
                        st.download_button("⬇️ Download Image", buf, "generated_image.png", "image/png")
                        st.success("✅ Done!")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# EDIT MODE
# ══════════════════════════════════════════════════════════════════════════════
else:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📤 Upload Panel")
        uploaded = st.file_uploader("Upload an image to edit", type=["png", "jpg", "jpeg"])
        prompt = st.text_area(
            "Edit Instructions",
            placeholder="e.g. change the background to a beach at sunset",
            height=150
        )
        st.caption("💡 Be specific: 'make the sky purple and add stars' works better than 'change colors'.")
        edit_btn = st.button("🎨 Apply AI Edit", type="primary", use_container_width=True)

    with col2:
        st.subheader("🖼 Output Preview")
        if uploaded:
            image = Image.open(uploaded).convert("RGB")
            st.image(image, caption="Original Image", use_container_width=True)

        if uploaded and edit_btn:
            if not prompt.strip():
                st.error("⚠️ Please enter edit instructions.")
            else:
                try:
                    with st.spinner("⏳ Applying edit… (first run loads model, may take a few minutes)"):
                        final_prompt = enhance_prompt(prompt)
                        st.info(f"✨ **Enhanced Prompt:** {final_prompt}")
                        result = edit_image(image=image, prompt=final_prompt)
                        st.image(result, caption="Edited Image", use_container_width=True)
                        buf = BytesIO()
                        result.save(buf, format="PNG")
                        buf.seek(0)
                        st.download_button("⬇️ Download Edited Image", buf, "edited_image.png", "image/png")
                        st.success("✅ Done!")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
