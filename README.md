# Job Board Data Pipeline

This repository contains code for a data pipeline that extracts job posting data from a public API, transforms it, and loads it into an Amazon Redshift data warehouse. The pipeline is designed to extract daily job posting data for Data Engineer and Data Analyst roles in Canada.

## Files

- `etl.py`: Contains functions for data extraction, transformation, and loading. It connects to the necessary services such as S3 and Redshift using the credentials provided in the environment variables.
- `util.py`: Provides utility functions for establishing connections to S3 and Redshift. It also configures logging to capture relevant information and errors during the execution of the pipeline.
- `main.py`: Defines an Apache Airflow DAG (Directed Acyclic Graph) that orchestrates the execution of the data pipeline. It schedules the pipeline to run daily and sets up the dependencies between tasks.
- `README.md`: This file, provides an overview of the repository and its contents.
- `pipeline_architecture.png`: A pipeline architecture diagram illustrating the flow of data and the components involved in the pipeline.

  
## Prerequisites
Before using the data pipeline, ensure you have the following prerequisites:

- Python: Make sure you have Python 3.x installed on your system.
- AWS Account: You need an AWS account to access Amazon S3 and Amazon Redshift services. Obtain your AWS access key ID and secret access key.
- RapidAPI Account: Create an account on RapidAPI (https://rapidapi.com) to obtain the API key required to access the job posting API.
- Apache Airflow: Set up an Apache Airflow environment to schedule and execute the data pipeline. Refer to the Airflow documentation for installation instructions.

## Usage

To use the data pipeline, follow these steps:

1. Set up the required environment variables: 
   - `aws_access_key_id`: Access key ID for AWS.
   - `aws_secret_access_key`: Secret access key for AWS.
   - `redshift_user`: Username for connecting to Amazon Redshift.
   - `redshift_password`: Password for connecting to Amazon Redshift.
   - `rapidAPI-key`: API key for accessing the job posting API.

2. Install the necessary dependencies: 
   - Make sure you have Python installed on your system.
   - Use `pip` or `conda` to install the required packages.

3. Customize the pipeline parameters (e.g., API URL, query parameters) in `main.py` if needed.

4. Run the data pipeline using Apache Airflow:
   - Set up an Airflow environment and configure it to use the DAG defined in `main.py`.
   - Ensure that the necessary Airflow connections and variables are set up (e.g., AWS credentials, Redshift connection).
   - Start the Airflow scheduler to trigger the pipeline at the scheduled intervals.

### Notes

- The data extraction step fetches job posting data from the specified API based on the provided query parameters.
- The extracted raw data is stored in an S3 bucket named `rawjobsdata` in JSON format.
- The transformation step processes the raw data and creates a transformed dataset containing specific columns.
- The transformed data is saved in an S3 bucket named `transformedjobsdata` in CSV format.
- The final step loads the transformed data from the S3 bucket into an Amazon Redshift table named `transformed_jobs`.
- Logging is configured to capture information and errors during the execution of the pipeline. The logging level is set to `INFO` to provide general progress information.
  
## Troubleshooting
If you encounter any issues while running the data pipeline, consider the following troubleshooting steps:

- Verify Environment Variables: Double-check that all the required environment variables are set correctly and have the appropriate values.
- Check Connectivity: Ensure that you have an active internet connection and can access the job posting API and the AWS services (S3, Redshift) from your environment.
- Review Logging Output: If the pipeline fails or produces unexpected results, review the log output to identify any error messages or warnings. The logs can provide insights into the root cause of the issue.
- Verify Dependencies: If you have added any additional dependencies beyond the standard library, make sure they are installed correctly. Check that the required versions of the packages are installed and compatible.
- Debugging: If the issue persists and you are unable to identify the problem, consider adding additional debug statements or using a debugger to inspect the code during execution. This can help pinpoint the source of the issue.

Please refer to the individual files for more detailed information on the implementation of each step of the pipeline.

If you have any questions or encounter any issues, feel free to reach out. Happy data pipelining!

## Disclaimer
This code is provided as-is without any warranties. Use it at your own risk. The author is not responsible for any damages or data loss caused by running this code.
