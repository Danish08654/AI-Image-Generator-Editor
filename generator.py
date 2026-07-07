from gradio_client import Client
from PIL import Image
import shutil, os

# Free public HF Space — no token, no download, no firewall issues
SPACE = "hysts/stable-diffusion-xl"

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = Client(SPACE)
    return _client

def generate_image(prompt: str, model: str = "sdxl", size: str = "1024x1024", api_key: str = "") -> Image.Image:
    """
    Generate image via free Hugging Face Space (hysts/stable-diffusion-xl).
    No token needed. No local download. Runs on HF servers.
    """
    client = _get_client()

    result = client.predict(
        prompt=prompt,
        negative_prompt="blurry, low quality, deformed, watermark, text",
        guidance_scale=7.5,
        num_inference_steps=25,
        api_name="/run"
    )

    # result is a file path to the generated image
    if isinstance(result, str) and os.path.exists(result):
        return Image.open(result).convert("RGB")
    elif isinstance(result, (list, tuple)):
        path = result[0] if result else None
        if path and os.path.exists(path):
            return Image.open(path).convert("RGB")

    raise RuntimeError(f"Unexpected response from Space: {result}")
