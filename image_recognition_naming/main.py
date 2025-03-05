# 

import glob
import json
import google.generativeai as genai
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# prompt_instruction = "You are shwon an image. Your job is to respond with a jso object describing the image with two words"

prompt_instruction = (
    "You are an AI assistant specialized in generating concise, descriptive filenames for images. "
    "Your task is to analyze the given image and respond with a JSON object containing a meaningful, minimal filename. "
    "Use exactly two words: an adjective or descriptor (e.g., color, size, emotion) and a noun (e.g., object, subject). "
    "Do not use articles, punctuation, special characters, or complex phrases. "
    "Strictly follow this format: {\"image1\": \"descriptor\", \"image2\": \"object\"}. "
    "Examples:\n"
    "- A bright sun in the sky → {\"image1\": \"bright\", \"image2\": \"sun\"}\n"
    "- A small puppy sitting on grass → {\"image1\": \"small\", \"image2\": \"puppy\"}\n"
    "- A red sports car on the road → {\"image1\": \"red\", \"image2\": \"car\"}"
)

model = genai.GenerativeModel("gemini-2.0-flash")

# function to list all models in Gemini
"""
 for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name) 
"""


def run(image_name):
    try:
        imgfile = genai.upload_file(image)
        result = model.generate_content(
            [imgfile, "\n\n", prompt_instruction]
        )

        ext = Path(image_name).suffix
        image_description = json.loads(result.text)
        new_filename = f"{image_description['image1']}_{image_description['image2']}{ext}"
        
        os.rename(image_name, new_filename)
        print(f"File renamed to : {new_filename}")
    
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except KeyError as e:
        print(f"Missing key in JSON: {e}")
    except OSError as e:
        print(f"Error renaming file: {e}")
    except Exception as e:
        print(f"Unexpected error : {e}")

image_extensions = ("*.jpg", "*.jpeg", "*.png")
image_files = []

for exe in image_extensions:
    image_files.extend(glob.glob(exe))

print(f"Found {len(image_files)} image file.")


for image in image_files:
    run(image)