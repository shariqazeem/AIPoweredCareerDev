# core/services.py
import requests

def get_career_recommendations(profile_data):
    # Replace with your Gemini API endpoint and API key
    url = "https://api.gemini.com/v1/recommendations"
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=profile_data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None
# core/services.py
def get_job_postings(profile_data):
    url = "https://api.gemini.com/v1/job_postings"
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=profile_data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None
