
def lambda_handler(event, context):

    print(json.dumps(event))

    record = event['Records'][0]
    
    s3bucket = record['s3']['bucket']['name']
    s3object = record['s3']['object']['key']
    
    s3Path = "s3://" + s3bucket + "/" + s3object
    jobName = s3object + '-' + 'transcript'

    client = boto3.client('transcribe')

    response = client.start_transcription_job(
        TranscriptionJobName=jobName,
        LanguageCode='en-US',
        MediaFormat='mp3',
        Media={
            'MediaFileUri': s3Path
        }
    )
    
    status = response['TranscriptionJob']['TranscriptionJobStatus']
    
    job_status = None
    
    while job_status not in ['COMPLETED', 'FAILED']:
        job = client.get_transcription_job(TranscriptionJobName=jobName)
        job_status = job['TranscriptionJob']['TranscriptionJobStatus']
        if job_status == 'COMPLETED':
            transcript_file_uri = job['TranscriptionJob']['Transcript']['TranscriptFileUri']
            transcript_response = requests.get(transcript_file_uri)
            data = json.loads(transcript_response.text)
            transcript = data['results']['transcripts'][0]['transcript']
            print(transcript)
            uploadByteStream = bytes(json.dumps(transcript).encode('UTF-8'))
            
            s3_client = boto3.client('s3')
            s3_bucket = 'transcript-file-bucket'
            s3_key = f"{jobName}.txt"
            s3_client.put_object(Bucket=s3_bucket, Key=s3_key, Body=uploadByteStream)
        elif job_status == 'FAILED':
            print('Transcription job failed')
            break
    
    return {
        'statusCode' : 200,
        'body' : ''
    }
