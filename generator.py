import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_image(prompt):

    response = client.images.generate(
        model="dall-e-3" ,
        prompt=prompt,
        size="1024x1024"
    )

    image_url = response.data[0].url

    return image_url
