import json

def fetch_cibil_score(uid):
    """
    Fetches the CIBIL score for a given UID from a simulated database (JSON file).
    """
    try:
        with open("cibil_db.json", "r") as f:
            cibil_db = json.load(f)
        score = cibil_db.get(uid)
        if score is not None:
            return {"uid": uid, "cibil_score": score}
        else:
            return {"uid": uid, "cibil_score": None, "error": "CIBIL score not found"}
    except Exception as e:
        return {"uid": uid, "cibil_score": None, "error": str(e)}
