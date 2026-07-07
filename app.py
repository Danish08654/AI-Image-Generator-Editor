import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from PIL import Image
from io import BytesIO

from generator import generate_image
from editor import edit_image
from prompt_engine import enhance_prompt

st.set_page_config(page_title="AI Image Generator & Editor", page_icon="🎨", layout="wide")

st.markdown("<h1 style='text-align:center;'>🎨 AI Image Generator & Editor</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:gray;'>"
    "Powered by Hugging Face Serverless Inference API · Free HF Token Required"
    "</p>", unsafe_allow_html=True
)
st.markdown("---")

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🔑 HF Token Setup")

    st.markdown("""
**Step 1:** Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

**Step 2:** Click **New token** → select **Read** role → Create

**Step 3:** Copy the token (starts with `hf_...`) and paste below
    """)

    hf_token = st.text_input(
        "Hugging Face Token",
        value=os.getenv("HF_TOKEN", ""),
        type="password",
        placeholder="hf_xxxxxxxxxxxxxxxxxxxxxxxx"
    )
    st.session_state["hf_token"] = hf_token

    if hf_token and hf_token.startswith("hf_"):
        st.success("✅ Token looks valid!")
    elif hf_token:
        st.warning("⚠️ Token should start with `hf_`")
    else:
        st.error("❌ Token required to use this app")

    st.markdown("---")
    st.markdown("**Models used**")
    st.markdown("🖼 Generate: `stable-diffusion-xl-base-1.0`")
    st.markdown("✏️ Edit: `instruct-pix2pix`")
    st.markdown("---")
    st.info("💡 Free tier: ~100–150 requests/day\n\n⏳ First request may take ~20–30s (cold start)")

# ── GATE ───────────────────────────────────────────────────────────────────────
if not st.session_state.get("hf_token", ""):
    st.warning("👈 Please enter your Hugging Face token in the sidebar to get started.")
    st.stop()

# ── MODE ───────────────────────────────────────────────────────────────────────
mode = st.radio("Choose Mode", ["🖼 Generate Image", "✏️ Edit Image"], horizontal=True)

# ── GENERATE ──────────────────────────────────────────────────────────────────
if mode == "🖼 Generate Image":
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("📝 Prompt Panel")
        prompt = st.text_area("Describe your image",
            placeholder="e.g. futuristic city at night with neon lights", height=150)
        size_choice = st.selectbox("Image Size",
            ["1024x1024", "1152x896", "896x1152", "768x768"])
        st.caption("💡 Keywords like *anime*, *painting*, *realistic* auto-enhance your prompt.")
        gen_btn = st.button("✨ Generate Image", type="primary", use_container_width=True)

    with col2:
        st.subheader("🖼 Output Preview")
        if gen_btn:
            if not prompt.strip():
                st.error("⚠️ Please enter a prompt.")
            else:
                try:
                    with st.spinner("⏳ Generating via HF Inference API…"):
                        final_prompt = enhance_prompt(prompt)
                        st.info(f"✨ **Enhanced Prompt:** {final_prompt}")
                        img = generate_image(
                            prompt=final_prompt,
                            size=size_choice,
                            api_key=st.session_state["hf_token"]
                        )
                        st.image(img, use_container_width=True, caption="Generated Image")
                        buf = BytesIO()
                        img.save(buf, format="PNG")
                        buf.seek(0)
                        st.download_button("⬇️ Download Image", buf, "generated_image.png", "image/png")
                        st.success("✅ Image generated successfully!")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ── EDIT ──────────────────────────────────────────────────────────────────────
else:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("📤 Upload Panel")
        uploaded = st.file_uploader("Upload an image to edit", type=["png", "jpg", "jpeg"])
        prompt = st.text_area("Edit Instructions",
            placeholder="e.g. change the background to a beach at sunset", height=150)
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
                    with st.spinner("⏳ Editing via HF Inference API…"):
                        final_prompt = enhance_prompt(prompt)
                        st.info(f"✨ **Enhanced Prompt:** {final_prompt}")
                        result = edit_image(
                            image=image,
                            prompt=final_prompt,
                            api_key=st.session_state["hf_token"]
                        )
                        st.image(result, caption="Edited Image", use_container_width=True)
                        buf = BytesIO()
                        result.save(buf, format="PNG")
                        buf.seek(0)
                        st.download_button("⬇️ Download Edited Image", buf, "edited_image.png", "image/png")
                        st.success("✅ Done!")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
