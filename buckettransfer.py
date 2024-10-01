import dotenv
dotenv.load_dotenv()
import os
import uuid
import base64
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
R2_ENDPOINT_URL = f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY")
R2_SECRET_KEY = os.getenv("R2_SECRET_KEY")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")
UUID_LENGTH = int(os.getenv("UUID_LENGTH"))

def get_r2_client():
    return boto3.client('s3',
        endpoint_url=R2_ENDPOINT_URL,
        aws_access_key_id=R2_ACCESS_KEY,
        aws_secret_access_key=R2_SECRET_KEY)

async def upload(b64, image_name=str(uuid.uuid4())[:UUID_LENGTH], useUUID=False):
    try:
        # Decode the base64 string into binary
        image = base64.b64decode(b64)
        
        if (useUUID):
            image_name += f"-{str(uuid.uuid4())[:UUID_LENGTH]}"
        
        # Get S3 (R2) client
        s3_client = get_r2_client()
        
        # Upload the image as .png to the R2 bucket
        response = s3_client.put_object(
            Bucket=R2_BUCKET_NAME,
            Key=f'live/{image_name}.png',
            Body=image,
            ContentType='image/png'
        )
        
        return f"https://mizu.cards/{image_name}.png"

    except NoCredentialsError:
        print("Error: Unable to find credentials")
    except ClientError as e:
        print(f"Client error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
def getAllImages():
    try:
        total = 0
        directories = os.listdir("cards")
        print(len(directories))
        for anime in directories:
            images = os.listdir(f"cards/{anime}")
            total += len(images)
            continue
            for image in images:
                with open(f"cards/{anime}/{image}", "rb") as f:
                    print(anime + "/" + image)
                    imgData = f.read()
                    s3_client = get_r2_client()
                    response = s3_client.put_object(
                        Bucket=R2_BUCKET_NAME,
                        Key=f'{anime}/{image}',
                        Body=imgData,
                        ContentType='image/png'
                    )
                    print(f"https://mizu.cards/{anime}/{image}")
        
        print(total)
    except Exception as e:
        print(e)
        
getAllImages()


def deleteAll():
    try:
        s3 = boto3.resource('s3',
            endpoint_url=R2_ENDPOINT_URL,
            aws_access_key_id=R2_ACCESS_KEY,
            aws_secret_access_key=R2_SECRET_KEY)
        bucket = s3.Bucket(R2_BUCKET_NAME)
        bucket.objects.all().delete()
    except Exception as e:
        print(e)

def generateScripts():
    for i in range(0, 10):
        with open(f"template.py", "r") as template:
            script = template.read()
            
            script = f"startPoint = {i*26}\n\n" + script
            
            with open(f"scripts/upload{i+1}.py", "w") as f:
                f.write(script)
                f.close()
                
generateScripts()