# server.py
import os
from flask import Flask, render_template, jsonify, request, send_file
from werkzeug.utils import secure_filename
import magnum_datagen
import server_utilities

app = Flask(__name__, static_folder="../static/dist", template_folder="../static")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/downloadDataFile")
def downloadDataFile():
    try:
        return send_file(magnum_datagen.genRunner(), as_attachment=True)
        # return send_file('./Data/exampleFile.csv', as_attachment=True)
    except Exception as e:
        return e

@app.route("/setUp")
def hello():
    features = [k for k, v in server_utilities.features.items()]
    setup = jsonify({
        "setup": {
            "features": features,
            "models": ['Churn-out']
        }
    })
    return setup    

UPLOAD_FOLDER = './Data/'
@app.route("/results", methods=['POST'])
def getResults():
    if 'file' not in request.files:
        return 'No File Uploaded'
    file = request.files['file']
    if file.filename == '':
        return 'No selected File'
    if file:
        filename = secure_filename(file.filename)
        # print(file)
        file.save(os.path.join(app.root_path, 'Data', filename))
        featuresSelected = request.form['features']
        featuresToBeExtracted = [(k,v()) for k,v in server_utilities.features.items() if k in featuresSelected]
        results = server_utilities.framework.frameworkRunner(featuresToBeExtracted, filename)
        return jsonify(results)
    
    

    
if __name__ == "__main__":
    app.run()
