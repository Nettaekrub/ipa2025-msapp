from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient
from bson import ObjectId
import os

app = Flask(__name__)

mongo_uri  = os.environ.get("MONGO_URI")
db_name    = os.environ.get("DB_NAME")

client = MongoClient(mongo_uri)
db = client[db_name]                             
routers = db["routers"]

@app.route("/")
def main():
    data = list(routers.find({}, {"_id": 0}))   
    return render_template("index.html", data=data)

@app.route("/add", methods=["POST"])
def add_info():
    ip_address = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")

    if ip_address and username and password:
        routers.insert_one({"ip_address": ip_address, "username": username, "password": password})
    return redirect(url_for("main"))

@app.route("/delete", methods=["POST"])
def delete_info():
    idx = int(request.form.get("idx"))
    data = list(routers.find({}, {"_id": 0}))
    if 0 <= idx < len(data):
        router = data[idx]
        routers.delete_one(router)
    return redirect(url_for("main"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)