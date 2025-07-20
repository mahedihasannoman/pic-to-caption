from fastapi import FastAPI, UploadFile, File, HTTPException, Security, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.security.api_key import APIKeyHeader
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import io
import os
from dotenv import load_dotenv

app = FastAPI()

# Load environment variables from .env file
load_dotenv()

# Define the API key and header
API_KEY = os.getenv("API_KEY", "defaultapikey")  # Replace "defaultapikey" with a fallback key or leave it empty
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# Load model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Mount the static directory to serve HTML files
app.mount("/static", StaticFiles(directory="static"), name="static")

def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate API key")
    return api_key

@app.get("/")
def read_root():
    return {"message": "Welcome to the Image Captioning API!"}

# Protect the /generate-alt route with API key authentication
@app.post("/generate-alt")
async def generate_alt(file: UploadFile = File(...), api_key: str = Depends(verify_api_key)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    inputs = processor(images=image, return_tensors="pt").to(device)
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)

    return {"alt_text": caption}
