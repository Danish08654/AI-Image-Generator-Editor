import os
from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO

def generate_image(prompt, model="dall-e-3", size="1024x1024", api_key=None):
    """
    Generate an image using OpenAI DALL-E API
    
    Args:
        prompt (str): The prompt describing the image to generate
        model (str): The model to use - "dall-e-3" or "dall-e-2"
        size (str): Image size - "1024x1024", "1792x1024", "1024x1792" for DALL-E 3
        api_key (str): OpenAI API key
    
    Returns:
        str: URL of the generated image
    """
    
    if not api_key:
        raise ValueError(" OpenAI API key is required. Please provide it in the sidebar.")
    
    if not prompt or not prompt.strip():
        raise ValueError(" Prompt cannot be empty")
    
    try:
        # Initialize OpenAI client with provided API key
        client = OpenAI(api_key=api_key)
        
        # Validate model choice
        valid_models = ["dall-e-3", "dall-e-2"]
        if model not in valid_models:
            raise ValueError(f" Invalid model: {model}. Must be one of {valid_models}")
        
        # Validate size for DALL-E 3
        if model == "dall-e-3":
            valid_sizes_3 = ["1024x1024", "1792x1024", "1024x1792"]
            if size not in valid_sizes_3:
                size = "1024x1024"
        else:
            valid_sizes_2 = ["256x256", "512x512", "1024x1024"]
            if size not in valid_sizes_2:
                size = "1024x1024"
        
        print(f" Generating image with {model}...")
        print(f" Prompt: {prompt[:100]}...")
        
        # Call the API with correct model name
        response = client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            quality="hd" if model == "dall-e-3" else "standard",
            n=1
        )
        
        # Extract and return image URL
        image_url = response.data[0].url
        print(f" Image generated successfully!")
        
        return image_url
    
    except ValueError as e:
        print(f" Validation Error: {str(e)}")
        raise
    except Exception as e:
        error_msg = str(e)
        if "invalid_api_key" in error_msg or "401" in error_msg:
            raise ValueError(" Invalid API Key! Please check your OpenAI API key in the sidebar.")
        elif "rate_limit" in error_msg or "429" in error_msg:
            raise ValueError(" Rate limit exceeded. Please wait a moment and try again.")
        elif "invalid_request" in error_msg:
            raise ValueError(f" Invalid request: Your prompt might violate content policy.")
        else:
            raise ValueError(f" Error generating image: {error_msg}")


def download_image(image_url, save_path="generated_image.png"):
    """
    Download an image from URL and save it
    
    Args:
        image_url (str): URL of the image
        save_path (str): Path to save the image
    
    Returns:
        PIL.Image: The downloaded image
    """
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        
        img = Image.open(BytesIO(response.content))
        img.save(save_path)
        
        print(f" Image saved to {save_path}")
        return img
    
    except Exception as e:
        print(f"❌ Error downloading image: {str(e)}")
        raise
