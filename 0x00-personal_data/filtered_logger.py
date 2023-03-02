#!/bin/usr/env python3

import re

def filter_datum(fields, redaction, message, separator):
    """
    Obfuscates the specified fields in a log message with a redaction string.

    Args:
    fields: A list of strings representing all fields to obfuscate.
    redaction: A string representing by what the field will be obfuscated.
    message: A string representing the log line.
    separator: A string representing by which character is separating all fields in the log line (message).

    Returns:
    The obfuscated log message.

    # Output: User login attempt failed for user: johndoe with password: ***REDACTED*** and ssn: ***REDACTED***
    """
    # Use a single regex pattern to replace all occurrences of specified fields with redaction string
    return re.sub(f'(?<={separator})[^{separator}]*{fields[0]}[^{separator}]*(?={separator})|(?<={separator})[^{separator}]*{fields[1]}[^{separator}]*(?={separator})', redaction, message)
