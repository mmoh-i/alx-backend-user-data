#!/bin/usr/env python3
import re


def filter_datum(fields: str, redaction: str,
        message: str, separator: str) -> str:
    """
    Obfuscates the specified fields in a log message with
    a redaction string
    """
    for field in fields:
        messge = re.sub(field+'=.*?'+separator,
            field+'='+redaction+separator, message)
    return messge
