import json
import uuid
import boto3
import base64
from io import BytesIO
s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get the MP3 file data from the event
    mp3_data = base64.b64decode(event['mp3Data'])
    mp3_name = event['mp3Name']
    
    new_mp3_name = mp3_name + '-' + str(uuid.uuid4()) +'.mp3'
    
    # Upload the MP3 file to the S3 bucket
    bucket_name = "audio-transcribe-textfile-bucket"
    s3.upload_fileobj(BytesIO(mp3_data), bucket_name, new_mp3_name)
    
    output_bucket_name = 'comprehend-keyphrases-bucket'
    output_key = new_mp3_name + '-transcript' + '-comprehend' + '.txt'
    # print(output_key)
    # waiter = s3.get_waiter('object_exists')
    # waiter.wait(Bucket = output_bucket_name, Key = output_key)
    
    #  # Get the result data from the S3 object
    # result_object = s3.get_object(Bucket=output_bucket_name, Key=output_key)
    # result_data = result_object['Body'].read().decode('utf-8')
    object_key = {
        "object_key": output_key
    }
  # Return the result data to the client
    return {
        'statusCode': 200,
        'body': object_key
    }
