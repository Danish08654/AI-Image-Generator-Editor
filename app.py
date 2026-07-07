import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from PIL import Image
from io import BytesIO

from generator import generate_image
from editor import edit_image
from prompt_engine import enhance_prompt, get_negative_prompt

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
    "Powered by Hugging Face · Stable Diffusion XL · InstructPix2Pix"
    "</p>",
    unsafe_allow_html=True
)
st.markdown("---")

# ── SIDEBAR — HF TOKEN (OPTIONAL) ─────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    st.markdown(
        "**Hugging Face Token** *(optional but recommended)*\n\n"
        "Free models work without a token but may be rate-limited. "
        "Get yours at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)."
    )
    hf_token = st.text_input(
        "HF Token",
        value=os.getenv("HF_TOKEN", ""),
        type="password",
        placeholder="hf_xxxxxxxxxxxxxxxxxxxx"
    )
    st.session_state["hf_token"] = hf_token

    st.markdown("---")
    st.markdown("**Models used**")
    st.markdown("🖼 **Generate:** `stabilityai/stable-diffusion-xl-base-1.0`")
    st.markdown("✏️ **Edit:** `timbrooks/instruct-pix2pix`")
    st.markdown("---")
    st.info(
        "If you see a **503 error**, the model is cold-starting on HF servers. "
        "Wait ~30 seconds and click again."
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
            ["1024x1024", "1152x896", "896x1152", "768x768"],
            help="1024×1024 is the default SDXL resolution."
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
                    with st.spinner("⏳ Generating your image (this may take ~30s)…"):
                        final_prompt = enhance_prompt(prompt)
                        st.info(f"✨ **Enhanced Prompt:** {final_prompt}")

                        img = generate_image(
                            prompt=final_prompt,
                            size=size_choice,
                            api_key=st.session_state.get("hf_token", "")
                        )

                        st.image(img, use_container_width=True, caption="Generated Image")

                        # Download
                        buf = BytesIO()
                        img.save(buf, format="PNG")
                        buf.seek(0)
                        st.download_button(
                            label="⬇️ Download Image",
                            data=buf,
                            file_name="generated_image.png",
                            mime="image/png"
                        )
                        st.success("✅ Image generated successfully!")

                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# EDIT MODE
# ══════════════════════════════════════════════════════════════════════════════
else:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📤 Upload Panel")
        uploaded = st.file_uploader(
            "Upload an image to edit",
            type=["png", "jpg", "jpeg"]
        )

        prompt = st.text_area(
            "Edit Instructions",
            placeholder="e.g. change the background to a beach at sunset",
            height=150
        )

        st.caption(
            "💡 Be specific: *'make the sky purple and add stars'* "
            "works better than *'change colors'*."
        )
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
                    with st.spinner("⏳ Applying AI edit (this may take ~30s)…"):
                        final_prompt = enhance_prompt(prompt)
                        st.info(f"✨ **Enhanced Prompt:** {final_prompt}")

                        result = edit_image(
                            image=image,
                            prompt=final_prompt,
                            api_key=st.session_state.get("hf_token", "")
                        )

                        st.image(result, caption="Edited Image", use_container_width=True)

                        # Download
                        buf = BytesIO()
                        result.save(buf, format="PNG")
                        buf.seek(0)
                        st.download_button(
                            label="⬇️ Download Edited Image",
                            data=buf,
                            file_name="edited_image.png",
                            mime="image/png"
                        )
                        st.success("✅ Image edited successfully!")

                except Exception as e:
                    st.error(f"❌ Error: {e}")
