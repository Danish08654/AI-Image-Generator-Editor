from huggingface_hub import InferenceClient
from PIL import Image
from io import BytesIO


def _pil_to_bytes(image: Image.Image) -> bytes:
    buf = BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()


def _resize(image: Image.Image, max_side: int = 512) -> Image.Image:
    w, h = image.size
    if max(w, h) <= max_side:
        return image

    scale = max_side / max(w, h)
    return image.resize(
        (int(w * scale) & ~1, int(h * scale) & ~1),
        Image.LANCZOS,
    )


def edit_image(image: Image.Image, prompt: str, api_key: str = "") -> Image.Image:

    if not api_key:
        raise RuntimeError(
            "Hugging Face token is required.\n"
            "Get a FREE token at: https://huggingface.co/settings/tokens"
        )

    image = _resize(image.convert("RGB"))

    client = InferenceClient(
        provider="hf-inference",
        api_key=api_key,
    )

    image_bytes = _pil_to_bytes(image)

    result = client.image_to_image(
        image=image_bytes,
        prompt=prompt,
        model="timbrooks/instruct-pix2pix",
    )

    return result
