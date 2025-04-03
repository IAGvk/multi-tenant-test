import requests

BASE_URL = "http://localhost:8000/api/v1"

def login_user(tenant_id: str, user_id: str, password: str) -> dict:
    url = f"{BASE_URL}/auth/login"
    payload = {"tenant_id": tenant_id, "user_id": user_id, "password": password}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def query_llm(token: str, question: str, context: str) -> str:
    url = f"{BASE_URL}/llm/query"
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"question": question, "context": context}
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("answer", "No response from LLM.")
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"