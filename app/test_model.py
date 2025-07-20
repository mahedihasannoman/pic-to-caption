from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

# Config
IMAGE_PATH = "example3.jpg"  # Replace with the actual path to your test image

# Load model and processor
print("🔄 Loading model...")
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base", use_fast=True)
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Load and preprocess image
print(f"🖼️  Loading image: {IMAGE_PATH}")
image = Image.open(IMAGE_PATH).convert("RGB")
inputs = processor(images=image, return_tensors="pt").to(device)

# Generate caption
print("⚙️  Generating ALT text...")
with torch.no_grad():  # Optimize inference
    output = model.generate(
        **inputs,
        max_length=100,  # Increased from default (~20) for longer captions
        min_length=30,   # Ensure minimum caption length
        num_beams=5,     # More beams for better quality
        length_penalty=1.0,  # Encourage longer sequences
        repetition_penalty=1.2,  # Reduce repetition
        do_sample=True,  # Enable sampling for more diverse captions
        temperature=0.7,  # Control randomness
        top_p=0.9,       # Nucleus sampling
        early_stopping=True
    )
caption = processor.decode(output[0], skip_special_tokens=True)

print("✅ ALT Text:", caption)
