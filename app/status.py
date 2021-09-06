"""
This module provides a blueprint for status-related resources.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import time

from . import START_TIME
from .docs import auto
from flask import Blueprint, jsonify, redirect


# --------------------------------------------------------------------------------
# Blueprint
# --------------------------------------------------------------------------------

status = Blueprint('status', __name__)


# --------------------------------------------------------------------------------
# Resources
# --------------------------------------------------------------------------------

@status.route('/')
def index():
  return redirect('/docs/')


@status.route('/status/', methods=['GET'])
@auto.doc()
def status_get():
  response = {
    'online': True,
    'uptime': round(time.time() - START_TIME, 3)
  }
  return jsonify(response)