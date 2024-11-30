import logging
import os

def setup_logger(log_file="app.log", level=logging.INFO):
    """
    Sets up a centralized logger that can be used across multiple modules.

    Args:
        log_file (str): File to which logs should be written.
        level (int): Logging level (e.g., logging.INFO, logging.DEBUG).

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Create a directory for logs if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Get a named logger (root logger for simplicity)
    logger = logging.getLogger("shared_logger")
    
    if not logger.hasHandlers():  # Avoid adding multiple handlers
        # Set logging level
        logger.setLevel(level)

        # Define the logging format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
