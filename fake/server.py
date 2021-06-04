from flask import Flask, jsonify, request
import numpy
import cv2
import base64
import logging
from fun_code import main as infer_medicine


log = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def predict_medicine():
    """
    Return prediction about medicine in image.

    Request Format:
    Multipart Form Request with image to run inference sent with key "image"

    Response Format:
    JSON Response
    {
        "authentic" : <bool>,
        "name" : <medicine name text>
        "description" : <text description about the medicine>
    }
    """

    # read image file string data
    filestr = request.files["medicine_image"].read()

    # convert image string data to numpy array
    npimg = numpy.fromstring(filestr, numpy.uint8)

    # convert numpy array to image
    img = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)

    # Run inference tasks here
    authentic, med_name, med_description = infer_medicine(img)

    return jsonify(
        {
            "authentic": authentic,
            "name": med_name,
            "description": med_description,
        }
    )
