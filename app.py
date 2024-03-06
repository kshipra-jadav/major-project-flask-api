from flask import Flask, request, Response, send_file
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import os

UPLOAD_FOLDER = "uploads"
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.isdir(app.config["UPLOAD_FOLDER"]):
    os.mkdir(UPLOAD_FOLDER)

@app.route("/", methods=["GET"])
def hello():
    return {"hello": "world"}

@app.route("/ocr", methods=["POST"])
def ocr():
    if request.method == "POST":
        if 'image' not in request.files:
            print('hello')
            return Response("Image Not Attached!", status=400)
        
        img = request.files['image']
        img_path = os.path.join(app.config["UPLOAD_FOLDER"], img.filename)
        img.save(img_path)
        
        model = ocr_predictor(pretrained=True)
        doc = DocumentFile.from_images(img_path)

        result = model(doc)

        return result.render()



if __name__ == "__main__":
    app.run(debug=True)