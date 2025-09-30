from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        pictures = [value['pic_url'] for value in data]
        return jsonify(pictures), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for value in data:
        if(value["id"] == id):
            return jsonify(value)
    return {"message": "Picture not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.json
    if not new_picture:
        return {"message": "Invalid Input"}, 422
    
    id = new_picture["id"]
    for value in data:
        if(value["id"] == id):
            return {"Message": f"picture with id {new_picture['id']} already present"}, 302
    
    try:
        data.append(new_picture)
    except NameError:
        return {"message": "data not defined"}, 500
    return jsonify(data[-1]), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = request.json
    if not picture:
        return {"message": "Invalid Input"}, 422
    
    picture_updated = False
    for index in range(len(data)):
        if(data[index]["id"] == id):
            data[index] = picture
            picture_updated = True
            break
    
    if picture_updated:
        return jsonify(data[index]), 200
        

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for index in range(len(data)):
        if(data[index]["id"] == id):
            data.pop(index)
            return {}, 204
    return {"message": "picture not found"}, 404
