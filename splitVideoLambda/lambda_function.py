import boto3
import time
import os
import subprocess
import shlex
import requests
import json
import glob


def handler(event, context):

#ffmpeg -i input.mp4 -c copy -map 0 -segment_time 00:20:00 -f segment output%03d.mp4

    print(event)
    #s3Key = event["Key"]
    
    #s3Key = "originalVideo/ToS.mp4"
    #s3BucketName = "fs-transcoding-output"
    
    s3Key = event["s3Key"]
    s3BucketName = event["s3Bucket"]
    
    #sample input event
    #{"s3Key": "originalVideo/ToS.mp4", "s3Bucket": "fs-transcoding-output"}
    
    s3Prefix = "splits"
    #extract the filename 
    
    s3_client = boto3.resource('s3')
    my_bucket = s3_client.Bucket('fs-transcoding-output')
    videofileName = s3Key.split('/')[-1]
    
    s3_client.Bucket(s3BucketName).download_file(s3Key, "/tmp/output.mp4")
    
    ffmpeg_cmd = "ffmpeg -i /tmp/output.mp4 -c copy -map 0 -segment_time 00:00:05 -f segment /tmp/split%03d.mp4"
        
    command1 = shlex.split(ffmpeg_cmd)
    print(command1)
    p1 = subprocess.run(command1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(p1)
    
    splitFiles = glob.glob("/tmp/split*.mp4")
    fileNameList = []
    print(splitFiles)
    for filename in splitFiles:
        print(filename)
        
        s3_client.meta.client.upload_file(filename, s3BucketName, s3Prefix + "/" + os.path.basename(filename))
        fileNameList.append(s3Prefix + "/" + os.path.basename(filename))
    
    returnJson = {}
    returnJson['fragmentList'] = fileNameList
    returnJson["s3Bucket"] = s3BucketName
    
    return {
        'statusCode': 200,
        'body': returnJson
    }
    
    