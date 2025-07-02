from flask import Flask, send_file, jsonify, request, render_template
from pymongo import MongoClient
from io import BytesIO
import base64

app = Flask(__name__)

# MongoDB
client = MongoClient("mongodb+srv://alyshahjudani5:dw5vdF2OY2W0sD19@test-db.aklnuk2.mongodb.net/")
db = client["sample_db"]
cnic_col = db["cnic_dumps"]  # 👈 only one collection now

@app.route("/")
def index():
    return render_template("index.html")

# ✅ Get list of image filenames
@app.route("/api/cnic-logs", methods=["GET"])
def get_complete_cnic_logs():
    try:
        # Fetch all documents, excluding the internal MongoDB ID
        cursor = cnic_col.find({}, {"_id": 0})
        full_logs = list(cursor)
        return jsonify(full_logs)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch logs: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
