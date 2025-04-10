import streamlit as st
from utils.api_client import get_rag_enriched_response
import time

def show():
    st.title("RAG-Enriched Analysis")
    
    # Show success message if transitioning from previous page
    if st.session_state.get('transitioning'):
        st.success("Retrieving similar cases...")
        del st.session_state.transitioning


    if "llm_response" not in st.session_state:
        st.warning("Please complete the initial analysis first")
        return
    
    if "rag_results" not in st.session_state:
        with st.spinner("Retrieving similar cases..."):
            rag_response = get_rag_enriched_response(
                st.session_state.token,
                st.session_state.llm_response
            )
            if "error" in rag_response:
                st.error(f"Error: {rag_response['error']}")
                return
            st.session_state.rag_results = rag_response
            # st.session_state.rag_results = rag_response.get("retrieved_contexts", [])
    
    # Display initial analysis
    st.subheader("Initial Analysis")
    st.text_area("", st.session_state.rag_results["answer"], height=200)
    
    # Display and select from retrieved cases
    st.subheader("Retrieved Similar Cases")
    selected_cases = []
    
    for case in st.session_state.rag_results.get("retrieved_contexts", []):
        col1, col2 = st.columns([0.1, 0.9])
        with col1:
            if st.checkbox("", key=f"case_{case['id']}"):
                selected_cases.append(case['text'])
        with col2:
            st.text_area(
                f"Similarity: {case['score']}", 
                case['text'], 
                height=100,
                key=f"text_{case['id']}"
            )
    
    if selected_cases:
        if st.button("Proceed to Final Analysis"):
            st.session_state.selected_cases = selected_cases
            st.session_state.transitioning = True
            st.success("Generating final analysis...")
            st.session_state.show_page = "page_4"
            time.sleep(2)
            st.rerun()