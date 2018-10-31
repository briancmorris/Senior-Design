# server.py
import os
from flask import Flask, render_template, jsonify, request, send_file
from werkzeug.utils import secure_filename
app = Flask(__name__, static_folder="../static/dist", template_folder="../static")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/downloadDataFile")
def downloadDataFile():
    try:
        return send_file('./Data/exampleFile.csv', as_attachment=True)
    except Exception as e:
        return e

@app.route("/setUp")
def hello():
    setup = jsonify({
        "setup": {
            "features": ['lifespan', 'emails recv'],
            "models": ['churn-out', 'lifetime value']
        }
    })
    return setup    

UPLOAD_FOLDER = './Data/'
@app.route("/results", methods=['POST'])
def getResults():
    print("GOT HERE")
    if 'file' not in request.files:
        return 'No File Uploaded'
    print("GOT HERE")
    file = request.files['file']
    if file.filename == '':
        return 'No selected File'
    if file:
        filename = secure_filename(file.filename)
        print(file)
        file.save(os.path.join(app.root_path, 'Data', filename))
        return 'Got the file'
    
    

    
if __name__ == "__main__":
    app.run()
