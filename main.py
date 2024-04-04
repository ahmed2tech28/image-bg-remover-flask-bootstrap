import os
from flask import Flask, render_template, request, redirect
from rembg import remove
from PIL import Image
import datetime

app = Flask(__name__)

UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DOWNLOAD_FOLDER = "./static/downloads/"
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

def remove_bg(path):
    img = Image.open(path)
    R = remove(img)
    os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)  # Create the directory if it doesn't exist
    new_file_name = os.path.join(app.config['DOWNLOAD_FOLDER'], datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f") + ".png")
    R.save(new_file_name)
    return new_file_name

@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        f = request.files["formFile"]
        filenametosave = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f") + "." + f.filename.split(".")[-1]
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filenametosave))
        filename = remove_bg(os.path.join(app.config['UPLOAD_FOLDER'], filenametosave))
        return render_template("index.html", title="RMBG - Official Site", filename=filename)
    return render_template("index.html", title="RMBG - Official Site")

if __name__ == "__main__":
    app.run(debug=True, port=3000)
