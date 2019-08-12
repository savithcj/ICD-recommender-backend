import boto3
import os
s3 = boto3.resource('s3')


def readFileFromS3(filename):
    print("Reading", filename, "from S3")
    s3client = boto3.client(
        's3',
        aws_access_key_id=os.environ['S3_ACCESS_KEY'],
        aws_secret_access_key=os.environ['S3_SECRET_ACCESS_KEY']
    )
    fileobj = s3client.get_object(
        Bucket='icd-django-data',
        Key=filename)
    filedata = fileobj['Body'].read()
    contents = filedata.decode('utf-8').split('\n')
    if contents[-1] == '':
        del contents[-1]
    return contents
