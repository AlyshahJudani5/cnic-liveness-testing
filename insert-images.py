import os
import base64
from pymongo import MongoClient
from datetime import datetime

# 1. Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://alyshahjudani5:dw5vdF2OY2W0sD19@test-db.aklnuk2.mongodb.net/")

# 2. Use your target database and collection
db = client["sample_db"]
cnic_dumps_col = db["cnic_dumps"]

# 3. Folder where your sample images are stored
image_folder = "images"

# 4. Loop through all image files
for image_name in os.listdir(image_folder):
    if image_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
        # Construct the full path to the image
        image_path = os.path.join(image_folder, image_name)

        # 5. Read the image and encode it as base64
        with open(image_path, 'rb') as f:
            image_data = f.read()
            base64_image = base64.b64encode(image_data).decode('utf-8')

        # 6. Prepare a single document with logs and image
        document = {
            "upload_time": datetime.utcnow(),
            "logs": {
                "cnic_details": {
                    "side": "front",
                    "type": "smart"
                },
                "details": {
                    "is_blurry": True,
                    "is_too_bright": False,
                    "is_too_dark": False
                },
                "is_authentic": False,
                "is_retry": True,
                "reason": "Most tests indicate this is likely a copy or fake"
            },
            "base64_image": base64_image
        }

        # 7. Insert the single document into MongoDB
        cnic_dumps_col.insert_one(document)
        print(f"[✔] Inserted: {image_name}")
