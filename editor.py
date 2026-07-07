from gradio_client import Client, handle_file
from PIL import Image
from io import BytesIO
import tempfile, os

# Free public HF Space for instruction-based editing
SPACE = "timbrooks/instruct-pix2pix"

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = Client(SPACE)
    return _client

def _save_temp(image: Image.Image) -> str:
    """Save PIL image to a temp file and return the path."""
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    image.save(tmp.name, format="PNG")
    return tmp.name

def _resize(image: Image.Image, max_side: int = 512) -> Image.Image:
    w, h = image.size
    if max(w, h) <= max_side:
        return image
    scale = max_side / max(w, h)
    return image.resize((int(w * scale) & ~1, int(h * scale) & ~1), Image.LANCZOS)

def edit_image(image: Image.Image, prompt: str, api_key: str = "") -> Image.Image:
    """
    Edit image via free Hugging Face Space (timbrooks/instruct-pix2pix).
    No token needed. No local download. Runs on HF servers.
    """
    image = _resize(image.convert("RGB"))
    tmp_path = _save_temp(image)

    try:
        client = _get_client()
        result = client.predict(
            image=handle_file(tmp_path),
            instruction=prompt,
            steps=20,
            randomize_seed=True,
            seed=0,
            text_cfg_scale=7.5,
            image_cfg_scale=1.5,
            api_name="/generate"
        )

        if isinstance(result, (list, tuple)):
            path = result[0] if result else None
        else:
            path = result

        if path and os.path.exists(path):
            return Image.open(path).convert("RGB")

        raise RuntimeError(f"Unexpected response from Space: {result}")
    finally:
        os.unlink(tmp_path)
