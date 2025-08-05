import json

with open("dummy_uid_db.json", "r") as f:
    DUMMY_UID_DB = json.load(f)

def validate_uid(data):
    print('uid to search :' + data.get("uid"))
    print(DUMMY_UID_DB)
    uid_data = DUMMY_UID_DB.get(data.get("uid"))
    print("Entered Data")
    print(data)
    print("searched result : ")
    print(uid_data)
    if not uid_data:
        return {"status": "failed", "reason": "UID not found"}
    for key in ["name", "parent", "address", "dob"]:
        if data.get(key) != uid_data.get(key):
            return {"status": "failed", "reason": f"Mismatch in {key}"}
    return {"status": "success"}
