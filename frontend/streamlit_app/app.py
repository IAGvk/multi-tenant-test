import streamlit as st
from utils.api_client import login_user, query_llm, create_pg_user
from utils.logger import get_logger

logger = get_logger(__name__)  # Use the centralized logger

# Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.token = None
    st.session_state.tenant_id = None
    st.session_state.user_id = None

st.title("Multi-Tenant LLM App")

if not st.session_state.logged_in:
    # Login Form
    with st.form("login_form"):
        tenant_id = st.text_input("Tenant ID")
        user_id = st.text_input("User ID")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            logger.debug("Login form submitted")
            response = login_user(tenant_id, user_id, password)
            logger.debug(f"Login response: {response}")
            if response.get("token"):
                st.session_state.logged_in = True
                st.session_state.token = response["token"]
                st.session_state.tenant_id = tenant_id
                st.session_state.user_id = user_id
                st.success("Login successful!")
            else:
                st.error("Invalid credentials. Please try again.")
    # Registration Form
    st.write("Don't have an account? Register below:")
    with st.form("registration_form"):
        reg_tenant_id = st.text_input("Tenant ID (Registration)")
        reg_user_id = st.text_input("User ID (Registration)")
        reg_password = st.text_input("Password (Registration)", type="password")
        reg_submitted = st.form_submit_button("Register")

        if reg_submitted:
            logger.debug("Registration form submitted")
            reg_response = create_pg_user(reg_tenant_id, reg_user_id, reg_password)
            logger.debug(f"Registration response: {reg_response}")
            if "error" not in reg_response:
                st.success("Registration successful! You can now log in.")
            else:
                st.error(f"Registration failed: {reg_response.get('error', 'Unknown error')}")

else:
    st.success(f"Logged in as User {st.session_state.user_id} under Tenant {st.session_state.tenant_id}")
    logger.debug(f"User {st.session_state.user_id} logged in under Tenant {st.session_state.tenant_id}")

    # File Upload for Context
    uploaded_file = st.file_uploader("Upload a context file", type=["txt"])
    context = ""
    if uploaded_file:
        context = uploaded_file.read().decode("utf-8")

    # Question Input
    question = st.text_input("Ask a question")

    if st.button("Submit"):
        if question and context:
            with st.spinner("Querying LLM..."):
                logger.debug(f"Querying LLM with question: {question} and context: {context}")
                response = query_llm(st.session_state.token, question, context)
                if response:
                    st.success(f"LLM Response: {response}")
                else:
                    st.error("Failed to get a response from the LLM.")
        else:
            st.error("Please provide both a question and context.")