import streamlit as st

st.set_page_config(page_title="PharmaDeliver", page_icon="💊", layout="wide")

# Sidebar
st.sidebar.title("PharmaDeliver")
role = st.sidebar.radio("Select Role", ["Patient View", "Pharmacist Dashboard"])

st.title("💊 PharmaDeliver")
st.caption("Medication Delivery from Your Pharmacy")

if role == "Patient View":
    st.header("New Medication Order")
    
    tab1, tab2 = st.tabs(["📄 Upload Prescription", "🔍 Manual Order"])
    
    with tab1:
        st.write("Upload clear photo of your prescription")
        uploaded = st.file_uploader("Choose image or PDF", type=['jpg','png','jpeg','pdf'])
        if uploaded:
            st.image(uploaded, caption="Prescription")
        notes = st.text_area("Additional Notes (urgency, allergies, etc.)")
        if st.button("Submit Prescription for Review", type="primary"):
            st.success("✅ Prescription submitted! We will review it shortly.")
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            med = st.text_input("Medicine Name")
            qty = st.number_input("Quantity", min_value=1, value=1)
        with col2:
            if st.button("Add to Cart"):
                st.success(f"Added {qty} × {med}")
    
    st.subheader("Delivery Details")
    address = st.text_area("Delivery Address")
    phone = st.text_input("Recipient Phone Number")
    if st.button("Submit Order", type="primary"):
        st.success("Order placed successfully! Order #PD-1001")

else:  # Pharmacist Dashboard
    st.header("🧑‍⚕️ Pharmacist Dashboard")
    
    tab1, tab2, tab3 = st.tabs(["📋 Pending Prescriptions", "📦 Active Orders", "📊 Today Summary"])
    
    with tab1:
        st.subheader("Pending Prescriptions")
        col1, col2 = st.columns([3,1])
        with col1:
            st.write("**Order #PD-1001** - John Doe")
            st.write("Phone: +254712345678")
            st.image("https://via.placeholder.com/600x400?text=Prescription+Image", caption="Uploaded Prescription")
        with col2:
            if st.button("✅ Approve"):
                st.success("Order Approved")
            if st.button("❌ Reject"):
                st.error("Order Rejected")
    
    with tab2:
        st.write("Active Orders (Being Prepared / Out for Delivery)")
        st.info("No active orders yet (demo)")
    
    with tab3:
        st.metric("Orders Today", "8")
        st.metric("Pending Review", "3")
        st.metric("Revenue Today", "$245")

st.sidebar.caption("Built for safe medication delivery")
