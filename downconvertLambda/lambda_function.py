import boto3
import time
import os
import subprocess
import shlex
import requests
import json

def handler(event, context):
    
    print(event)
    s3Key = event["ItemSelector"]["Key"]
    print("S3Key" + s3Key)
    
    #s3Key = "splits/output000.mp4"
    #extract the filename 
    
    videoFileName = s3Key.split('/')[-1]
    #videoFileNameWithoutExtension = videoFileName.split('.')[0]
    
    
    #s3Bucket = "fs-transcoding-output"
    s3Bucket = event["ItemSelector"]["s3Bucket"]
    
    s3 = boto3.resource('s3')
    
    #local_file_name = '/tmp/output000.mp4'
    local_file_name = '/tmp/' + videoFileName
    
    s3.Bucket(s3Bucket).download_file(s3Key, local_file_name)
    
    downConvertedFilename = "dc_" + videoFileName
    ffmpeg_cmd = "/opt/bin/ffmpeg -i " + local_file_name + " -b:v 0.5M /tmp/" + downConvertedFilename
    
    command1 = shlex.split(ffmpeg_cmd)
    print(command1)
    p1 = subprocess.run(command1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #print(p1)
    #print("audio output")
    
    #outputBucketName = os.environ['targetS3']
    #rint(outputBucketName)
    
    s3_client = boto3.client('s3')
    
    s3.meta.client.upload_file('/tmp/' + downConvertedFilename, s3Bucket, 'downconverts/' + downConvertedFilename)
    
    return {
        "statusCode" : 200,
        "convertedFragment" : 'downconverts/' + downConvertedFilename,
        "s3Bucket" : s3Bucket
    }
    
    