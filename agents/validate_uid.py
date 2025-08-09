import json

with open("dummy_uid_db.json", "r") as f:
    DUMMY_UID_DB = json.load(f)

def validate_uid(extracted_data, entered_data):
    """
    extracted_data: dict from PDF
    entered_data: dict from form (optional, but recommended)
    """
    uid = extracted_data.get("uid")
    print('uid to search :' + str(uid))
    print(DUMMY_UID_DB)
    uid_data = DUMMY_UID_DB.get(uid)
    print("Extracted Data (PDF):")
    print(extracted_data)
    print("Entered Data (Form):")
    print(entered_data)
    print("Searched result in DB:")
    print(uid_data)
    if not uid_data:
        return {"status": "failed", "reason": "UID not found in database"}

    # Check PDF-extracted data vs DB
    for key in [k for k in extracted_data.keys() if k != "uid"]:
        if extracted_data.get(key) != uid_data.get(key):
            return {"status": "failed", "reason": f"Mismatch in {key} between PDF and database"}

    # If entered_data is provided, check entered data vs DB
    if entered_data:
        for key in ["name", "parent", "address", "dob"]:
            if entered_data.get(key) != uid_data.get(key):
                return {"status": "failed", "reason": f"Mismatch in {key} between entered data and database"}

    return {"status": "success"}
