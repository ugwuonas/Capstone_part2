import os
import logging
import boto3
import psycopg2


# Configure logging
logging.basicConfig(level=logging.INFO)

def get_s3_connection():
    try:
       
        s3 = boto3.client(
            service_name='s3',
            region_name='ca-central-1',
            aws_access_key_id = os.getenv("aws_access_key_id"),
            aws_secret_access_key= os.getenv("aws_secret_access_key")
        )
        
        logging.info("Connected to S3 successfully")
        return s3
    except Exception as e:
        logging.error(f"Error connecting to S3: {e}")
        return None


def get_redshift_connection():
    try:
        
        conn = psycopg2.connect(
            host='redshift-cluster-1.casnx5izlkyy.ca-central-1.redshift.amazonaws.com',
            port=5439,
            database='dev',
            user= os.getenv("redshift_user"),
            password= os.getenv("redshift_password")
        )
        logging.info("Connected to Redshift successfully")
        return conn
    
    except Exception as e:
        logging.error(f"Error connecting to Redshift: {e}")
        return None







