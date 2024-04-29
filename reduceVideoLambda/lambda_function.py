import boto3
import time
import os
import subprocess
import shlex
import requests
import json


def handler(event, context):

    print(event)
    
    s3Bucket = "fs-transcoding-output"
    #s3Key = event["Key"]
    s3_client = boto3.resource('s3')
    my_bucket = s3_client.Bucket(s3Bucket)
    
    
    
    listOfFiles = []
    for record in event:
        fileName = record["convertedFragment"].split('/')[-1]
        s3Bucket = record["s3Bucket"]
        listOfFiles.append(fileName)
        my_bucket.download_file(record["convertedFragment"], "/tmp/" + fileName)
    
    #s3Key = "downconverts/"
    #extract the filename 
    
    
    
    #for objects in my_bucket.objects.filter(Prefix="downconverts/"):
    #    print(objects.key)
    #    fileName = objects.key.split('/')[-1]
    #    if(len(objects.key.split('/')[-1]) >0):
    #        my_bucket.download_file(objects.key, "/tmp/" + fileName)
    #        listOfFiles.append(fileName)
            
    print(listOfFiles) 
    listOfFiles.sort()
    
    with open('/tmp/listOfFragments.txt', 'w') as f:
        for line in listOfFiles:
            f.write(f"file /tmp/{line}\n")
    f.close()
    
    f = open('/tmp/listOfFragments.txt', 'r')
    file_contents = f.read()
    print(file_contents)
    
    
    ffmpeg_cmd = "/opt/bin/ffmpeg -f concat -safe 0 -i /tmp/listOfFragments.txt -c copy /tmp/output.mp4"
        
    command1 = shlex.split(ffmpeg_cmd)
    print(command1)
    p1 = subprocess.run(command1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(p1)
    
    s3_client.meta.client.upload_file('/tmp/output.mp4', s3Bucket, 'finalOutput/output.mp4')
    
    
