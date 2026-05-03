import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="PharmaDeliver", page_icon="💊", layout="wide")

# Initialize session state
if 'orders' not in st.session_state:
    st.session_state.orders = []

st.title("💊 PharmaDeliver")
st.caption("Medication Delivery from Your Trusted Pharmacy")

# Role Selection
role = st.sidebar.selectbox("Select Your Role", ["Patient", "Pharmacist"])

if role == "Patient":
    st.header("Welcome, Patient 👋")
    
    menu = st.radio("What would you like to do?", 
                   ["Place New Order", "My Orders"], horizontal=True)
    
    if menu == "Place New Order":
        st.subheader("New Medication Order")
        
        tab1, tab2 = st.tabs(["📄 Upload Prescription", "🔍 Manual / OTC Order"])
        
        with tab1:
            uploaded = st.file_uploader("Upload Prescription Photo or PDF", 
                                      type=['jpg', 'jpeg', 'png', 'pdf'])
            if uploaded:
                st.image(uploaded, width=500)
            
            col1, col2 = st.columns(2)
            with col1:
                address = st.text_area("Delivery Address", height=100)
            with col2:
                recipient_phone = st.text_input("Recipient Phone Number")
            
            notes = st.text_area("Additional Notes (Allergies, Urgency, etc.)")
            
            if st.button("🚀 Submit Prescription for Review", type="primary", use_container_width=True):
                new_order = {
                    "id": f"PD-{1000 + len(st.session_state.orders)}",
                    "type": "Prescription",
                    "status": "Pending Review",
                    "address": address,
                    "phone": recipient_phone,
                    "notes": notes,
                    "time": datetime.now().strftime("%d %b %H:%M")
                }
                st.session_state.orders.append(new_order)
                st.success(f"✅ Order {new_order['id']} submitted successfully!")
        
        with tab2:
            st.info("Manual order feature coming soon...")
    
    elif menu == "My Orders":
        st.subheader("My Orders")
        if st.session_state.orders:
            df = pd.DataFrame(st.session_state.orders)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("You have no orders yet.")

else:  # Pharmacist Dashboard
    st.header("🧑‍⚕️ Pharmacist Dashboard")
    
    tabs = st.tabs(["📋 Pending Prescriptions", "🚚 Active Orders", "📊 Overview"])
    
    with tabs[0]:
        st.subheader("Pending Prescriptions")
        pending = [o for o in st.session_state.orders if o["status"] == "Pending Review"]
        
        if pending:
            for order in pending:
                with st.expander(f"📌 Order {order['id']} - {order['phone']}"):
                    st.write(f"**Address:** {order['address']}")
                    st.write(f"**Time:** {order['time']}")
                    st.write(f"**Notes:** {order.get('notes', 'None')}")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Approve", key=order['id']):
                            order["status"] = "Approved - Preparing"
                            st.rerun()
                    with col2:
                        if st.button("❌ Reject", key=order['id']+"r"):
                            order["status"] = "Rejected"
                            st.rerun()
        else:
            st.info("No pending prescriptions")
    
    with tabs[1]:
        st.subheader("Active / In Progress Orders")
        active = [o for o in st.session_state.orders if "Approved" in o["status"]]
        for order in active:
            st.success(f"Order {order['id']} → {order['status']}")
    
    with tabs[2]:
        total = len(st.session_state.orders)
        pending_count = len([o for o in st.session_state.orders if o["status"] == "Pending Review"])
        st.metric("Total Orders", total)
        st.metric("Pending Review", pending_count)

st.sidebar.info("Switch role from sidebar")
