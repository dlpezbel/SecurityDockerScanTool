from flask import Flask, jsonify

from project.service.check_container_service import Check

app = Flask(__name__)


@app.route('/')
def hello_world():
    return send_response()


@app.route('/containers/<id>/check')
def check(id):
    check = Check()
    return jsonify({"result": check.check_and_fix(id)}), 200


@app.route("/health")
def health():
    return jsonify({"status": "UP"}), 200


def send_response():
    return jsonify({"message": "Hello World"}), 200


if __name__ == '__main__':
    app.debug = True
    app.run()
