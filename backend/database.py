

import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv


# Load database credentials from the .env file
env_path = Path(__file__).with_name(".env")
load_dotenv(dotenv_path=env_path)


def get_connection():

    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    return connection
