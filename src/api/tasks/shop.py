from celery import Celery
import os, sys

sys.path.append(os.path.join(sys.path[0][:-9]))

from database import s3, celery
from config import REDIS_PORT, BUCKET


#@celery.task
def push_photo(photo, id):


    for key in s3.list_objects(Bucket='for9may'):
        print(key)

    #s3.upload_file('utka.jpg', 'for9may', 'utka.jpg')
    #s3.put_object(Bucket=BUCKET, Key=f"{id}_main.jpg", Body=photo)
    #s3.put_object(Bucket='for9may', Key='Test', Body=("егор лох"))
    
    return 0

push_photo(23, 21)
