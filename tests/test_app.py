import dash
import dash.testing
import pytest
import sys
sys.path.insert(1, '/Users/youssefabdelhamid/Documents/GitHub/BitsNBytes-IT-Project-1/prod')
import app  # import your app module

from dash.testing.application_runners import import_app
from dash.testing.browser import Browser

def test_app():
    # Import the app
    app = import_app("app")

    # Create a test browser
    with Browser() as browser:
        # Start the app in a test context
        browser.start_server(app)

        # Use the test browser to simulate user interactions and check the app's response
        # For example, you can check if the correct elements are present on the page:
        assert browser.find_element("#upload-data")
        assert browser.find_element("#remove-duplicates")
        assert browser.find_element("#fill-na")
        assert browser.find_element("#column-select")
        assert browser.find_element("#data-visualization")
        assert browser.find_element("#summary-stats")
        assert browser.find_element("#export-data")
        assert browser.find_element("#download-data")

        # You can also simulate user interactions and check the app's response
        # For example, you can simulate a file upload and check if the dropdown options are updated correctly:
        # browser.send_keys("#upload-data", "path/to/test/file.csv")
        # assert browser.find_element("#column-select").text == "Expected dropdown options"

# Run the test with pytest
if __name__ == "__main__":
    pytest.main([__file__])