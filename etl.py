import csv
import os
import boto3
from datetime import date
import psycopg2
import requests
import json
import pandas as pd
from util import get_s3_connection, load_data_to_s3, get_redshift_connection
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def extract_raw_data(url, headers, querystring):
    response = requests.get(url=url, headers=headers, params=querystring)
    raw_data = response.json()
    return raw_data

def transform_raw_data():
    transformed_data_list = []
    for i in raw_data["data"]:
        transformed_data_list.append({
            "employer_website": i["employer_website"],
            "job_id": i["job_id"],
            "job_employment_type": i["job_employment_type"],
            "job_title": i["job_title"],
            "job_apply_link": i["job_apply_link"],
            "job_description": i["job_description"],
            "job_city": i["job_city"],
            "job_country": i["job_country"],
            "job_posted_at_timestamp": i["job_posted_at_timestamp"],
            "employer_company_type": i["employer_company_type"]
        })

    transformed_data_df = pd.DataFrame(transformed_data_list)
    # Save the DataFrame as a CSV file in memory
    csv_data = transformed_data_df.to_csv(index=False)
    return csv_data

def stage_raw_data():
    # Stage the raw data in S3 bucket
    load_data_to_s3('rawjobsdata', f"raw_jobs_data_{date.today()}.json", body=json.dumps(raw_data))

def stage_transformed_data():
    # Stage transformed data in S3 bucket

    load_data_to_s3('transformedjobsdata', f"transformed_jobs_data_{date.today()}.csv", body=transformed_data)


def load_data_to_redshift():
    try:
        # Load data to Redshift
        redshift_conn = get_redshift_connection()
        redshift_cur = redshift_conn.cursor()
        
        # Create the target table in Amazon Redshift
        create_table_query = """
            CREATE TABLE IF NOT EXISTS transformed_jobs (
                employer_website VARCHAR,
                job_id VARCHAR,
                job_employment_type VARCHAR,
                job_title VARCHAR,
                job_apply_link VARCHAR,
                job_description VARCHAR(8000),
                job_city VARCHAR,
                job_country VARCHAR,
                job_posted_at_timestamp VARCHAR,
                employer_company_type VARCHAR
            )
        """
        redshift_cur.execute(create_table_query)

        copy_query = f"""
            COPY transformed_jobs
            FROM 's3://transformedjobsdata/transformed_jobs_data_{date.today()}.csv'
            CREDENTIALS 'aws_access_key_id={os.environ['aws_access_key_id']};aws_secret_access_key={os.environ['aws_secret_access_key']}'
            FORMAT AS CSV
            IGNOREHEADER 1
        """
        redshift_cur.execute(copy_query)

        redshift_conn.commit()
        redshift_conn.close()
        print("Data loaded to Redshift successfully.")
        
    except psycopg2.Error as e:
        print("Error connecting to Redshift:", str(e))
    except Exception as e:
        print("An error occurred:", str(e))
        



    # API details
url = "https://jsearch.p.rapidapi.com/search"
querystring = {"query": "Data Engineer, Data Analyst", "page": "1", "num_pages": "1", "date_posted": "today"}
headers = {
    "X-RapidAPI-Key": os.environ['rapidAPI-key'],
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}
# Establish S3 Connection
region = "ca-central-1"
access_key_id = 'AKIAYYI7KKEMACJKL4E5'
secret_access_key = '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'

# Establish Redshift Connection
redshift_host = 'redshift-cluster-2.cfz4dilotntk.ca-central-1.redshift.amazonaws.com'
redshift_port = 5439
redshift_database = 'dev'
redshift_user = 'awsuser'
redshift_password = 'Learn1n9'

raw_data = extract_raw_data(url, headers, querystring)

transformed_data = transform_raw_data()

stage_raw_data()

stage_transformed_data()

load_data_to_redshift()