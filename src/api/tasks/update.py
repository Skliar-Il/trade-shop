from celery import Celery
from tempfile import SpooledTemporaryFile
from io import BytesIO
from PIL import Image
import os, sys, base64

sys.path.append(os.path.join(sys.path[0][:-9]))

from database import s3, celery
from config import REDIS_PORT, BUCKET


@celery.task
async def push_photos(photos, id):
    
    for i in range(len(photos)):
        s3.put_object(Bucket=BUCKET, Key=f"{id}_{i+1}_photo.jpg", Body=photos[i].file)
    
    return 0

@celery.task
async def push_photo(photo, id, ident_id):
    s3.put_object(Bucket=BUCKET, Key=f"{id}_{ident_id}_photo.jpg", Body=photo.file)
    
    return 0

