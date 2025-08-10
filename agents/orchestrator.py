from agents.file_reader import extract_data_from_pdf
from agents.validate_uid import validate_uid
from agents.response_agent import send_confirmation_email
from agents.error_handler import error_handler
import os, uuid

TEMP_MEMORY = {}
TEMP_DIR = "temp_uploads"

def orchestrator(user_input, uploaded_file):
    file_id = str(uuid.uuid4())
    file_path = os.path.join(TEMP_DIR, f"{file_id}.pdf")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    TEMP_MEMORY[file_id] = {"status": "initiated"}

    extracted_data = extract_data_from_pdf(file_path)
    if not extracted_data:
        error_handler(file_id, "PDF could not be read or parsed by LLM")
        return "PDF is not readable"
    print("user input")
    print(user_input)
    print("Extracted Data")
    print(extracted_data)
    email = user_input.pop("email", None)

    validation_result = validate_uid(extracted_data, user_input)
    TEMP_MEMORY[file_id]["validation"] = validation_result
    if email: 
        send_confirmation_email(
            email,
            validation_result["status"],
            validation_result.get("reason", ""),
            user_input.get("name", "")
        )
    else:
       print("Email address not provided") 
    return f"Validation status: {validation_result['status'].upper()}"
