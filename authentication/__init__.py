from flask import Blueprint
# New module initializes
routes = Blueprint('routes',__name__)

# Reference file path in module
from .index import *
from .services import *
from .queries import *
from .endpoint import *