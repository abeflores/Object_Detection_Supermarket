import settings
from flask import Flask
import flask_login
import utils

from werkzeug.utils import secure_filename
import os
import cv2
from middleware import model_detect
from flask_httpauth import HTTPTokenAuth

from flask import (
    flash,
    redirect,
    render_template,
    request,
    url_for,
    jsonify,
)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = settings.UPLOAD_FOLDER
app.config["PROCESSED_FOLDER"] = settings.PROCESSED_FOLDER
app.secret_key = "secret key"

# Login Manager
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

auth = HTTPTokenAuth(scheme="Bearer")

# Define user model
class User(flask_login.UserMixin):
    def __init__(self, id, name):
        self.id = id
        self.name = name


@login_manager.user_loader
def user_loader(token):
    if token not in settings.TOKENS:
        return

    user = User(token, settings.TOKENS[token])
    return user


@login_manager.request_loader
def request_loader(request):
    token = request.form.get("token")
    if token not in settings.TOKENS:
        return

    user = User(token, settings.TOKENS[token])
    return user


@auth.verify_token
def verify_token(token):
    if token in settings.TOKENS:
        return settings.TOKENS[token]


# Views
@app.route("/", methods=["GET"])
def index():
    if flask_login.current_user.is_authenticated:
        return render_template("index.html", name=flask_login.current_user.name)
    else:
        return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    token = request.form["token"]
    if token in settings.TOKENS:
        user = User(token, settings.TOKENS[token])
        flask_login.login_user(user)
        return redirect(url_for("index"))
    else:
        flash("Invalid Token!")
        return redirect(url_for("index"))


@app.route("/", methods=["POST"])
@flask_login.login_required
def upload_image():
    """
    Function used in the frontend so it can upload and show an image.
    When it receives an image from the UI, it also calls the ML model to
    get and display the detections.
    """
    # No file received, show basic UI
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)

    # File received but no filename is provided, show basic UI
    file = request.files["file"]
    if file.filename == "":
        flash("No image selected for uploading")
        return redirect(request.url)

    # File received and it's an image, it must show it and get detections
    if file and utils.allowed_file(file.filename):

        hash_imgname = utils.get_file_hash(file)
        img_savepath = os.path.join(settings.UPLOAD_FOLDER, hash_imgname)

        if not os.path.exists(img_savepath):  # Check if the img already exist
            file.stream.seek(0)
            file.save(img_savepath)
            if not utils.verify_image(img_savepath):  # Check corruption
                os.remove(img_savepath)
                flash("Image is corrupted, try with another one")
                return redirect(request.url)

        detection_dict = model_detect(hash_imgname)

        alpha = 0.5
        utils.draw_mask(
            detection_dict["bouding_boxes"], hash_imgname, alpha
        )  # Save the masked image

        return render_template(
            "index.html", filename=hash_imgname, name=flask_login.current_user.name
        )

    # File received and but it isn't an image
    else:
        flash("Allowed image types are -> png, jpg, jpeg, gif")
        return redirect(request.url)


@app.route("/display/<filename>")
@flask_login.login_required
def display_image(filename):
    """
    Display uploaded image in the UI.
    """
    return redirect(url_for("static", filename="uploads/" + filename), code=301)


@app.route("/display/processed/<filename>")
@flask_login.login_required
def display_image_processed(filename):
    """
    Display uploaded image in the UI.
    """
    return redirect(url_for("static", filename="processed/" + filename), code=301)


@app.route("/logout", methods=["POST"])
def logout():
    flask_login.logout_user()
    return redirect(url_for("index"))


@app.route("/detect", methods=["POST"])
@auth.login_required
def detect():
    """
    Endpoint used to get detections without need to access the UI.
    """
    if "file" not in request.files:
        rpse = {"success": False, "detections": None}
        return jsonify(rpse), 400

    # File received but no filename is provided
    file = request.files["file"]
    if file.filename == "":
        rpse = {"success": False, "detections": None}
        return jsonify(rpse), 400

    # File received and it's an image, it must show it and get predictions
    if file and utils.allowed_file(file.filename):
        file.filename = utils.get_file_hash(file)
        image_full_path = os.path.join(
            settings.UPLOAD_FOLDER, secure_filename(file.filename)
        )
        if (
            os.path.exists(image_full_path) == False
        ):  # To avoid overwritte the image on disk
            file.save(image_full_path)
            if not utils.verify_image(image_full_path):  # Check corruption
                os.remove(image_full_path)
                rpse = {"success": False, "detections": None}
                return jsonify(rpse), 400

        detection_dict_tmp = model_detect(file.filename)

        detection_dict = {"User": auth.current_user(), "Data:": detection_dict_tmp}

        rpse = {"success": True, "detections": detection_dict}
        return jsonify(rpse), 200
    else:
        rpse = {"success": False, "detections": None}
        return jsonify(rpse), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=settings.API_DEBUG)
