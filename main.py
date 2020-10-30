from flask import Flask
from compile.runner import run_code
app = Flask(__name__)


@app.route('/')
def hello_world():
    output = run_code("print('hello')", "python", 3)
    print(output)
    return 'Hello, World!'


app.run(port=8080)
