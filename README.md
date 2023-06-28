<<<<<<< HEAD
# Capstone_part1

# COVID-19 Data Import Script

This script imports COVID-19 data from a CSV file into a PostgreSQL database. It utilizes the `psycopg2` library to establish a connection with the database and the `pandas` library to read the CSV file.

## Prerequisites

- Python 3.x
- PostgreSQL database server
- Required Python libraries: `psycopg2`, `pandas`

## Setup

1. Create a database and a table called covid_19_data to hold the data in postgresql.
   
3. Install the required Python libraries:
   pip install psycopg2 pandas

Update the connection details in the script:
  conn = get_db_connection('<host>', '<database>', '<user>', '<password>')
  Replace <host>, <database>, <user>, and <password> with your PostgreSQL server details.
  
The script will read the data from the provided URL and insert it into the covid_19_data table in the specified database.

Notes
The script assumes that the provided CSV file has columns with the following names: 'SNo', 'ObservationDate', 'Province', 'Country', 'LastUpdate', 'Confirmed', 'Deaths', 'Recovered'. If your CSV file has different column names, please adjust the script accordingly.
The 'ObservationDate' column in the CSV file is expected to be in the format '%m/%d/%Y'. If your date format is different, modify the datetime.strptime() function accordingly.
=======
# Capstone_part2
>>>>>>> origin/main
