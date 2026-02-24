"""
Tests for pyexploratory.core.file_parser.
"""

import base64
import json

import pandas as pd
import pytest

from pyexploratory.core.file_parser import parse_upload


def _encode(content: bytes, content_type: str = "text/csv") -> str:
    """Build a base64-encoded upload string mimicking dcc.Upload."""
    encoded = base64.b64encode(content).decode("utf-8")
    return f"data:{content_type};base64,{encoded}"


class TestParseCSV:
    def test_basic_csv(self):
        csv_bytes = b"a,b,c\n1,2,3\n4,5,6"
        result = parse_upload(_encode(csv_bytes), "test.csv")
        assert isinstance(result, pd.DataFrame)
        assert list(result.columns) == ["a", "b", "c"]
        assert len(result) == 2

    def test_csv_with_missing_values(self):
        csv_bytes = b"x,y\n1,\n,3"
        result = parse_upload(_encode(csv_bytes), "data.csv")
        assert len(result) == 2
        assert pd.isna(result["y"].iloc[0])


class TestParseJSON:
    def test_flat_json(self):
        data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
        json_bytes = json.dumps(data).encode("utf-8")
        result = parse_upload(_encode(json_bytes, "application/json"), "data.json")
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert "name" in result.columns

    def test_nested_json_normalized(self):
        data = [{"user": {"name": "Alice"}, "score": 90}]
        json_bytes = json.dumps(data).encode("utf-8")
        result = parse_upload(_encode(json_bytes, "application/json"), "nested.json")
        assert "user.name" in result.columns


class TestUnsupportedFormat:
    def test_txt_returns_none(self):
        result = parse_upload(_encode(b"some text"), "readme.txt")
        assert result is None

    def test_pdf_returns_none(self):
        result = parse_upload(_encode(b"%PDF-fake"), "doc.pdf")
        assert result is None
