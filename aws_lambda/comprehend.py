import boto3
import uuid
import json


s3 = boto3.client('s3')
comprehend = boto3.client('comprehend')                                                                                                                        

def lambda_handler(event, context):
    print(json.dumps(event))
    record = event['Records'][0]
    
    s3bucket = record['s3']['bucket']['name']
    s3object = record['s3']['object']['key']
    
    new_s3object = s3object[:-4]
    
    jobName = new_s3object + '-' + 'comprehend' 
    
    response = s3.get_object(Bucket = s3bucket, Key = s3object)
    text = response['Body'].read().decode('utf-8')
    
    response = comprehend.detect_key_phrases(
        Text=text,
        LanguageCode='en'
    )

    # Extract the list of key phrases from the response object
    key_phrases = [kp['Text'] for kp in response['KeyPhrases']]
    
    uploadByteStream = bytes(json.dumps(key_phrases).encode('UTF-8'))
    
    s3_client = boto3.client('s3')
    s3_bucket = 'comprehend-keyphrases-bucket'
    s3_key = f"{jobName}.txt"
    s3_client.put_object(Bucket=s3_bucket, Key=s3_key, Body=uploadByteStream)
    
    print(key_phrases)
