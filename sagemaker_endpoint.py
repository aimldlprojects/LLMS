# approach 1
from sagemaker.sklearn import SKLearn
from sagemaker import get_execution_role
import sagemaker

# Define the SageMaker execution role
role = get_execution_role()

# Create a SageMaker session
sagemaker_session = sagemaker.Session()

# Define the S3 location for storing the script
script_s3_location = 's3://your-s3-bucket/scripts'

# Upload the script to S3
script_s3_path = sagemaker_session.upload_data(path='hello_world.py', bucket='your-s3-bucket', key_prefix='scripts')

# Create an SKLearn estimator with a smaller instance type
estimator = SKLearn(entry_point='hello_world.py',
                    role=role,
                    source_dir='.',
                    framework_version='0.23-1',
                    instance_type='ml.t2.micro',  # Use a smaller instance type
                    sagemaker_session=sagemaker_session)

# Deploy the script as an endpoint
predictor = estimator.deploy(instance_type='ml.t2.micro', endpoint_name='hello-world-endpoint')

# Assuming you have already deployed the endpoint and have the 'predictor' object

# Sample input data
input_data = '{"input": "sample_input_data"}'

# Make a prediction using the deployed endpoint
result = predictor.predict(input_data)

# Print the result
print(result)



# Approach 2
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
