from io import BytesIO
from typing import Optional

import cv2
import numpy as np
from huggingface_hub import InferenceClient
from PIL import Image, ImageEnhance, ImageFilter

try:
    from rembg import remove
    REMBG_AVAILABLE = True
except ImportError:
    REMBG_AVAILABLE = False


# ==========================================================
# Helper Functions
# ==========================================================

def _pil_to_bytes(image: Image.Image) -> bytes:
    """Convert PIL Image to PNG bytes."""
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def _resize(image: Image.Image, max_side: int = 512) -> Image.Image:
    """Resize image while maintaining aspect ratio."""
    w, h = image.size

    if max(w, h) <= max_side:
        return image

    scale = max_side / max(w, h)

    new_w = max(2, int(w * scale))
    new_h = max(2, int(h * scale))

    # Even dimensions
    new_w -= new_w % 2
    new_h -= new_h % 2

    return image.resize((new_w, new_h), Image.LANCZOS)


# ==========================================================
# AI Image Editing
# ==========================================================

def edit_image(
    image: Image.Image,
    prompt: str,
    api_key: str
) -> Image.Image:
    """
    AI edit using Hugging Face InstructPix2Pix.
    """

    if not api_key:
        raise RuntimeError(
            "Hugging Face token is required.\n"
            "https://huggingface.co/settings/tokens"
        )

    image = _resize(image.convert("RGB"))

    client = InferenceClient(
        provider="hf-inference",
        api_key=api_key,
    )

    result = client.image_to_image(
        image=_pil_to_bytes(image),
        prompt=prompt,
        model="timbrooks/instruct-pix2pix",
    )

    return result


# ==========================================================
# Background Removal
# ==========================================================

def remove_background(image: Image.Image) -> Image.Image:
    """
    Remove image background using rembg.
    """

    if not REMBG_AVAILABLE:
        raise RuntimeError(
            "rembg is not installed.\n"
            "pip install rembg onnxruntime"
        )

    output = remove(_pil_to_bytes(image))

    return Image.open(BytesIO(output)).convert("RGBA")


# ==========================================================
# Blur Background
# ==========================================================

def blur_image(image: Image.Image, radius: int = 8) -> Image.Image:
    return image.filter(ImageFilter.GaussianBlur(radius))


# ==========================================================
# Brightness
# ==========================================================

def adjust_brightness(
    image: Image.Image,
    factor: float
) -> Image.Image:
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)


# ==========================================================
# Contrast
# ==========================================================

def adjust_contrast(
    image: Image.Image,
    factor: float
) -> Image.Image:
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)


# ==========================================================
# Saturation
# ==========================================================

def adjust_saturation(
    image: Image.Image,
    factor: float
) -> Image.Image:
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(factor)


# ==========================================================
# Sharpen
# ==========================================================

def sharpen_image(
    image: Image.Image,
    factor: float = 2.0
) -> Image.Image:
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(factor)


# ==========================================================
# Cartoon Effect
# ==========================================================

def cartoon_effect(image: Image.Image) -> Image.Image:

    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.medianBlur(gray, 5)

    edges = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        9,
        9,
    )

    color = cv2.bilateralFilter(img, 9, 300, 300)

    cartoon = cv2.bitwise_and(color, color, mask=edges)

    return Image.fromarray(
        cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
    )


# ==========================================================
# Sketch Effect
# ==========================================================

def sketch_effect(image: Image.Image) -> Image.Image:

    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

    inv = 255 - img

    blur = cv2.GaussianBlur(inv, (21, 21), 0)

    sketch = cv2.divide(img, 255 - blur, scale=256)

    return Image.fromarray(sketch)


# ==========================================================
# Pencil Drawing
# ==========================================================

def pencil_effect(image: Image.Image) -> Image.Image:

    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

    sketch, _ = cv2.pencilSketch(
        cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR),
        sigma_s=60,
        sigma_r=0.07,
        shade_factor=0.05,
    )

    return Image.fromarray(sketch)


# ==========================================================
# AI Upscaling (Simple)
# ==========================================================

def upscale_image(
    image: Image.Image,
    scale: int = 2
) -> Image.Image:
    """
    Lightweight image upscaling.
    """

    w, h = image.size

    return image.resize(
        (w * scale, h * scale),
        Image.LANCZOS,
    )
