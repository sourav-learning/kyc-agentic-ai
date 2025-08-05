import streamlit as st
import datetime
from agents.orchestrator import orchestrator

st.title("Instant KYC Validator")

with st.form("kyc_form"):
    name = st.text_input("Full Name (As per UID)")
    parent = st.text_input("Parent's Name")
    address = st.text_area("Address")
    uid = st.text_input("UID Number")
    dob = st.date_input("Date of Birth", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
    email = st.text_input("Email")
    uploaded_file = st.file_uploader("Upload UID PDF")
    submitted = st.form_submit_button("Validate")
    print("parent : " + parent)
    if submitted:
        if not uploaded_file or not uploaded_file.name.endswith(".pdf"):
            st.error("Please upload a valid PDF file")
        else:
            user_input = {
                "name": name,
                "parent": parent,
                "address": address,
                "uid": uid,
                "dob": str(dob),
                "email": email
            }
            result = orchestrator(user_input, uploaded_file)
            st.success(result)
