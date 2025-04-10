from utils.logger import get_logger
import requests

logger = get_logger(__name__)  # Use the centralized logger

BASE_URL = "http://backend:8000/api/v1/endpoints"

def create_user(tenant_name: str, user_id: str, password: str) -> dict:
    url = f"{BASE_URL}/user/create"
    payload = {
        "tenant_name": tenant_name,
        "user_id": user_id,
        "password": password
    }
    logger.debug(f"Payload sent to create user: {payload}")
    try:
        response = requests.post(url, json=payload)
        logger.debug(f"Response from create user: {response.status_code} - {response.text}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during user creation: {e}")
        return {"error": str(e)}

def login_user(tenant_name: str, user_id: str, password: str) -> dict:
    url = f"{BASE_URL}/auth/login"
    payload = {
        "tenant_name": tenant_name,
        "user_id": user_id,
        "password": password
    }
    logger.debug(f"Payload sent to login: {payload}")
    try:
        response = requests.post(url, json=payload)
        logger.debug(f"Response from login: {response.status_code} - {response.text}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error during login: {e}")
        return {"error": str(e)}
        
def query_llm(token: str, question: str, context: str) -> str:
    url = f"{BASE_URL}/llm/query"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"question": question, "context": context}
    logger.debug(f"Payload sent to LLM: {payload}")
    try:
        response = requests.post(url, json=payload, headers=headers)
        logger.debug(f"Response from LLM: {response.status_code} - {response.text}")
        response.raise_for_status()
        return response.json().get("answer", "No response from LLM.")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error querying LLM: {e}")
        return f"Error: {str(e)}"


def get_rag_enriched_response(token: str, initial_response: str) -> dict:
    url = f"{BASE_URL}/llm/rag-query"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"initial_response": initial_response}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting RAG response: {e}")
        return f"Error: {str(e)}"

def get_final_analysis(token: str, initial_response: str, selected_contexts: list) -> dict:
    url = f"{BASE_URL}/llm/final-analysis"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "initial_response": initial_response,
        "selected_contexts": selected_contexts
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting final analysis: {e}")
        return f"Error: {str(e)}"

def submit_architecture_review(token: str, review_data: dict) -> dict:
    """Submit architecture review data to backend"""
    url = f"{BASE_URL}/llm/query"
    headers = {"Authorization": f"Bearer {token}"}
    
    # Format the review data into a structured question
    context = f"""
    Architecture Review Details:
    - Internet Facing: {review_data.get('internet_facing')}
    - Data Sensitivity: {review_data.get('data_sensitivity')}
    - Existing Components: {review_data.get('existing_components')}
    - New Components: {review_data.get('new_components')}
    - Hosting Attributes: {review_data.get('hosting_attributes')}
    """
    
    payload = {
        "question": "Analyze this architecture for security and compliance considerations",
        "context": context
    }
    
    logger.debug(f"Payload sent to architecture review: {payload}")
    try:
        response = requests.post(url, json=payload, headers=headers)
        logger.debug(f"Response from architecture review: {response.status_code} - {response.text}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error submitting architecture review: {e}")
        return {"error": str(e)}