import streamlit as st
from utils.api_client import query_llm

def show():
    st.title("Initial LLM Analysis")
    
    if "review_inputs" not in st.session_state:
        st.warning("Please submit the architecture review form first")
        return
    
    if "llm_response" not in st.session_state:
        with st.spinner("Getting LLM analysis..."):
            response = query_llm(
                st.session_state.token,
                "Analyze architecture",
                str(st.session_state.review_inputs)
            )
            st.session_state.llm_response = response
    
    st.text_area("LLM Analysis", st.session_state.llm_response, height=300)
    
    if st.button("Proceed to RAG-Enriched Response"):
        st.session_state.current_page = "page_3"
        st.rerun()