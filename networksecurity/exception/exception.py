import sys  # Importing sys to capture error details
from networksecurity.logging import logger  # Importing a custom logging module

# Custom Exception class for Network Security-related errors
class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details: sys):
        """
        Initializes the NetworkSecurityException with a custom error message and details.
        
        :param error_message: The message describing the error
        :param error_details: The `sys` module to extract traceback details
        """
        self.error_message = error_message  # Store the error message
        # Extracting traceback information from the error_details
        _,_,exc_tb = error_details.exc_info()  
        
        # Extract the line number where the exception occurred
        self.lineno = exc_tb.tb_lineno
        # Extract the file name where the exception occurred
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        """
        Returns a formatted error string when the exception is printed.
        """
        return "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
            self.file_name,  # Name of the file where the error occurred
            self.lineno,  # Line number of the error
            str(self.error_message)  # Original error message
        )

# Main script execution
if __name__ == "__main__":
    try:
        logger.logging.info("Enter the try block.")  # Log an informational message
        a = 1 / 0  # Deliberately causing a ZeroDivisionError
        print("This will not be printed", a)  # This line will not execute
    except Exception as e:
        # Catch any exception and raise a custom exception with detailed information
        raise NetworkSecurityException(e, sys)