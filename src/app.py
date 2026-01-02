import boto3
import os
from PIL import Image
import logging
from botocore.exceptions import ClientError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the S3 client
s3_client = boto3.client('s3')

def process_image_from_s3(bucket_name, object_key, output_bucket):
    """
    Downloads an image from S3, makes it grayscale, and uploads it back.
    """
    local_input = f"/tmp/{object_key}"
    local_output = f"/tmp/processed-{object_key}"
    
    try:
        # Step A: Download from S3
        logger.info(f"Downloading {object_key} from {bucket_name}...")
        s3_client.download_file(bucket_name, object_key, local_input)
        
        # Step B: Process locally (using working logic)
        with Image.open(local_input) as img:
            grayscale = img.convert("L")
            grayscale.save(local_output)
        
        # Step C: Upload back to the 'processed' bucket
        logger.info(f"Uploading to {output_bucket}...")
        s3_client.upload_file(local_output, output_bucket, f"processed-{object_key}")
        
        logger.info("Task completed successfully!")
    
    except ClientError as e:
        # Log specific AWS errors (e.g., Access Denied or 404)
        logger.error(f"AWS Error: {e.response['Error']['Code']} - {e.response['Error']['Message']}")
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        # Cleanup
        for f in [local_input, local_output]:
            if os.path.exists(f):
                os.remove(f)

if __name__ == "__main__":
    # For testing, we use environmental variables (Best Practice)
    SOURCE_BUCKET = os.environ.get('UPLOAD_BUCKET', 'your-unique-upload-bucket')
    DEST_BUCKET = os.environ.get('PROCESSED_BUCKET', 'your-unique-processed-bucket')
    FILE_TO_TEST = 'test.jpg'
 

    process_image_from_s3(SOURCE_BUCKET, FILE_TO_TEST, DEST_BUCKET)