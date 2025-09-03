import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import base64
import os

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash-image-preview")

resp = model.generate_content(
    "Generate a photorealistic green minimalistic PX logo on black, 1:1, high-contrast",
    generation_config={
        "response_modalities": ["TEXT", "IMAGE"],
        "candidate_count": 1,
    }
)

i = 0
for part in resp.parts:
    if hasattr(part, "inline_data") and part.inline_data.data:
        img_bytes = part.inline_data.data
        Image.open(BytesIO(img_bytes)).save(f"out_{i}.png")
        i += 1
    elif hasattr(part, "text") and part.text:
        print(part.text)

print(f"Saved {i} image(s).")
