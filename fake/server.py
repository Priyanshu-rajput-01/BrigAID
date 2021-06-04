from flask import Flask, jsonify, request
from flask.helpers import make_response
from flask.wrappers import Response
import numpy
import cv2
import base64
import logging


log = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def predict_medicine():

    # read image file string data
    filestr = request.files["image"].read()
    # log.debug("Image String : %s", filestr)
    # convert string data to numpy array
    npimg = numpy.fromstring(filestr, numpy.uint8)
    # convert numpy array to image
    img = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)

    # Run inference tasks here
    # results = infer(img)

    retval, img_buffer = cv2.imencode(".jpg", img)
    log.debug("Return Val : %s \n Output : %s", retval, img_buffer)

    response = make_response(bytes(img_buffer))
    response.headers["Content-Type"] = "image/jpeg"

    return response
    # return jsonify({"image": base64.b64encode(img_buffer).decode("utf-8")})
