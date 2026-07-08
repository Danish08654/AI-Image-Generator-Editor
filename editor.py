from gradio_client import Client, handle_file
from PIL import Image
import tempfile

SPACE_NAME = "Rd786/DanishZulfiqar"

def edit_image(image, prompt, api_key=""):
    client = Client(SPACE_NAME)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        image.save(tmp.name)

        result = client.predict(
            image=handle_file(tmp.name),
            prompt=prompt,
            api_name="/predict",
        )

    return Image.open(result).convert("RGB")
