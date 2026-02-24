"""
File parsing logic for uploaded CSV, Excel, and JSON files.

Pure business logic — no Dash dependencies.
"""

import base64
import io
import json
import os
from typing import Optional

import pandas as pd


def parse_upload(contents: str, filename: str) -> Optional[pd.DataFrame]:
    """
    Parse an uploaded file's base64 contents into a DataFrame.

    Args:
        contents: The raw base64 content string from dcc.Upload
                  (format: "data:content_type;base64,<data>").
        filename: Original filename, used to detect format.

    Returns:
        A DataFrame on success, or None if the format is unsupported.

    Raises:
        ValueError: If the file cannot be parsed.
    """
    _content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    extension = os.path.splitext(filename)[1].lower()

    if extension == ".csv":
        return pd.read_csv(io.StringIO(decoded.decode("utf-8")))
    elif extension in (".xlsx", ".xls"):
        return pd.read_excel(io.BytesIO(decoded))
    elif extension == ".json":
        json_data = json.loads(decoded.decode("utf-8"))
        return pd.json_normalize(json_data)
    else:
        return None
