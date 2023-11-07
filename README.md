# LLMS

import requests
import boto3
from botocore.exceptions import NoCredentialsError

# Replace these with your S3 bucket and PDF URL
s3_bucket_name = 'your-s3-bucket-name'
pdf_url = 'https://example.com/your-pdf-url.pdf'

def copy_pdf_to_s3(pdf_url, s3_bucket_name):
    try:
        # Get the PDF content from the URL
        response = requests.get(pdf_url)
        pdf_content = response.content

        # Initialize the S3 client
        s3 = boto3.client('s3')

        # Specify the S3 object key (file name in S3)
        object_key = 'your-pdf-file-name.pdf'

        # Upload the PDF content to S3 bucket
        s3.upload_fileobj(
            Fileobj=io.BytesIO(pdf_content),
            Bucket=s3_bucket_name,
            Key=object_key
        )

        print(f'PDF file successfully copied to S3 bucket: s3://{s3_bucket_name}/{object_key}')
    except NoCredentialsError:
        print('AWS credentials are not configured.')
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    copy_pdf_to_s3(pdf_url, s3_bucket_name)

