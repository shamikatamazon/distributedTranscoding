mkdir packages
pip3 install --target packages/ requests
pip3 install --target packages/ boto3
pip3 install --target packages/ shlex
pip3 install --target packages/ subprocess
pip3 install --target packages/ os
pip3 install --target packages/ json
pip3 install --target packages/ glob
cd packages

zip -r ../reduce-deployment-package.zip .
cd ..
zip -g reduce-deployment-package.zip lambda_function.py 

aws s3 cp reduce-deployment-package.zip s3://fs-transcoding-output/lambdaCode/

aws lambda update-function-code --function-name VideoReducer --s3-bucket fs-transcoding-output --s3-key lambdaCode/reduce-deployment-package.zip