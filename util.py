import boto3
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_s3_connection():
    try:
       
        s3 = boto3.resource(
            service_name='s3',
            region_name='ca-central-1',
            aws_access_key_id = os.environ['aws_access_key_id'],
            aws_secret_access_key= os.environ['aws_secret_access_key']
        )
        print("Connected to S3 successfully")
        return s3
    except Exception as e:
        print(f"Error connecting to S3: {e}")
        return None


def get_redshift_connection():
    try:
        
        conn = psycopg2.connect(
            host='redshift-cluster-2.cfz4dilotntk.ca-central-1.redshift.amazonaws.com',
            port=5439,
            database='dev',
            user= os.environ['redshift_user'],
            password= os.environ['redshift_password']
        )
        print("Connected to Redshift successfully")
        return conn
    
    except Exception as e:
        print(f"Error connecting to Redshift: {e}")
        return None


def load_data_to_s3(bucket, key, body):
    s3_client = get_s3_connection()

    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=bucket, Key=key, Body=body)
        print(f"Data uploaded successfully to S3 bucket: {bucket} as object: {key}")
    except Exception as e:
        print(f"Error uploading data to S3 bucket: {bucket}")
        print(e)






