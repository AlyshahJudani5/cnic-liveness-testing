import os
from pymongo import MongoClient
from datetime import datetime

# 1. Connect to MongoDB running on localhost
client = MongoClient("mongodb+srv://alyshahjudani5:dw5vdF2OY2W0sD19@test-db.aklnuk2.mongodb.net/")

# 2. Choose (or create) a database and collection
db = client["sample_db"]
images_col = db["images"]
logs_col = db["logs"]

# 3. Folder where your sample images are stored
image_folder = "images"


# 4. Loop through all files in the folder
for image_name in os.listdir(image_folder):
    if image_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):

        image_path = os.path.join(image_folder, image_name)

        # 5. Open the image file in binary read mode
        with open(image_path, 'rb') as f:
            image_data = f.read()

        # 6. Prepare the document with metadata and binary data
        image_doc = {
            "filename": image_name,
            "data": image_data,
            "upload_time": datetime.utcnow()
        }

        # 7. Insert the image document into MongoDB
        images_col.insert_one(image_doc)

        # 8. Log the insert in a separate logs collection
        log_entry = {
                        "filename": image_name,
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
                    }
        logs_col.insert_one(log_entry)

        print(f"[✔] Inserted and logged: {image_name}")
