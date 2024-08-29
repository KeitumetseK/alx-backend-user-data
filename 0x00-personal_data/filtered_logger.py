#!/usr/bin/env python3
"""Module for handling personal data with logging, database connection,
and filtering."""

import re
import logging
import os
import mysql.connector
from typing import List, Tuple

# Constants
PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """Return the log message with obfuscated fields."""
    pattern = '|'.join([f'{field}=[^{separator}]*' for field in fields])
    return re.sub(pattern, lambda m: f"{m.group(0).split('=')[0]}={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize the formatter with fields to redact."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record by obfuscating sensitive fields."""
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Create and return a logger with redaction for PII fields."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connect to the database using credentials from environment variables."""
    db_user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        database=db_name
    )


def main() -> None:
    """Read data from the database and log it with sensitive fields obfuscated."""
    db = get_db()
    cursor = db.cursor()

    query = "SELECT name, email, phone, ssn, password, ip, last_login, user_agent FROM users"
    cursor.execute(query)

    logger = get_logger()
    for row in cursor:
        message = f"name={row[0]};email={row[1]};phone={row[2]};ssn={row[3]};password={row[4]};ip={row[5]};last_login={row[6]};user_agent={row[7]}"
        logger.info(message)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()

