class InvalidDatasetName(Exception):
    """
    Exception raised for invalid dataset names.

    Attributes:
        message (str): Explanation of the error.
    
    Methods:
        __init__(self, message: str) -> None:
            Initializes the exception with a message.
    """
    
    def __init__(self, message: str) -> None:
        """
        Initialize the InvalidDatasetName exception.

        Parameters:
            message (str): Explanation of the error.
        """
        super().__init__(message)
