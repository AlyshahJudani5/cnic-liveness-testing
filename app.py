from flask import Flask, send_file, jsonify, request, render_template
from pymongo import MongoClient
from io import BytesIO
import base64
from bson import ObjectId

app = Flask(__name__)

# MongoDB
client = MongoClient("mongodb+srv://alyshahjudani5:dw5vdF2OY2W0sD19@test-db.aklnuk2.mongodb.net/")
db = client["sample_db"]
cnic_col = db["cnic_dumps"]  # 👈 only one collection now

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/cnic-logs", methods=["GET"])
def get_complete_cnic_logs():
    try:
        # Fetch all documents, including the _id
        cursor = cnic_col.find({})
        full_logs = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
            full_logs.append(doc)
        return jsonify(full_logs)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch logs: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
