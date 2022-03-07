
## HTML To PDF Lambda, Serverless, python with wkhtmltox

### Installation required :
- https://www.serverless.com/ 
- Python3.8
- Install PIP
- git
- node12.x

### Go to root directory and follow steps :
- virtualenv env - to create virtual env
- source env/Scripts/activate
- pip install -r requirements.txt - to install python dependencies
- npm install

### Configuration ServerLess :
- serverless config credentials --provider aws --key dhsfkjhdfjhksdhf --secret 65454sdfsdfsd45sd4fsdf --overwrite
- sls deploy

### This function will return sign url of s3