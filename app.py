import streamlit as st
from datetime import datetime, date

# --- Page Configuration ---
st.set_page_config(
    page_title="Cumberland County FOAA Generator",
    page_icon="⚖️",
    layout="wide"
)

# --- Agency Directory Data ---
AGENCY_DATA = {
    "Cumberland County Sheriff's Office (Patrol/Jail)": {
        "name": "Cumberland County Sheriff's Office",
        "attn": "FOAA Public Access Officer / Records Division",
        "address": "36 County Way\nPortland, ME 04102",
        "note": "Includes Patrol Division and Cumberland County Jail Operations"
    },
    "Portland Police Department": {
        "name": "Portland Police Department",
        "attn": "FOAA Public Access Officer / Records Division",
        "address": "109 Middle Street\nPortland, ME 04101",
        "note": "Municipal Law Enforcement Records"
    },
    "Regional Dispatch Center (CCSO Dispatch)": {
        "name": "Cumberland County Regional Communications Center",
        "attn": "Communications Director / FOAA Custodian",
        "address": "22 High Street, Suite 1\nWindham, ME 04062",
        "note": "Handles PSAP, 911 Audio, and Regional CAD Dispatch Logs"
    }
}

CITIES_TOWNS = [
    "Portland", "South Portland", "Westbrook", "Gray", "Windham", 
    "Gorham", "Scarborough", "Brunswick", "Falmouth", "Cape Elizabeth", 
    "Yarmouth", "Freeport", "Standish", "Cumberland", "Bridgton", 
    "Harpswell", "New Gloucester", "Harrison", "Casco", "Naples", 
    "Raymond", "Sebago", "Baldwin", "Pownal", "North Yarmouth", "Other / Unincorporated"
]

# --- Header ---
st.title("⚖️ Cumberland County Legal Records & FOAA Generator")
st.markdown(
    "Generate statutorily compliant public records demand letters pursuant to the "
    "**Maine Freedom of Access Act (1 M.R.S. §§ 401–521)**."
)
st.divider()

# --- Main Layout ---
col_form, col_preview = st.columns([1.1, 1], gap="large")

with col_form:
    st.subheader("1. Target Agency & Requester Information")
    
    selected_agency_key = st.selectbox(
        "Target Agency",
        options=list(AGENCY_DATA.keys()),
        help="Select the agency that holds custody of the requested records."
    )
    agency_info = AGENCY_DATA[selected_agency_key]
    st.caption(f"📍 **Routing to:** {agency_info['name']} ({agency_info['note']})")

    with st.expander("Requester Contact Details", expanded=True):
        req_col1, req_col2 = st.columns(2)
        with req_col1:
            req_name = st.text_input("Full Name / Counsel Name", placeholder="e.g., Jane Doe, Esq.")
            req_org = st.text_input("Firm / Organization (Optional)", placeholder="e.g., Doe Legal Services")
            req_email = st.text_input("Email Address", placeholder="jane@example.com")
        with req_col2:
            req_phone = st.text_input("Phone Number", placeholder="(207) 555-0199")
            req_address = st.text_area("Mailing Address", placeholder="123 Congress St, Suite 400\nPortland, ME 04101", height=108)

    st.subheader("2. Incident & Case Details")
    
    date_col1, date_col2 = st.columns(2)
    with date_col1:
        start_date = st.date_input("Incident Start Date", value=date.today())
    with date_col2:
        end_date = st.date_input("Incident End Date", value=date.today())

    loc_col1, loc_col2 = st.columns([1, 1.5])
    with loc_col1:
        incident_town = st.selectbox("Municipality / Town", options=CITIES_TOWNS, index=0)
    with loc_col2:
        incident_address = st.text_input("Specific Incident Address / Intersection", placeholder="e.g., 400 Block of Forest Ave / Exit 48")

    case_col1, case_col2 = st.columns(2)
    with case_col1:
        cad_number = st.text_input("CAD / Incident Log Number (if known)", placeholder="e.g., 26-014829")
    with case_col2:
        involved_parties = st.text_input("Involved Parties' Names (& DOB if known)", placeholder="e.g., John Smith (DOB: 04/12/1985)")

    additional_context = st.text_area(
        "Additional Identifying Context (Optional)",
        placeholder="Provide any specific unit numbers, badge numbers, or time windows (e.g., 21:00 to 23:30 EST) to narrow the search.",
        height=75
    )

    st.subheader("3. Requested Document Checklist")
    st.caption("Select all records required for this demand:")

    doc_cad = st.checkbox("CAD (Computer-Aided Dispatch) Call Logs & Unit Timestamps", value=True)
    doc_911 = st.checkbox("911 Audio Transcripts & Radio Transmission Logs", value=True)
    doc_summary = st.checkbox("Initial Incident/Arrest Summary Sheets", value=True)
    doc_jail = st.checkbox("Jail Booking/Intake Slips (if handled at Cumberland County Jail)", value=False)
    doc_notes = st.checkbox("Officer Field Interview Notes & Metadata", value=False)
    
    custom_docs = st.text_input("Additional Specific Records (Optional)", placeholder="e.g., Body-Worn Camera (BWC) footage index, Cruiser dashcam video")

    st.subheader("4. Fee Waiver & Delivery Preferences")
    include_fee_waiver = st.checkbox("Include Public Interest & Legal Case Review Fee Waiver Request (1 M.R.S. § 408-A(11))", value=True)
    fee_cap = st.number_input("Maximum Pre-Authorized Cost Threshold ($)", min_value=0, value=25, step=5, help="If the fee waiver is denied, ask the agency to notify you before exceeding this amount.")
    export_format = st.radio("Preferred Export File Format", options=["Markdown (.md)", "Plain Text (.txt)"], horizontal=True)

# --- Letter Generation Logic ---
current_date_str = datetime.now().strftime("%B %d, %Y")

if start_date == end_date:
    date_range_str = start_date.strftime("%B %d, %Y")
else:
    date_range_str = f"{start_date.strftime('%B %d, %Y')} through {end_date.strftime('%B %d, %Y')}"

location_str = f"{incident_address}, {incident_town}, Maine" if incident_address.strip() else f"{incident_town}, Maine"
cad_str = cad_number.strip() if cad_number.strip() else "Not Known / Unassigned (Please search by date, location, and party names)"
parties_str = involved_parties.strip() if involved_parties.strip() else "Not Specified / All involved subjects at listed location"

# Build Document Bullet List
selected_documents = []
if doc_cad:
    selected_documents.append(
        "**CAD (Computer-Aided Dispatch) Call Logs & Unit Timestamps:** Complete dispatch printouts, call-for-service sheets, unit status histories (dispatch, en route, on-scene, clear timestamps), and all dispatcher or officer narrative remarks entered into the CAD system."
    )
if doc_911:
    selected_documents.append(
        "**911 Audio Transcripts & Radio Transmission Logs:** Full audio recordings and written transcripts (if available) of all incoming 911/non-emergency calls for service, as well as all primary and tactical radio channel transmissions associated with the incident."
    )
if doc_summary:
    selected_documents.append(
        "**Initial Incident/Arrest Summary Sheets:** All non-confidential initial incident reports, arrest reports, probable cause affidavits, uniform summons and complaints, and dispatch event summaries pursuant to 16 M.R.S. § 804."
    )
if doc_jail:
    selected_documents.append(
        "**Jail Booking/Intake Slips (Cumberland County Jail):** All intake records, booking sheets, arrestee intake logs, time-of-admission records, bail/release logs, and holding facility transfer documentation."
    )
if doc_notes:
    selected_documents.append(
        "**Officer Field Interview Notes & Metadata:** All contemporaneous field notes, witness interview logs, canvas notes, and associated electronic record metadata (including creation dates, modification timestamps, and author logs)."
    )
if custom_docs.strip():
    selected_documents.append(f"**Additional Specified Records:** {custom_docs.strip()}")

if not selected_documents:
    docs_formatted_md = "* *[No specific document categories selected. Please select at least one category in the checklist.]*"
else:
    docs_formatted_md = "\n".join([f"* {doc}" for doc in selected_documents])

# Build Requester Header Block
requester_lines = []
if req_name.strip():
    requester_lines.append(req_name.strip())
if req_org.strip():
    requester_lines.append(req_org.strip())
if req_address.strip():
    requester_lines.append(req_address.strip())
if req_email.strip():
    requester_lines.append(f"Email: {req_email.strip()}")
if req_phone.strip():
    requester_lines.append(f"Phone: {req_phone.strip()}")

requester_header = "\n".join(requester_lines) if requester_lines else "[Requester Name / Contact Information]"
signature_name = req_name.strip() if req_name.strip() else "[Requester Signature / Printed Name]"

# Build Context Line
context_block = f"\n* **Additional Identifying Details:** {additional_context.strip()}" if additional_context.strip() else ""

# Build Fee Waiver Block
if include_fee_waiver:
    fee_section = f"""### Fee Waiver Request & Cost Limitation
Pursuant to **1 M.R.S. § 408-A(11)**, I formally request a waiver of all fees associated with searching for, retrieving, compiling, and reproducing these records. Disclosure of the requested information is in the public interest, is critical to legal case review, and will likely contribute significantly to public understanding of government operations and law enforcement activities in Cumberland County. Furthermore, this request is not made primarily for any commercial purpose.

If this fee waiver request is denied in whole or in part, please provide an itemized advance cost estimate pursuant to **1 M.R.S. § 408-A(9)** before incurring any charges in excess of **${fee_cap:.2f}**."""
else:
    fee_section = f"""### Cost Estimate & Fee Limitation
Pursuant to **1 M.R.S. § 408-A(9)**, please notify me in advance with an itemized cost estimate if the total fees for searching, retrieving, compiling, and copying these records are expected to exceed **${fee_cap:.2f}**."""

# --- Construct Full Markdown Letter ---
letter_md = f"""{requester_header}

**Date:** {current_date_str}

**VIA ELECTRONIC MAIL / CERTIFIED MAIL**

**To:**
{agency_info['attn']}
{agency_info['name']}
{agency_info['address']}

**RE: Formal Public Records Request — Maine Freedom of Access Act (1 M.R.S. §§ 401–521)**

Dear Public Access Officer / Custodian of Records:

Pursuant to the Maine Freedom of Access Act (FOAA), 1 M.R.S. §§ 401–521, I am writing to request access to and copies of public records in the custody or control of the **{agency_info['name']}** concerning the following incident:

### Incident & Case Identifiers
* **Incident Date(s):** {date_range_str}
* **Incident Location / Municipality:** {location_str}
* **CAD / Incident Log Number:** {cad_str}
* **Involved Parties:** {parties_str}{context_block}

### Requested Records
Please provide digital copies of the following records (including any electronic records stored in databases, RMS/CAD servers, or audio logging systems, as defined under 1 M.R.S. § 402(3)):

{docs_formatted_md}

### Statutory Timeline & Severability
Pursuant to **1 M.R.S. § 408-A(1)**, you are statutorily required to acknowledge receipt of this request within **five (5) working days** of receiving it, and to provide a good-faith estimate of the time within which the agency will comply with the request.

If any portion of the requested records is claimed to be exempt from disclosure under the Intelligence and Investigative Record Information Act (16 M.R.S. §§ 801–809) or any other statutory exception, please redact only the strictly exempt portions and release the remainder of the reasonably segregable record. For any withheld record or redaction, please provide a written denial within five (5) working days stating the specific statutory citation authorizing the withholding, as mandated by **1 M.R.S. § 408-A(4)**.

{fee_section}

### Format & Delivery
To minimize reproduction costs and administrative burden, please produce all responsive records electronically via email (or secure electronic file transfer) to **{req_email.strip() if req_email.strip() else '[Insert Email Address]'}**.

Thank you for your prompt attention to this statutory request.

Sincerely,

{signature_name}
"""

# Create Plain Text version by stripping Markdown emphasis
letter_txt = (
    letter_md
    .replace("### ", "")
    .replace("**", "")
    .replace("*[", "[")
    .replace("]*", "]")
)

# --- Preview & Export Column ---
with col_preview:
    st.subheader("📄 Live Demand Letter Preview")
    
    if not selected_documents:
        st.warning("⚠️ Please select at least one document category from the checklist on the left.")

    # Prepare Download File Details
    safe_town = incident_town.lower().replace(" ", "_")
    file_date = start_date.strftime("%Y%m%d")
    
    if export_format == "Markdown (.md)":
        download_data = letter_md
        file_name = f"FOAA_Demand_{safe_town}_{file_date}.md"
        mime_type = "text/markdown"
    else:
        download_data = letter_txt
        file_name = f"FOAA_Demand_{safe_town}_{file_date}.txt"
        mime_type = "text/plain"

    st.download_button(
        label=f"⬇️ Download Finalized Letter ({export_format})",
        data=download_data,
        file_name=file_name,
        mime=mime_type,
        type="primary",
        use_container_width=True
    )

    with st.container(border=True):
        if export_format == "Markdown (.md)":
            st.markdown(letter_md)
        else:
            st.text(letter_txt)
