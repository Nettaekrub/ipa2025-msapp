from pymongo import MongoClient
import os

# ถ้าไม่มี env ก็ใช้ default localhost
mongo_uri = os.environ.get("MONGO_URI")
client = MongoClient(mongo_uri)

try:
    # ทดสอบเชื่อมต่อ (server_info จะ throw ถ้าต่อไม่ได้)
    info = client.server_info()
    print("✅ Connected to MongoDB")
    print("Version:", info.get("version"))
except Exception as e:
    print("❌ Cannot connect to MongoDB")
    print("Error:", e)
