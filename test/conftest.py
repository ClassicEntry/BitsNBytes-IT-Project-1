"""
This file contains fixtures and utilities for testing Dash applications.
"""

import pytest
from dash.testing.application_runners import import_app
from dash.testing.browser import Browser


@pytest.fixture(scope="session")
def dash_duo(request):
    """
    Fixture for creating a DashComposite instance using Firefox browser.

    This fixture is used to create a DashComposite instance, which is a combination of a Dash app and a browser.
    It uses the Firefox browser for testing purposes.

    Args:
        request (pytest.request): The pytest request object.

    Yields:
        DashComposite: A DashComposite instance.

    """
    from dash.testing.composite import DashComposite

    with DashComposite(Browser.FIREFOX) as dc:
        yield dc
