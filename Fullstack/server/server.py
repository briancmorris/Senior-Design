# server.py
from flask import Flask, render_template, jsonify

app = Flask(__name__, static_folder="../static/dist", template_folder="../static")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/hello")
def hello():
    setup = jsonify({
        "setup": {
            "features": ['lifespan', 'emails recv'],
            "models": ['churn-out']
        }
    })
    return setup    

if __name__ == "__main__":
    app.run()
