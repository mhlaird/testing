from PIL import Image
import os

def clean_png(filepath):
    try:
        # Open the image
        with Image.open(filepath) as img:
            # Convert to RGBA if not already
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Create a new image without the ICC profile
            cleaned = Image.new('RGBA', img.size)
            cleaned.paste(img)
            
            # Save back to the same location
            cleaned.save(filepath, 'PNG', optimize=True)
            print(f"Cleaned: {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.PNG')):
                filepath = os.path.join(root, file)
                clean_png(filepath)

if __name__ == "__main__":
    assets_dir = "assets/images"
    print(f"Processing PNG files in {assets_dir}...")
    process_directory(assets_dir)
    print("Done!") 