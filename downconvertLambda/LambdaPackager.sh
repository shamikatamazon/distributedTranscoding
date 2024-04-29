mkdir packages
pip3 install --target packages/ requests
pip3 install --target packages/ boto3
pip3 install --target packages/ shlex
pip3 install --target packages/ subprocess
pip3 install --target packages/ os
pip3 install --target packages/ json
cd packages

zip -r ../my-deployment-package.zip .
cd ..
zip -g my-deployment-package.zip lambda_function.py 

aws s3 cp my-deployment-package.zip s3://fs-transcoding-output/lambdaCode/

aws lambda update-function-code --function-name video_downconverter --s3-bucket fs-transcoding-output --s3-key lambdaCode/my-deployment-package.zip