import streamlit as st

st.set_page_config(page_title="PharmaDeliver", page_icon="💊", layout="centered")

# Initialize session state for cart
if 'cart' not in st.session_state:
    st.session_state.cart = []

page = st.sidebar.selectbox(
    "Menu", ["🏠 Home", "📦 New Order", "📋 My Orders", "👤 Profile"]
)

st.title("💊 PharmaDeliver")
st.markdown("**Medication Delivery from Your Pharmacy**")

if page == "🏠 Home":
    st.header("Welcome!")
    st.write("Fast & Reliable Medicine Delivery")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Orders Today", "18")
    with col2:
        st.metric("Pending Prescriptions", "7")
    
    if st.button("Place New Order", type="primary", use_container_width=True):
        st.switch_page("pages/02_New_Order.py")  # We'll improve this first

elif page == "📦 New Order":
    st.header("🛒 New Medication Order")
    
    tab1, tab2 = st.tabs(["📄 Upload Prescription", "🔍 Manual Order"])
    
    with tab1:
        st.write("Upload clear photo of your prescription")
        uploaded_file = st.file_uploader("Choose image or PDF", type=['jpg', 'jpeg', 'png', 'pdf'])
        if uploaded_file:
            st.image(uploaded_file, caption="Prescription Preview", use_column_width=True)
        
        notes = st.text_area("Additional Notes (e.g. urgency, allergies)", height=100)
        
        if st.button("Submit Prescription for Review", type="primary"):
            st.success("✅ Prescription submitted! We will review it within 30 minutes.")
            st.info("You will be notified once approved.")

    with tab2:
        st.write("Add medicines manually (good for refills & OTC)")
        col1, col2 = st.columns([3,1])
        with col1:
            med_name = st.text_input("Medicine Name + Strength")
        with col2:
            qty = st.number_input("Quantity", min_value=1, value=10)
        
        if st.button("Add to Cart"):
            if med_name:
                st.session_state.cart.append({"medicine": med_name, "qty": qty})
                st.success(f"Added: {qty} × {med_name}")
            else:
                st.warning("Please enter medicine name")

        # Show Cart
        if st.session_state.cart:
            st.subheader("Your Cart")
            for i, item in enumerate(st.session_state.cart):
                st.write(f"{item['qty']} × {item['medicine']}")
            
            if st.button("Clear Cart"):
                st.session_state.cart = []
                st.rerun()

    # Delivery Details
    st.subheader("Delivery Details")
    address = st.text_area("Delivery Address", placeholder="Full address with landmarks")
    phone = st.text_input("Recipient Phone Number", value="+")
    
    if st.button("Submit Order", type="primary", use_container_width=True):
        if st.session_state.cart or uploaded_file:
            st.success("🎉 Order Submitted Successfully!")
            st.balloons()
        else:
            st.error("Please add items or upload prescription")

else:
    st.info("This page is under development.")

st.caption("Pharma Delivery App • Safe & Trusted")
