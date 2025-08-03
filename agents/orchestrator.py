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

    validation_result = validate_uid(extracted_data)
    TEMP_MEMORY[file_id]["validation"] = validation_result

    send_confirmation_email(
        user_input["email"],
        validation_result["status"],
        validation_result.get("reason", ""),
        user_input.get("name", "")
    )
    return f"Validation status: {validation_result['status'].upper()}"
