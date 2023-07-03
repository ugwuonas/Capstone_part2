import csv
import os
import boto3
from datetime import date
import psycopg2
import requests
import json
import pandas as pd
import redshift_connector

def get_s3_connection(access_key_id, secret_access_key, region):
    s3 = boto3.client(
            's3',
            region_name = region,
            aws_access_key_id = access_key_id,
            aws_secret_access_key = secret_access_key
            )
    return s3

def get_redshift_connection(host, port, database, user, password):
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        print("Connected to Redshift")
        return conn
    
    except Exception as e:
        print(f"Error connecting to Redshift: {e}")
        return None


def load_data_to_s3(bucket, key, body):
    s3 = boto3.client('s3')

    try:
        s3.put_object(Bucket=bucket, Key=key, Body=body)
        print(f"Data uploaded successfully to S3 bucket: {bucket} as object: {key}")
    except Exception as e:
        print(f"Error uploading data to S3 bucket: {bucket}")
        print(e)