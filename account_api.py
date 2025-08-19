
import json
import random
import string
from flask import Flask, request, jsonify

app = Flask(__name__)

DB_FILE = "accounts_db.json"

def generate_account_number():
    # Generates a unique 12-digit account number
    return ''.join(random.choices(string.digits, k=12))

@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.get_json()
    try:
        with open(DB_FILE, "r") as f:
            db = json.load(f)
        accounts = db.get("accounts", [])

        # Generate unique account number
        account_number = generate_account_number()
        # Ensure uniqueness
        existing_numbers = {acc.get("account_number") for acc in accounts}
        while account_number in existing_numbers:
            account_number = generate_account_number()
        print(account_number)
        data["account_number"] = account_number
        print(data)
        accounts.append(data)
        db["accounts"] = accounts
        with open(DB_FILE, "w") as f:
            json.dump(db, f, indent=2)
        return jsonify({"status": "success", "account": data}), 201
    except Exception as e:
        return jsonify({"status": "failed", "reason": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
