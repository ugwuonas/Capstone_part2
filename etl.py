import os
import logging
from datetime import date
import json
import pandas as pd
import psycopg2
import requests
from dotenv import load_dotenv
from util import get_s3_connection, get_redshift_connection


# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)


def extract_raw_data(url, headers, querystring):
    response = requests.get(url=url, headers=headers, params=querystring)
    raw_data = response.json()

    s3_hook = get_s3_connection()  # Connect to s3

   # Stage raw data to s3
    s3_hook.load_string(json.dumps(raw_data), f"raw_jobs_data_{date.today()}.json", bucket_name='rawjobsdata')


def transform_data():
    s3_hook = get_s3_connection()  # Connect to s3

   #Get raw data from the s3 bucket
    raw_data = json.loads(s3_hook.read_key(f"raw_jobs_data_{date.today()}.json", bucket_name='rawjobsdata'))

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

   # Stage csv data to s3
    s3_hook.load_string(csv_data, f"transformed_jobs_data_{date.today()}.csv", bucket_name='transformedjobsdata')


def load_data_to_redshift():
    try:
        # Connect to redshift
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
        logging.info("Data loaded to Redshift successfully.")
        
    except psycopg2.Error as e:
        logging.error("Error connecting to Redshift:", str(e))
    except Exception as e:
        logging.exception("An error occurred:", str(e))
        

