from flask import Flask, send_file, jsonify, request, render_template
from pymongo import MongoClient
from io import BytesIO

app = Flask(__name__)

# MongoDB
client = MongoClient("mongodb+srv://alyshahjudani5:dw5vdF2OY2W0sD19@test-db.aklnuk2.mongodb.net/")
db = client["sample_db"]
images_col = db["images"]
logs_col = db["logs"]  # 👈 we use this now

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/images", methods=["GET"])
def list_images():
    filenames = images_col.distinct("filename")
    print(f"[✔] Found {len(filenames)} images in the database.")
    return jsonify(filenames)

@app.route("/image/<filename>", methods=["GET"])
def get_image(filename):
    image_doc = images_col.find_one({"filename": filename})
    if not image_doc:
        return jsonify({"error": "Image not found"}), 404
    return send_file(BytesIO(image_doc["data"]), mimetype="image/jpeg", download_name=filename)

# ✅ NEW: Endpoint to get logs
@app.route("/api/logs", methods=["GET"])
def get_logs():
    logs = logs_col.find()
    result = []
    for log in logs:
        log.pop("_id")  # remove internal MongoDB ID
        result.append(log)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
