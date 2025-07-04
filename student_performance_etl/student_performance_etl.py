# === Built-in and External Imports ===
import json
import os
import sys

import numpy as np

# Data handling libraries
import pandas as pd
import pymongo

# Load environment variables (e.g., DB connection strings) securely
from dotenv import load_dotenv

from student_performance_indicator.exception.exception import (
    StudentPerformanceException,
)

# Custom exception and logging modules (defined in your project)
from student_performance_indicator.logger.logger import logger

load_dotenv()

# Get MongoDB connection string from .env file
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)  # Remove or log securely in production

# For validating SSL certificates during MongoDB connection
import certifi

ca = certifi.where()


# === Core Class for Data Extraction and MongoDB Insertion ===
class StudentPerformanceExtract:
    """
    Handles reading network-related CSV data and inserting it into MongoDB.
    """

    def __init__(self):
        """
        Constructor for any future setup logic.
        """
        try:
            pass  # Placeholder
        except Exception as e:
            logger.error("Initialization failed", exc_info=True)
            raise StudentPerformanceException(e, sys)

    def cv_to_json_convertor(self, file_path):
        """
        Reads a CSV file and converts it to a list of dictionaries (JSON-like format).

        Args:
            file_path (str): Path to the CSV file.

        Returns:
            list: List of records, each as a dictionary (ready for MongoDB insertion).
        """
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            logger.error("Failed to convert CSV to JSON", exc_info=True)
            raise StudentPerformanceException(e, sys)

    def insert_data_to_mongodb(self, records, database, collection):
        """
        Inserts a list of dictionaries into a MongoDB collection.

        Args:
            records (list): List of JSON-like records.
            database (str): Name of the MongoDB database.
            collection (str): Target collection name.

        Returns:
            int: Number of records successfully inserted.
        """
        try:
            # Establish MongoDB client connection
            mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)

            # Access the target database and collection
            db = mongo_client[database]
            collection = db[collection]

            # Insert records into the collection
            collection.insert_many(records)

            return len(records)
        except Exception as e:
            logger.error("Error inserting records into MongoDB", exc_info=True)
            raise StudentPerformanceException(e, sys)


# === Entry point for script execution ===
if __name__ == "__main__":
    FILE_PATH = "data/stud.csv"  # Fixed backslash for cross-platform
    DATABASE = "Iyan-coder"
    COLLECTION = "StudentPerformanceData"

    network_obj = StudentPerformanceExtract()

    # Convert CSV to JSON
    records = network_obj.cv_to_json_convertor(FILE_PATH)
    print(records)

    # Insert into MongoDB
    no_of_records = network_obj.insert_data_to_mongodb(records, DATABASE, COLLECTION)
    print(f"{no_of_records} records inserted.")
    logger.info(f"{len(records)} records inserted into {DATABASE}.{COLLECTION}")
