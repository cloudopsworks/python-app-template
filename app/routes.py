from flask import Blueprint, jsonify

main_blueprint = Blueprint('main', __name__)


# Sample Routes

@main_blueprint.route('/')
def index():
    return "Welcome to my Flask App!"


@main_blueprint.route('/api', methods=['GET'])
def api_home():
    return jsonify({"message": "This is the API endpoint", "status": "success"})


@main_blueprint.route('/hello/<name>', methods=['GET'])
def hello_name(name):
    return f"Hello, {name.capitalize()}!"


@main_blueprint.route('/square/<int:number>', methods=['GET'])
def square(number):
    result = number * number
    return jsonify({"number": number, "square": result})


@main_blueprint.route('/status', methods=['GET'])
def status():
    return jsonify({"app": "Flask Sample App", "status": "OK"})