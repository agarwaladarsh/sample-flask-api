from flask import jsonify, request
# import socket
from app import app
from . import endpoint as url
from . import json_actions
from . import services
from shared.sharedservices import token_req
import shared.sharedservices as sharedservices
import os
import json


# Return the user data logged in
@json_actions.route(url.read_json, methods=['GET'])
def read_json():
    return jsonify({'message': 'SUCCESS'}), 200


@json_actions.route(url.upload_json, methods=['POST'])
def upload_json():
    f = request.files['file']

    if not os.path.exists('temp'):
        os.mkdir('temp')

    f.save('temp/' + f.filename)

    f_read = open('temp/' + f.filename)
    data = json.loads(f_read.read())
    print(data.keys())
    f.close()

    return jsonify({'message': 'Uploaded Successfully'}), 200
