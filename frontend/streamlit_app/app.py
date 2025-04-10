import streamlit as st
from utils.api_client import login_user, create_user, query_llm
from utils.logger import get_logger
from sections import page_1, page_2, page_3, page_4
import time


logger = get_logger(__name__)  # Use the centralized logger

def init_session_state():
    if "show_page" not in st.session_state:
        st.session_state.show_page = "page_1"
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.token = None
        st.session_state.tenant_name = None
        st.session_state.user_id = None

def setup_page_config():
    st.set_page_config(
        page_title="Multi-Tenant LLM App",
        layout="wide",
    )

def setup_sidebar_styling():
    st.markdown("""
        <style>
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
        }
        .stButton, .stRadio, .stCheckbox {
            margin-bottom: 1rem;
        }
        div[data-testid="stSidebarNav"] {
            position: fixed;
            top: 0;
            left: 0;
            height: 100%;
            background-color: #f8f9fa;
        }
        </style>
    """, unsafe_allow_html=True)

def show_navigation_sidebar():
    st.sidebar.title("Navigation")
    pages = {
        "Architecture Input": "page_1",
        "Initial Analysis": "page_2",
        "RAG Enhanced Analysis": "page_3",
        "Final Analysis": "page_4"
    }
    
    # Show current user info
    st.sidebar.success(f"User: {st.session_state.user_id}\nTenant: {st.session_state.tenant_name}")
    
    # Highlight current page in navigation
    for page_name, page_id in pages.items():
        if page_id == st.session_state.show_page:
            st.sidebar.markdown(
                f'<div style="background-color: #e6e6e6; padding: 0.5rem; border-radius: 5px;"><b>{page_name}</b></div>',
                unsafe_allow_html=True
            )
        else:
            # Make page name clickable
            if st.sidebar.button(page_name, key=f"nav_{page_id}"):
                st.session_state.show_page = page_id
                st.rerun()

def show_login_form(tenant_options):
    with st.form("login_form"):
        tenant_name = st.selectbox("Tenant Name", tenant_options)
        user_id = st.text_input("User ID")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            logger.debug("Login form submitted")
            response = login_user(tenant_name, user_id, password)
            if response.get("token"):
                st.session_state.logged_in = True
                st.session_state.token = response["token"]
                st.session_state.tenant_name = tenant_name
                st.session_state.user_id = user_id
                st.success("Login successful!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")

def show_registration_form(tenant_options):
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


def show_app_content():
    show_navigation_sidebar()
    
    # Show current page content
    if st.session_state.show_page == "page_1":
        page_1.show()
    elif st.session_state.show_page == "page_2":
        page_2.show()
    elif st.session_state.show_page == "page_3":
        page_3.show()
    elif st.session_state.show_page == "page_4":
        page_4.show()


def show_auth_page():
    st.title("Welcome to ARKI")
    st.subheader("Multi-tenant LLM App for architecture review.")
    st.write("Please log in to continue.")

    tenant_options = ["tenant_1", "tenant_2"]
    col1, col2 = st.columns([1, 1])   
    with col1:
        show_login_form(tenant_options)
    with col2:
        with st.expander("Don't have an account? Register below:"):
            show_registration_form(tenant_options)


def main():
    setup_page_config()
    init_session_state()
    setup_sidebar_styling()
    
    if not st.session_state.logged_in:
        show_auth_page()
    else:
        show_app_content()


if __name__ == "__main__":
    main()