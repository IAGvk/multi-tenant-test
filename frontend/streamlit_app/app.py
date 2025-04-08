import streamlit as st
from utils.api_client import login_user, create_user, query_llm
from utils.logger import get_logger
from sections import page_1, page_2, page_3


logger = get_logger(__name__)  # Use the centralized logger

# Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.token = None
    st.session_state.tenant_name = None
    st.session_state.user_id = None

st.title("Multi-Tenant LLM App")

# Add tenant selection dropdown
tenant_options = ["tenant_1", "tenant_2"]

if not st.session_state.logged_in:
    # Login Form
    with st.form("login_form"):
        tenant_name = st.selectbox("Tenant Name", tenant_options)
        user_id = st.text_input("User ID")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            logger.debug("Login form submitted")
            response = login_user(tenant_name, user_id, password)
            logger.debug(f"Login response: {response}")
            if response.get("token"):
                st.session_state.logged_in = True
                st.session_state.token = response["token"]
                st.session_state.tenant_name = tenant_name 
                st.session_state.user_id = user_id
                st.success("Login successful! Rerun the page for homescreen")
            else:
                st.error("Invalid credentials. Please try again.")
    # Registration Form
    with st.expander("Don't have an account? Register below:"):
        with st.form("registration_form"):
            reg_tenant_name = st.selectbox("Tenant", tenant_options)
            reg_user_id = st.text_input("User ID (Registration)")
            reg_password = st.text_input("Password (Registration)", type="password")
            reg_submitted = st.form_submit_button("Register")

            if reg_submitted:
                logger.debug("Registration form submitted")
                reg_response = create_user(reg_tenant_name, reg_user_id, reg_password)
                logger.debug(f"Registration response: {reg_response}")
                if "error" not in reg_response:
                    st.success("Registration successful! You can now log in.")
                else:
                    st.error(f"Registration failed: {reg_response.get('error', 'Unknown error')}")

else:
    st.success(f"Logged in as User {st.session_state.user_id} under Tenant {st.session_state.tenant_name}")
    logger.debug(f"User {st.session_state.user_id} logged in under Tenant {st.session_state.tenant_name}")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    pages = {
        "Architecture Input": "page_1",
        "Initial Analysis": "page_2",
        "RAG Enhanced Analysis": "page_3"
    }
    
    selected_page = st.sidebar.radio("Go to", list(pages.keys()))
    st.session_state.current_page = pages[selected_page]

    # Display current page
    if st.session_state.current_page == "page_1":
        page_1.show()
    elif st.session_state.current_page == "page_2":
        page_2.show()
    elif st.session_state.current_page == "page_3":
        page_3.show()