from flask import Blueprint
# New module initializes
json_actions = Blueprint('json_actions',__name__)

# Reference file path in module
from .index import *
from .services import *
from .queries import *
from .endpoint import *