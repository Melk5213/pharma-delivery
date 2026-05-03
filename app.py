import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="PharmaDeliver", page_icon="💊", layout="wide")

# Initialize session state
if 'orders' not in st.session_state:
    st.session_state.orders = []

st.sidebar.title("💊 PharmaDeliver")
role = st.sidebar.selectbox("Login as", ["Patient", "Pharmacist"])

st.title("PharmaDeliver")
st.caption("**Safe Medication Delivery from Your Pharmacy**")

if role == "Patient":
    st.header("Welcome! 👋")
    
    menu = st.radio("Main Menu", ["🛒 Place New Order", "📦 My Orders", "🛍️ Quick OTC"], horizontal=True)
    
    if menu == "🛒 Place New Order":
        st.subheader("New Order")
        
        order_type = st.radio("Order Type", ["Upload Prescription", "Manual Order (OTC/Refill)"])
        
        if order_type == "Upload Prescription":
            st.write("**Upload your prescription**")
            uploaded_file = st.file_uploader("Choose Image or PDF", type=["jpg", "jpeg", "png", "pdf"])
            if uploaded_file:
                st.image(uploaded_file, width=400)
            
            col1, col2 = st.columns(2)
            with col1:
                address = st.text_area("Delivery Address", placeholder="Full address with landmarks")
            with col2:
                recipient_phone = st.text_input("Recipient Phone Number")
            
            notes = st.text_area("Additional Notes (Allergies, Urgency, etc.)", height=80)
            
            if st.button("Submit Prescription for Review", type="primary", use_container_width=True):
                new_order = {
                    "id": f"PD-{1000 + len(st.session_state.orders)}",
                    "type": "Prescription",
                    "status": "Pending Review",
                    "address": address,
                    "phone": recipient_phone,
                    "notes": notes,
                    "time": datetime.now().strftime("%d %b %H:%M"),
                    "items": "Prescription Items"
                }
                st.session_state.orders.append(new_order)
                st.success(f"✅ Order **{new_order['id']}** submitted successfully!")
                st.balloons()
        
        else:
            st.info("Manual OTC order with cart coming in next version")
    
    elif menu == "📦 My Orders":
        st.subheader("My Orders")
        if st.session_state.orders:
            df = pd.DataFrame(st.session_state.orders)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No orders yet. Place your first order!")
    
    else:
        st.info("Quick OTC section coming soon...")

else:  # ==================== PHARMACIST DASHBOARD ====================
    st.header("🧑‍⚕️ Pharmacist Dashboard")
    
    tab1, tab2, tab3 = st.tabs(["📋 Pending Prescriptions", "🚚 Active Orders", "📊 Overview"])
    
    with tab1:
        st.subheader("Pending Prescriptions")
        pending = [o for o in st.session_state.orders if o.get("status") == "Pending Review"]
        
        if pending:
            for order in pending:
                with st.expander(f"Order {order['id']} — {order['phone']}"):
                    st.write(f"**Address:** {order['address']}")
                    st.write(f"**Time:** {order['time']}")
                    st.write(f"**Notes:** {order.get('notes', 'No notes')}")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("✅ Approve", key=order['id']):
                            order["status"] = "Approved - Preparing"
                            st.rerun()
                    with col2:
                        if st.button("🚚 Out for Delivery", key=order['id']+"d"):
                            order["status"] = "Out for Delivery"
                            st.rerun()
                    with col3:
                        if st.button("❌ Reject", key=order['id']+"r"):
                            order["status"] = "Rejected"
                            st.rerun()
        else:
            st.success("No pending prescriptions. Great job!")
    
    with tab2:
        st.subheader("Active & Recent Orders")
        active = [o for o in st.session_state.orders if o.get("status") != "Pending Review"]
        if active:
            df_active = pd.DataFrame(active)
            st.dataframe(df_active, use_container_width=True)
        else:
            st.info("No active orders")
    
    with tab3:
        total_orders = len(st.session_state.orders)
        pending_count = len([o for o in st.session_state.orders if o.get("status") == "Pending Review"])
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Orders", total_orders)
        col2.metric("Pending Review", pending_count)
        col3.metric("Completed", total_orders - pending_count)

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Version 1.0\nBuilt for safe & trusted delivery")
