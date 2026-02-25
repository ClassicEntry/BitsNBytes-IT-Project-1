"""
Import all callback modules to trigger @dash.callback() registration.

This module must be imported after the Dash app instance is created.
"""

from pyexploratory.callbacks import charts  # noqa: F401
from pyexploratory.callbacks import export  # noqa: F401
from pyexploratory.callbacks import import_script  # noqa: F401
from pyexploratory.callbacks import ml  # noqa: F401
from pyexploratory.callbacks import step_panel  # noqa: F401
from pyexploratory.callbacks import table  # noqa: F401
from pyexploratory.callbacks import upload  # noqa: F401
