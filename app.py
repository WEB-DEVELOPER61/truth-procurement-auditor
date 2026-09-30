import streamlit as st
import pandas as pd
from datetime import datetime
import re

st.set_page_config(
    page_title="Project TRUTH | Procurement Compliance Auditor",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ Project TRUTH: Automated Public Procurement Compliance Auditor")
st.caption("Empirical Evaluation Engine Benchmarked Against Rajasthan Transparency in Public Procurement (RTPP) Rules, 2013 (Rule 43)")

def parse_date(date_str):
    cleaned = date_str.strip().replace("PM", " PM").replace("AM", " AM")
    cleaned = re.sub(r'\s+', ' ', cleaned)
    for fmt in ["%d-%b-%Y %I:%M %p", "%d-%b-%Y", "%d/%m/%Y"]:
        try:
            return datetime.strptime(cleaned, fmt)
        except ValueError:
            continue
    return None

def audit_record(tid, pub_str, close_str, cost, dept):
    p_dt = parse_date(pub_str)
    c_dt = parse_date(close_str)
    if not p_dt or not c_dt:
        return None
    
    window = round((c_dt - p_dt).total_seconds() / 86400.0, 2)
    min_mandate = 7.0 if cost <= 1000000 else (10.0 if cost <= 20000000 else 20.0)
    deficit = max(0.0, round(min_mandate - window, 2))
    
    if window >= min_mandate:
        status = "COMPLIANT"
    elif window < 5.0:
        status = "CRITICAL VIOLATION"
    else:
        status = "MODERATE DEFICIT"
        
    return {
        "Tender ID": tid,
        "Department": dept,
        "Estimated Cost": f"₹{cost:,.0f}",
        "Published Date": pub_str,
        "Closing Date": close_str,
        "Window (Days)": window,
        "Statutory Mandate": f"{min_mandate:.0f} Days",
        "Deficit (Days)": deficit,
        "Compliance Status": status
    }

# 40-Tender Empirical Dataset Extracted from eProc Rajasthan Server Logs
RAW_DATA = [
    # Page 1 (S.No 1 - 20)
    ("2026_CEPWD_602278_1", "30-Sep-2026 06:10 PM", "13-Oct-2026 06:00 PM", 1200000, "PWD Nagaur"),
    ("2026_CEPWD_602263_1", "30-Sep-2026 06:05 PM", "24-Oct-2026 06:00 PM", 4500000, "PWD Bhilwara"),
    ("2026_CEPWD_602279_1", "30-Sep-2026 06:05 PM", "12-Oct-2026 06:00 PM", 800000, "PWD Nagaur"),
    ("2026_CEPWD_602250_1", "30-Sep-2026 06:05 PM", "24-Oct-2026 06:00 PM", 3800000, "PWD Bhilwara"),
    ("2026_CEPWD_602278_2", "30-Sep-2026 06:00 PM", "14-Oct-2026 06:00 PM", 600000, "PWD Nagaur"),
    ("2026_CEPWD_602278_3", "30-Sep-2026 06:00 PM", "13-Oct-2026 06:00 PM", 750000, "PWD Nagaur"),
    ("2026_CEPWD_602278_4", "30-Sep-2026 06:00 PM", "13-Oct-2026 06:00 PM", 500000, "PWD Nagaur"),
    ("2026_CEPWD_602264_1", "30-Sep-2026 06:00 PM", "12-Oct-2026 06:00 PM", 2200000, "PWD Dungarpur"),
    ("2026_CEPWD_602287_1", "30-Sep-2026 06:00 PM", "27-Oct-2026 06:00 PM", 6500000, "PWD Jaipur"),
    ("2026_CEPWD_602278_5", "30-Sep-2026 06:00 PM", "13-Oct-2026 06:00 PM", 900000, "PWD Nagaur"),
    ("2026_CEPWD_602250_2", "30-Sep-2026 05:40 PM", "28-Oct-2026 06:00 PM", 5200000, "PWD Rajsamand"),
    ("2026_CEPWD_602194_4", "30-Sep-2026 05:10 PM", "05-Oct-2026 04:00 PM", 850000, "PWD Nohar"),
    ("2026_CEPWD_602194_5", "30-Sep-2026 05:10 PM", "05-Oct-2026 06:00 PM", 950000, "PWD Nohar"),
    ("2026_CEPWD_602194_6", "30-Sep-2026 05:10 PM", "05-Oct-2026 04:00 PM", 780000, "PWD Nohar"),
    ("2026_CEPWD_602194_7", "30-Sep-2026 05:10 PM", "05-Oct-2026 06:00 PM", 900000, "PWD Nohar"),
    ("2026_CEPWD_602194_1", "30-Sep-2026 05:00 PM", "05-Oct-2026 04:00 PM", 850000, "PWD Nohar"),
    ("2026_CEPWD_602191_1", "30-Sep-2026 05:00 PM", "05-Oct-2026 06:00 PM", 750000, "PWD Nohar"),
    ("2026_CEPWD_602242_1", "30-Sep-2026 05:00 PM", "20-Oct-2026 06:00 PM", 2500000, "PWD City III"),
    ("2026_CEPWD_602194_2", "30-Sep-2026 05:00 PM", "05-Oct-2026 04:00 PM", 900000, "PWD Nohar"),
    ("2026_CEPWD_602195_1", "30-Sep-2026 04:30 PM", "07-Oct-2026 11:30 AM", 600000, "PWD Dudu"),
    # Page 2 (S.No 21 - 40)
    ("2026_CEPWD_602197_1", "30-Sep-2026 04:30 PM", "07-Oct-2026 06:00 PM", 650000, "PWD Nawalgarh"),
    ("2026_CEPWD_602197_2", "30-Sep-2026 04:25 PM", "07-Oct-2026 06:00 PM", 550000, "PWD Nawalgarh"),
    ("2026_CEPWD_602197_3", "30-Sep-2026 04:20 PM", "07-Oct-2026 06:00 PM", 700000, "PWD Nawalgarh"),
    ("2026_CEPWD_602074_1", "30-Sep-2026 04:15 PM", "06-Oct-2026 06:00 PM", 400000, "PWD Neem-Ka-Thana"),
    ("2026_CEPWD_602128_3", "30-Sep-2026 03:30 PM", "04-Oct-2026 06:00 PM", 1804000, "PWD Chirawa"),
    ("2026_CEPWD_602128_2", "30-Sep-2026 03:30 PM", "04-Oct-2026 06:00 PM", 873000, "PWD Chirawa"),
    ("2026_CEPWD_602128_6", "30-Sep-2026 03:30 PM", "04-Oct-2026 06:00 PM", 495000, "PWD Chirawa"),
    ("2026_CEPWD_602128_1", "30-Sep-2026 03:30 PM", "04-Oct-2026 06:00 PM", 4896000, "PWD Chirawa"),
    ("2026_CEPWD_602128_5", "30-Sep-2026 03:30 PM", "04-Oct-2026 06:00 PM", 1000000, "PWD Chirawa"),
    ("2026_CEPWD_602128_4", "30-Sep-2026 03:30 PM", "04-Oct-2026 06:00 PM", 792000, "PWD Chirawa"),
    ("2026_CEPWD_602126_1", "30-Sep-2026 03:15 PM", "23-Oct-2026 06:00 PM", 3500000, "PWD Alwar"),
    ("2026_CEPWD_602119_1", "30-Sep-2026 03:15 PM", "12-Oct-2026 06:00 PM", 17574000, "PWD Bhilwara"),
    ("2026_CEPWD_601957_1", "30-Sep-2026 02:30 PM", "08-Oct-2026 06:00 PM", 1500000, "PWD Churu"),
    ("2026_CEPWD_601931_13", "30-Sep-2026 02:20 PM", "22-Oct-2026 06:00 PM", 4200000, "PWD Khairthal"),
    ("2026_CEPWD_601931_12", "30-Sep-2026 02:15 PM", "22-Oct-2026 06:00 PM", 5100000, "PWD Khairthal"),
    ("2026_CEPWD_601931_11", "30-Sep-2026 02:05 PM", "22-Oct-2026 06:00 PM", 3800000, "PWD Khairthal"),
    ("2026_CEPWD_602061_1", "30-Sep-2026 02:00 PM", "26-Oct-2026 06:00 PM", 2900000, "PWD Bali"),
    ("2026_CEPWD_601931_10", "30-Sep-2026 01:55 PM", "22-Oct-2026 06:00 PM", 4600000, "PWD Khairthal"),
    ("2026_CEPWD_601931_9", "30-Sep-2026 01:50 PM", "22-Oct-2026 06:00 PM", 5300000, "PWD Khairthal"),
    ("2026_CEPWD_602014_1", "30-Sep-2026 01:20 PM", "08-Oct-2026 03:00 PM", 800000, "PWD City-I Jaipur"),
]

# Process Records
results = [audit_record(*row) for row in RAW_DATA]
df = pd.DataFrame(results)

# Quantitative Metrics
c1, c2, c3, c4 = st.columns(4)
total_count = len(df)
crit_count = len(df[df["Compliance Status"] == "CRITICAL VIOLATION"])
mod_count = len(df[df["Compliance Status"] == "MODERATE DEFICIT"])
comp_count = len(df[df["Compliance Status"] == "COMPLIANT"])

c1.metric("Sample Size", total_count)
c2.metric("Critical Violations (<5d)", crit_count, delta=f"{round((crit_count/total_count)*100, 1)}%", delta_color="inverse")
c3.metric("Moderate Deficits", mod_count, delta=f"{round((mod_count/total_count)*100, 1)}%", delta_color="inverse")
c4.metric("Compliant Tenders", comp_count, delta=f"{round((comp_count/total_count)*100, 1)}%")

st.markdown("---")

tab1, tab2 = st.tabs(["📊 Empirical Audit Registry", "🔍 Real-Time Tender Verifier"])

with tab1:
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        selected_depts = st.multiselect("Filter by Department / Division", options=sorted(df["Department"].unique()), default=sorted(df["Department"].unique()))
    with col_f2:
        selected_status = st.multiselect("Filter by Statutory Status", options=df["Compliance Status"].unique(), default=df["Compliance Status"].unique())
        
    filtered = df[(df["Department"].isin(selected_depts)) & (df["Compliance Status"].isin(selected_status))]
    st.dataframe(filtered, use_container_width=True, height=450)

with tab2:
    st.subheader("Audit a Single Custom Tender Notice")
    col1, col2 = st.columns(2)
    with col1:
        u_id = st.text_input("Tender ID / Ref", "2026_CUSTOM_01")
        u_cost = st.number_input("Estimated Procurement Value (INR)", value=1500000, step=100000)
        u_dept = st.text_input("Department / Circle", "PWD Division X")
    with col2:
        u_pub = st.text_input("Published Timestamp", "30-Sep-2026 03:30 PM")
        u_close = st.text_input("Bid Closing Timestamp", "05-Oct-2026 06:00 PM")
        
    if st.button("Run Compliance Audit"):
        res = audit_record(u_id, u_pub, u_close, u_cost, u_dept)
        if res:
            if res["Compliance Status"] == "CRITICAL VIOLATION":
                st.error(f"🚨 CRITICAL NON-COMPLIANCE: Window is {res['Window (Days)']} days. RTPP Rule 43 requires {res['Statutory Mandate']}. Deficit: {res['Deficit (Days)']} days.")
            elif res["Compliance Status"] == "MODERATE DEFICIT":
                st.warning(f"⚠️ MODERATE DEFICIT: Window is {res['Window (Days)']} days (Mandate: {res['Statutory Mandate']}).")
            else:
                st.success(f"✅ FULLY COMPLIANT: Window is {res['Window (Days)']} days (Satisfies {res['Statutory Mandate']} requirement).")
