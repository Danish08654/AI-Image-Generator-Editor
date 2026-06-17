from PIL import Image
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def edit_image(image, prompt):

    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        image.save(tmp.name)

        result = client.images.edit(
            model="gpt-image-1",
            image=open(tmp.name, "rb"),
            prompt=prompt
        )

    return result.data[0].url