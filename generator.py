import requests
from PIL import Image
from io import BytesIO


# Free HF Inference API — Stable Diffusion XL
HF_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"


def generate_image(prompt: str, model: str = "sdxl", size: str = "1024x1024", api_key: str = "") -> Image.Image:
    """
    Generate an image using Hugging Face Inference API (SDXL).
    Returns a PIL Image object.
    """
    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    # Parse size into width/height parameters
    try:
        width, height = map(int, size.split("x"))
    except ValueError:
        width, height = 1024, 1024

    payload = {
        "inputs": prompt,
        "parameters": {
            "width": width,
            "height": height,
            "num_inference_steps": 30,
            "guidance_scale": 7.5,
        }
    }

    response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=120)

    if response.status_code == 503:
        raise RuntimeError(
            "Model is loading on Hugging Face servers. Please wait 20–30 seconds and try again."
        )
    if response.status_code == 401:
        raise RuntimeError(
            "Invalid or missing Hugging Face API token. "
            "Get a free token at https://huggingface.co/settings/tokens"
        )
    if response.status_code != 200:
        raise RuntimeError(
            f"Hugging Face API error {response.status_code}: {response.text[:300]}"
        )

    image = Image.open(BytesIO(response.content)).convert("RGB")
    return image
