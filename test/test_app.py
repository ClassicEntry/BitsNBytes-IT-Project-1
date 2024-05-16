"""
This file contains test cases for the Dash application.

The test cases include:
- Testing the navigation functionality
- Testing the data import functionality
- Testing the data analysis functionality
- Testing the sidebar links
- Testing the content of the page after starting the server and performing certain actions

These test cases ensure that the Dash application is functioning correctly and that the different
features and elements of the application are displayed as expected.
"""

import pytest
from dash.testing.application_runners import import_app
from dash.testing.browser import Browser

app = next(dash_app())

def dash_app():
    """
    Returns the Dash application object.

    Returns:
        Dash: The Dash application object.
    """
    app = import_app("prod/app.py")
    yield app


# def test_navigation(dash_duo):
#     """
#     Test the navigation functionality.

#     Args:
#         dash_duo (Dash): The Dash testing object.

#     Returns:
#         None
#     """
#     dash_duo.start_server(app)

#     dash_duo.find_element("#nav-link-import-data").click()
#     assert dash_duo.find_element("#page-import-data").is_displayed()
def test_navigation(dash_duo):
    """
    Test the navigation functionality.

    Args:
        dash_duo (Dash): The Dash testing object.

    Returns:
        None
    """
    dash_duo.start_server(app)

    dash_duo.find_element("#nav-link-import-data").click()
    assert dash_duo.find_element("#page-import-data").is_displayed()

def test_data_import(dash_duo):
    """
    Test the data import functionality.

    Args:
        dash_duo (Dash): The Dash testing object.

    Returns:
        None
    """
    dash_duo.start_server(app)
    dash_duo.find_element("#nav-link-import-data").click()

    dash_duo.upload_file("tests/test_data.csv", "#upload-data")

    assert dash_duo.find_element("#data-preview").is_displayed()

    dash_duo.find_element("#analysis-summary").click()


def test_data_analysis(dash_duo):
    """
    Test the data analysis functionality.

    Args:
        dash_duo (Dash): The Dash testing object.

    Returns:
        None
    """
    dash_duo.start_server(app)
    dash_duo.find_element("#nav-link-data-analysis").click()

    assert dash_duo.find_element("#summary-stats").is_displayed()


def test_sidebar_links(dash_duo):
    """
    Test the sidebar links.

    Args:
        dash_duo (Dash): The Dash testing object.

    Returns:
        None
    """
    dash_duo.start_server(app)

    assert dash_duo.find_element("#nav-link-import-data").is_displayed()
    assert dash_duo.find_element("#nav-link-data-analysis").is_displayed()


def test_page_content(dash_duo):
    """
    Test the content of the page after starting the server and performing certain actions.

    This function tests the content of the page after starting the server and performing certain actions.
    It checks if the page elements are displayed correctly.

    Args:
        dash_duo (Dash): The Dash testing object.

    Returns:
        None
    """
    # Start the server
    dash_duo.start_server(app)

    # Check if the import data page element is displayed
    assert dash_duo.find_element("#page-import-data").is_displayed()

    # Click on the data analysis navigation link
    dash_duo.find_element("#nav-link-data-analysis").click()

    # Check if the data analysis page element is displayed
    assert dash_duo.find_element("#page-data-analysis").is_displayed()
