from PIL import Image
from gradio_client import Client, handle_file

# Replace with your own Space
SPACE_NAME = "DanishZulfiqar/instruct-pix2pix"

client = Client(SPACE_NAME)


def edit_image(image: Image.Image, prompt: str):

    image.save("temp.png")

    result = client.predict(
        image=handle_file("temp.png"),
        prompt=prompt,
        api_name="/predict"
    )

    return Image.open(result)
