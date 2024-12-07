from flask import Flask

app = Flask(__name__)


@app.route("/")
def input_page():
    return "Hello! this is the input page <h1>Hello<h1>"


@app.route("/reslts")
def results():
    return "This is our results page"


if __name__ == '__main__':
    app.run()
