import streamlit as st
from utils.api_client import get_final_analysis
import time

def show():
    st.title("Final Enhanced Analysis")
    
    # Show success message if transitioning from previous page
    if st.session_state.get('transitioning'):
        st.success("Preparing final analysis...")
        del st.session_state.transitioning


    if "selected_cases" not in st.session_state:
        st.warning("Please select relevant cases first")
        return
    
    if "final_analysis" not in st.session_state:
        with st.spinner("Generating final analysis..."):
            final_response = get_final_analysis(
                st.session_state.token,
                st.session_state.llm_response,
                st.session_state.selected_cases
            )
            if "error" in final_response:
                st.error(f"Error: {final_response['error']}")
                return
            st.session_state.final_analysis = final_response
    
    st.markdown("### Final Analysis")
    st.markdown(st.session_state.final_analysis.get("answer", ""))
    
    st.text_area(
        "Final Enhanced Analysis",
        st.session_state.final_analysis,
        height=400
    )
    
    if st.button("Start New Analysis"):
        # Clear session state for new analysis
        for key in ['review_inputs', 'llm_response', 
                    'rag_results', 
                   'selected_cases', 'final_analysis',
                   'transitioning']:
            if key in st.session_state:
                del st.session_state[key]
        st.success("Starting new analysis...")
        st.session_state.show_page = "page_1"
        time.sleep(2)
        st.rerun()