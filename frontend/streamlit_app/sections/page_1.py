import streamlit as st
from PIL import Image
from utils.api_client import submit_architecture_review
import time

def show():
    st.title("Architecture Review Input")
    
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        question1 = st.radio("Is this an Internet facing application?", ("Yes", "No"))
        question2 = st.selectbox(
            "What is the sensitivity of data involved?", 
            ["PUBLIC", "INTERNAL", "PROTECTED", "HIGHLY PROTECTED"]
        )
        question3a = st.text_input(
            "What are the existing components of this architecture from review standpoint?"
        )
        question3b = st.text_input(
            "What are the new components being added for review in this architecture?"
        )
        question4 = st.text_input(
            "What are the hosting attributes for this architecture?",
            help="If left blank, the model infers this from the architecture diagram"
        )

    with col2:
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Architecture", use_container_width=True)

    if st.button("Submit"):
        if "token" not in st.session_state:
            st.error("Please login first")
            return
            
        # Store inputs in session state
        review_data = {
            "internet_facing": question1,
            "data_sensitivity": question2,
            "existing_components": question3a,
            "new_components": question3b,
            "hosting_attributes": question4
        }
        
        
        # Submit to backend
        with st.spinner("Processing architecture review..."):
            response = submit_architecture_review(
                st.session_state.token,
                review_data
            )
            
            if "error" not in response:
                st.session_state.review_inputs = review_data
                st.session_state.transitioning = True
                st.success("Review submitted successfully!")
                st.session_state.show_page = "page_2"
                time.sleep(3)
                st.rerun()
            else:
                st.error(f"Error submitting review: {response.get('error')}")