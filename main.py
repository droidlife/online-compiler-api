from flask import Flask
from flask import request, jsonify
from compile.runner import run_code
app = Flask(__name__)


@app.route('/', methods=['POST'])
def hello_world():
    json = request.get_json()
    output = run_code(json["code"], "python", 3)
    return jsonify(output._getvalue())


app.run(port=8080)
