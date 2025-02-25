import os
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

# Load BLIP-2 model for image captioning
device = "cuda" if torch.cuda.is_available() else "cpu"
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to(device)

def generate_image_caption(image_path):
    """Generates a caption describing the image"""
    try:
        image = Image.open(image_path).convert("RGB")
        inputs = processor(images=image, return_tensors="pt").to(device)

        with torch.no_grad():
            caption_ids = model.generate(**inputs)
            caption = processor.decode(caption_ids[0], skip_special_tokens=True)
        
        return caption
    except Exception as e:
        print(f"Error generating caption: {e}")
        return None

def clean_text_for_filename(text):
    """Cleans text for safe file naming"""
    return "".join(c if c.isalnum() or c in [" ", "_"] else "" for c in text)[:50].replace(" ", "_")

def rename_image_by_caption(image_path):
    """Renames an image based on BLIP-2 generated caption"""
    caption = generate_image_caption(image_path)

    if caption:
        new_name = f"{clean_text_for_filename(caption)}.jpg"
    else:
        new_name = f"Image_{os.path.basename(image_path)}"

    new_path = os.path.join(os.path.dirname(image_path), new_name)
    os.rename(image_path, new_path)
    return new_path
