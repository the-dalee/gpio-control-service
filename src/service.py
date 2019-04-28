from web.controller import get_pin, put_pin
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/pins/<pin>", methods=['GET', 'PUT'])
def hello(pin: int):
    if request.method == 'GET':
        response = get_pin(pin)
        return jsonify(response)
    elif request.method == 'PUT':
        response = put_pin(pin, request.get_json(force=True))
        return jsonify(response)
