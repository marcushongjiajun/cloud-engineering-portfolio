import boto3
import os
from PIL import Image
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_image(input_path, output_path):
    """
    Opens an image and converts it to grayscale.
    This simulates 'processing' the data.
    """
    try:
        with Image.open(input_path) as img:
            logger.info(f"Processing image: {input_path}")
            grayscale = img.convert("L")
            grayscale.save(output_path)
            logger.info(f"Successfully saved to: {output_path}")
    except Exception as e:
        logger.error(f"Error processing image: {e}")

if __name__ == "__main__":
    # Local Test:
    # 1. Place a file named 'test.jpg' in your folder.
    # 2. Run: python src/app.py
    # 3. It will create 'prrocessed_test.jpg'

    in_file = "test.jpg"
    out_file = "processed_test.jpg"


    if os.path.exists(in_file):
        process_image(in_file, out_file)
    else:
        logger.warning(f"File {in_file} not found. Place an image in the root folder to test!")