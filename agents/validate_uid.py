import json

with open("dummy_uid_db.json", "r") as f:
    DUMMY_UID_DB = json.load(f)

def validate_uid(data):
    uid_data = DUMMY_UID_DB.get(data.get("uid"))
    if not uid_data:
        return {"status": "failed", "reason": "UID not found"}
    for key in ["name", "parent", "address", "dob"]:
        if data.get(key) != uid_data.get(key):
            return {"status": "failed", "reason": f"Mismatch in {key}"}
    return {"status": "success"}
