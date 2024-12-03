import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from a .env file into the script.

MONGO_DB_URL = os.getenv("MONGO_DB_URL")  # Fetch the MongoDB connection URL from the environment variables.
print(MONGO_DB_URL)  # Print the MongoDB connection URL to verify it is loaded correctly.

import certifi  # Provides a set of trusted root certificates.
ca = certifi.where()  # Get the path to the trusted certificate authority file.

# Importing essential libraries for data manipulation and database interaction.
import pandas as pd  # For handling and processing tabular data.
import numpy as np  # For numerical operations (not used in the current script).
import pymongo  # For connecting to and interacting with MongoDB.

# Importing custom exception and logging classes from a project module.
from networksecurity.exception.exception import NetworkSecurityException  # Custom exception handling class.
from networksecurity.logging.logger import logging  # Custom logging utility.

class NetworkDataExtract():
    def __init__(self):
        try:
            pass  # No initialization logic yet.
        except Exception as e:
            raise NetworkSecurityException(e, sys)  # Raise a custom exception if initialization fails.

    def cv_to_json_convertor(self, file_path):
        """
        Converts a CSV file to a JSON-like dictionary structure for MongoDB insertion.
        Args:
            file_path: Path to the CSV file.
        Returns:
            A list of dictionaries, where each dictionary represents a record from the CSV.
        """
        try:
            data = pd.read_csv(file_path)  # Read the CSV file into a DataFrame.
            data.reset_index(drop=True, inplace=True)  # Reset the DataFrame's index.
            records = list(json.loads(data.T.to_json()).values())  # Convert the DataFrame into a list of dictionaries.
            return records  # Return the list of dictionaries.
        except Exception as e:
            raise NetworkSecurityException(e, sys)  # Raise a custom exception in case of an error.

    def insert_data_mongodb(self, records, database, collection):
        """
        Inserts records into a MongoDB collection.
        Args:
            records: List of dictionaries to insert.
            database: Name of the MongoDB database.
            collection: Name of the MongoDB collection.
        Returns:
            Number of records inserted.
        """
        try:
            self.database = database  # Set the database name.
            self.collection = collection  # Set the collection name.
            self.records = records  # Set the records to insert.

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)  # Connect to MongoDB using the URL from the environment variables.
            self.database = self.mongo_client[self.database]  # Access the specified database.

            self.collection = self.database[self.collection]  # Access the specified collection.
            self.collection.insert_many(self.records)  # Insert all records into the collection.
            return len(self.records)  # Return the number of records inserted.
        except Exception as e:
            raise NetworkSecurityException(e, sys)  # Raise a custom exception in case of an error.

if __name__ == "__main__":
    # File path to the CSV containing network data.
    FILE_PATH = "Network_Data\phisingData.csv"
    DATABASE = "PINAKI_AI"  # Name of the database to use.
    Collection = "NetworkData"  # Name of the collection to use.
    
    # Create an object of the NetworkDataExtract class.
    networkobj = NetworkDataExtract()

    # Convert the CSV data to a list of JSON-like records.
    records = networkobj.cv_to_json_convertor(file_path=FILE_PATH)
    print(records)  # Print the converted records for verification.

    # Insert the records into MongoDB and print the number of inserted records.
    no_of_records = networkobj.insert_data_mongodb(records, DATABASE, Collection)
    print(no_of_records)