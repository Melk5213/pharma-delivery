import streamlit as st
from datetime import datetime

st.set_page_config(page_title="PharmaDeliver", page_icon="💊", layout="centered")

page = st.sidebar.selectbox(
    "Menu",
    ["🏠 Home", "📦 New Order", "📋 My Orders", "👤 Profile"]
)

st.title("💊 PharmaDeliver")
st.markdown("**Medication Delivery from Your Pharmacy**")

if page == "🏠 Home":
    st.header("Welcome!")
    st.write("Fast & Reliable Medicine Delivery")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Orders Today", "12")
    with col2:
        st.metric("Pending Prescriptions", "5")
    
    if st.button("Place New Order", type="primary", use_container_width=True):
        st.success("New Order page coming soon...")

elif page == "📦 New Order":
    st.header("New Medication Order")
    order_type = st.radio("How would you like to order?", 
                         ["Upload Prescription", "Manual / OTC Order"])
    
    if order_type == "Upload Prescription":
        uploaded_file = st.file_uploader("Upload Prescription (image or PDF)", type=['jpg', 'jpeg', 'png', 'pdf'])
        if uploaded_file:
            st.image(uploaded_file, caption="Prescription")
        notes = st.text_area("Additional Notes")
        if st.button("Submit for Review"):
            st.success("✅ Prescription submitted successfully!")
    
    else:
        med = st.text_input("Medicine Name")
        qty = st.number_input("Quantity", min_value=1, value=10)
        if st.button("Add to Cart"):
            st.success(f"Added {qty} × {med}")

else:
    st.info("This section is under development.")

st.caption("Pharma Delivery App - Built by You")
