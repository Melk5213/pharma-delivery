import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="PharmaDeliver", page_icon="💊", layout="wide")

# Fake database (will be replaced with real DB later)
if 'orders' not in st.session_state:
    st.session_state.orders = []

st.sidebar.title("💊 PharmaDeliver")
role = st.sidebar.radio("Mode", ["Patient", "Pharmacist"])

st.title("PharmaDeliver - Medication Delivery")

if role == "Patient":
    st.header("Place New Order")
    
    tab1, tab2 = st.tabs(["📄 Upload Prescription", "🔍 Manual Order"])
    
    with tab1:
        st.subheader("Upload Prescription")
        uploaded = st.file_uploader("Upload clear prescription", type=['jpg','png','jpeg','pdf'])
        if uploaded:
            st.image(uploaded, width=400)
        notes = st.text_area("Notes (urgency, allergies, etc.)")
        address = st.text_area("Delivery Address")
        recipient_phone = st.text_input("Recipient Phone Number")
        
        if st.button("Submit Prescription", type="primary"):
            new_order = {
                "id": f"PD-{len(st.session_state.orders)+1001}",
                "type": "Prescription",
                "status": "Pending Review",
                "address": address,
                "phone": recipient_phone,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state.orders.append(new_order)
            st.success(f"Order {new_order['id']} submitted successfully!")

    with tab2:
        st.subheader("Manual Order (OTC/Refill)")
        med = st.text_input("Medicine Name & Strength")
        qty = st.number_input("Quantity", min_value=1, value=1)
        if st.button("Add Item & Proceed"):
            st.info("Cart feature coming in next update")

    # My Orders
    if st.session_state.orders:
        st.subheader("My Recent Orders")
        df = pd.DataFrame(st.session_state.orders)
        st.dataframe(df, use_container_width=True)

else:  # Pharmacist Mode
    st.header("🧑‍⚕️ Pharmacist Dashboard")
    
    tab1, tab2, tab3 = st.tabs(["📋 Pending Review", "🚚 Active Orders", "📊 Summary"])
    
    with tab1:
        st.subheader("Pending Prescriptions")
        pending = [o for o in st.session_state.orders if o["status"] == "Pending Review"]
        
        for order in pending:
            with st.expander(f"Order {order['id']} - {order['phone']}"):
                st.write(f"**Address:** {order['address']}")
                st.write(f"**Submitted:** {order['time']}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Approve", key=order['id']):
                        order["status"] = "Approved - Preparing"
                        st.success("Approved!")
                with col2:
                    if st.button("❌ Reject", key=order['id']+"rej"):
                        order["status"] = "Rejected"
                        st.error("Rejected")
    
    with tab2:
        st.subheader("Active Orders")
        active = [o for o in st.session_state.orders if "Approved" in o["status"]]
        for order in active:
            st.write(f"Order {order['id']} → {order['status']}")
    
    with tab3:
        st.metric("Total Orders Today", len(st.session_state.orders))
        st.metric("Pending Review", len([o for o in st.session_state.orders if o["status"] == "Pending Review"]))

st.sidebar.success("App Updated")
