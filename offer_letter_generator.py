import streamlit as st
from docx import Document
from io import BytesIO
from datetime import date


# ----------------- SIMPLE AUTHENTICATION (with Login Button) -----------------
import streamlit as st

# --- Define valid HR users ---
VALID_USERS = {
    "pruthvi": "Paarth@2025",
    "shiva ": "BAnalyst@312231",
}

# Initialize session state for login tracking
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Sidebar login section
st.sidebar.title("🔐 HR Login")

if not st.session_state.authenticated:
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    login_btn = st.sidebar.button("Login")

    if login_btn:
        if username in VALID_USERS and VALID_USERS[username] == password:
            st.session_state.authenticated = True
            st.success(f"✅ Welcome, {username}!")
        else:
            st.error("❌ Invalid username or password. Please try again.")
    else:
        st.info("Please log in to access the Offer Letter Generator.")
        st.stop()
else:
    st.sidebar.success("✅ Logged in successfully.")
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.experimental_rerun()
# ----------------------------------------------------------


def generate_offer_letter(name, title, address, manager, joining_date, consultancy_line):
    # Load the original template
    doc = Document("Offer Letter.docx")

    for p in doc.paragraphs:
        if "Name" in p.text:
            p.text = p.text.replace("Name", name)
        if "Title" in p.text:
            p.text = p.text.replace("Title", title)
        if "Employee Address" in p.text:
            p.text = p.text.replace("Employee Address", address)
        if "Manager Name" in p.text:
            p.text = p.text.replace("Manager Name", manager)
        if "Date of Joining" in p.text:
            p.text = p.text.replace("Date of Joining", joining_date)
        # Replace the entire consultancy fee line
        if "(Amount)" in p.text and "INR" in p.text:
            p.text = consultancy_line

    # Save to memory buffer
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# ---------------- Streamlit UI ----------------
st.title("📄 Offer Letter Generator")
st.write("Fill in the details to generate a customized employee offer letter.")

with st.form("offer_form"):
    name = st.text_input("Employee Name")
    title = st.text_input("Designation / Title")
    address = st.text_area("Employee Address")
    manager = st.text_input("Manager Name")
    joining_date = st.date_input("Date of Joining", date.today()).strftime("%d-%m-%Y")
    consultancy_line = st.text_area(
        "Consultancy Fee Line (Full sentence)",
        value="You shall be paid a consultancy fee of (Amount) INR 1,25,000/- (Indian Rupees One Lakh Twenty-Five Thousand only) per month, subject to deduction of 10% TDS as per the provisions of the Income Tax Act, 1961. "
    )

    submitted = st.form_submit_button("Generate Offer Letter")

if submitted:
    if not all([name, title, address, manager, consultancy_line]):
        st.error("⚠️ Please fill all fields before generating.")
    else:
        doc_file = generate_offer_letter(name, title, address, manager, joining_date, consultancy_line)
        st.success("✅ Offer Letter Generated Successfully!")
        st.download_button(
            label="⬇️ Download Offer Letter (.docx)",
            data=doc_file,
            file_name=f"Offer_Letter_{name.replace(' ', '_')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
