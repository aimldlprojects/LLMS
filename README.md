Goodluck


def hello_world():
    return "Hello, World!"


# model.py
from hello_world import hello_world

class HelloWorldModel:
    def predict(self):
        return hello_world()

# Instantiate the model
model = HelloWorldModel()

# Save the model to disk (this is necessary for SageMaker)
import joblib
joblib.dump(model, 'model.joblib')


# deploy_script.py
from sagemaker.sklearn import SKLearnModel
from sagemaker import get_execution_role
import sagemaker

# Define the SageMaker execution role
role = get_execution_role()

# Create a SageMaker session
sagemaker_session = sagemaker.Session()

# Define the S3 location for storing the model artifact
model_s3_location = 's3://your-s3-bucket/model'

# Upload the model to S3
model_s3_path = sagemaker_session.upload_data(path='model.joblib', bucket='your-s3-bucket', key_prefix='model')

# Create an SKLearnModel
model = SKLearnModel(model_data=model_s3_path,
                    role=role,
                    entry_point='model.py',  # The script that loads your model
                    source_dir='.',  # Directory containing your model script and dependencies
                    framework_version='0.23-1')  # Your scikit-learn version

# Deploy the model to an endpoint
predictor = model.deploy(instance_type='ml.m4.xlarge', endpoint_name='hello-world-endpoint')


# Test the endpoint
import boto3
runtime = boto3.client('sagemaker-runtime')

response = runtime.invoke_endpoint(EndpointName='hello-world-endpoint',
                                   ContentType='application/json',
                                   Body='{}')

result = response['Body'].read()
print(result)

