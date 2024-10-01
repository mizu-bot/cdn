

import dotenv
dotenv.load_dotenv()
import os
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

def getAllImages():
    try:
        directories = os.listdir("cards")
        for i in range(startPoint, startPoint + 26):
            anime = directories[i]
            print(f"STARTING {anime.upper()}")
            images = os.listdir(f"cards/{anime}")
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
    except Exception as e:
        print(e)
        
getAllImages()