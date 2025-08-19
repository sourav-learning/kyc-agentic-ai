
from agents.file_reader import extract_data_from_pdf
from agents.validate_uid import validate_uid
from agents.response_agent import send_confirmation_email
from agents.error_handler import error_handler
from agents.cibil_agent import fetch_cibil_score
from agents.account_creation_agent import create_account
import os, uuid
import glob

TEMP_MEMORY = {}
TEMP_DIR = "temp_uploads"

def cleanTempFolder():
    files = sorted(
    glob.glob(os.path.join(TEMP_DIR, "*.pdf")),
    key=os.path.getmtime,
    reverse=True
    )
    for old_file in files[5:]:
        try:
            os.remove(old_file)
        except Exception as e:
            print(f"Could not delete {old_file}: {e}")

def orchestrator(user_input, uploaded_file):
    file_id = str(uuid.uuid4())
    file_path = os.path.join(TEMP_DIR, f"{file_id}.pdf")
    os.makedirs(TEMP_DIR, exist_ok=True)  # Ensure the directory exists
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    TEMP_MEMORY[file_id] = {"status": "initiated"}
    cleanTempFolder()
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

    # Only check CIBIL score if validation is successful and application_type is 'Apply for Loan'

    cibil_result = None
    account_result = None
    if isinstance(validation_result, dict) and validation_result.get("status", "").lower() == "success":
        if user_input.get("application_type") == "Apply for Loan":
            cibil_result = fetch_cibil_score(user_input.get("uid"))
        elif user_input.get("application_type") == "New Account Opening":
            # Remove application_type before sending to account creation
            account_details = user_input.copy()
            account_details.pop("application_type", None)
            account_result = create_account(account_details)


    # Send confirmation email for KYC validation (existing logic)
    if email:
        send_confirmation_email(
            email,
            validation_result["status"],
            validation_result.get("reason", ""),
            user_input.get("name", ""),
            subject="KYC Validation Result"
        )
    else:
        print("Email address not provided")

    # Send additional email for account creation or loan application
    if email and isinstance(validation_result, dict) and validation_result.get("status", "").lower() == "success":
        from agents.response_agent import generate_email_body
        if user_input.get("application_type") == "New Account Opening" and account_result:
            account_number = account_result.get("account", {}).get("account_number")
            subject = "Account Creation Confirmation"
            body = generate_email_body(
                status="success",
                reason=f"Your new account has been created successfully. Your account number is {account_number}.",
                user_name=user_input.get("name", "")
            )
            # Send the email
            send_confirmation_email(email, "success", body, user_input.get("name", ""), subject)
        elif user_input.get("application_type") == "Apply for Loan" and cibil_result:
            cibil_score = cibil_result.get("cibil_score")
            approved = isinstance(cibil_score, (int, float)) and cibil_score > 700
            subject = "Loan Application Status"
            if approved:
                reason = f"Congratulations! Your loan is approved. Your CIBIL score is {cibil_score}."
            else:
                reason = f"Unfortunately, your loan is not approved. Your CIBIL score is {cibil_score}."
            body = generate_email_body(
                status="success" if approved else "failed",
                reason=reason,
                user_name=user_input.get("name", "")
            )
            send_confirmation_email(email, "success" if approved else "failed", body, user_input.get("name", ""), subject)

    # Return a formal text message summarizing the result
    status = validation_result.get("status", "").upper() if isinstance(validation_result, dict) else str(validation_result)
    reason = validation_result.get("reason", "") if isinstance(validation_result, dict) else ""
    msg = f"KYC Validation Status: {status}."
    if reason:
        msg += f" Reason: {reason}."

    if cibil_result:
        cibil_score = cibil_result.get("cibil_score")
        msg += f" CIBIL Score: {cibil_score}."
        if isinstance(cibil_score, (int, float)) and cibil_score > 700:
            msg += " You are eligible for a loan."
        elif cibil_score is None:
            msg += " CIBIL Score not found."

    if account_result:
        if account_result.get("status") == "success":
            account_number = account_result.get("account", {}).get("account_number")
            if account_number:
                msg += f" Account creation successful. Your account number is {account_number}."
            else:
                msg += " Account creation successful. We are unable to share account number now."
        else:
            msg += f" Account creation failed: {account_result.get('reason', 'Unknown error')}."

    return msg
