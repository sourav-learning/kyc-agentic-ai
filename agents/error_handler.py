TEMP_MEMORY = {}

def error_handler(file_id, reason):
    TEMP_MEMORY[file_id] = {"status": "error", "reason": reason}
    print(f"[ERROR] {file_id}: {reason}")
