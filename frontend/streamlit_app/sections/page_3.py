import streamlit as st
from utils.api_client import get_rag_enriched_response

def show():
    st.title("RAG-Enriched Analysis")
    
    if "llm_response" not in st.session_state:
        st.warning("Please complete the initial analysis first")
        return
    
    if "rag_response" not in st.session_state:
        with st.spinner("Enriching response with similar cases..."):
            rag_response = get_rag_enriched_response(
                st.session_state.token,
                st.session_state.llm_response
            )
            st.session_state.rag_response = rag_response
    
    st.text_area(
        "Final Enhanced Analysis",
        st.session_state.rag_response,
        height=400
    )