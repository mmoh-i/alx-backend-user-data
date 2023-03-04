#!/bin/usr/env python3
import re
import logging
from typing import List

PII_FIELDS = ("name", "phone", "email", "ssn", "password")

def filter_datum(fields: List[str], redaction: str,
        message: str, separator: str) -> str:
    """
    Obfuscates the specified fields in a log message with
    a redaction string
    """
    for field in fields:
        message = re.sub(field+'=.*?'+separator,
                field+'='+redaction+separator, message)
    return message

    #Log formatter
class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        return filter_datum(
                self.fields, self.REDACTION, message, self.SEPARATOR)

    #2. Create logger
def get_logger() -> logging.Logger:
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)

    return logger

#Connect to secure database
def get_db() -> mysql.connector.connection.MySQLConnection:
    db_usr = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_psswd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
            user=db_usr,
            password=db_psswd,
            host=db_host,
            database=db_name
            )

#4. Read and filter data 
def main() -> None:
    """function will obtain a database connection
    nd retrieve all rows in the users table.
    """
    conn = get_db()
    logger = get_logger()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    for row in cursor.fetchall():
        str_row = ''.join(
                f"{filed}={val];" for field, val in zip(cursor.column_names, row)
                )
        logger.info(str_row)
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()

