"""
The flask application package.
"""

from flask import Flask
import os

app = Flask(__name__, instance_relative_config=True)

import FlaskWeb.views
