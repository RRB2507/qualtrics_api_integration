import requests
import os
import time

# Set your Qualtrics details here
CLIENT_ID = os.environ.get("QUALTRICS_CLIENT_ID")  # Replace with your client ID
CLIENT_SECRET = os.environ.get("QUALTRICS_CLIENT_SECRET")  # Replace with your client secret
DATA_CENTER = "sjc1"  # Replace with your Qualtrics data center (e.g., "sjc1", "iad1")
SURVEY_ID = "SV_abc123XYZ"  # Replace with your survey ID

# Token endpoint and API endpoints
TOKEN_URL = f"https://{DATA_CENTER}.qualtrics.com/oauth2/token"
EXPORT_URL = f"https://{DATA_CENTER}.qualtrics.com/API/v3/surveys/{SURVEY_ID}/export-responses"

def get_access_token(client_id, client_secret):
    """
    Generate an OAuth token using Client ID and Client Secret.
    """
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    response = requests.post(TOKEN_URL, data=payload)
    response.raise_for_status()
    return response.json()["access_token"]

def export_survey_responses(access_token):
    """
    Initiate the export of survey responses.
    """
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {"format": "csv"}
    response = requests.post(EXPORT_URL, json=payload, headers=headers)
    response.raise_for_status()
    progress_id = response.json()["result"]["progressId"]
    print(f"Export initiated. Progress ID: {progress_id}")
    return progress_id

def check_export_progress(access_token, progress_id):
    """
    Check the progress of the export.
    """
    url = f"{EXPORT_URL}/{progress_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    while True:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        progress_status = response.json()["result"]["status"]
        print(f"Progress: {progress_status}")
        if progress_status == "complete":
            file_url = response.json()["result"]["fileUrl"]
            print(f"Export complete. File available at: {file_url}")
            return file_url
        elif progress_status == "failed":
            raise Exception("Export failed.")
        time.sleep(5)  # Wait for 5 seconds before checking again

def download_file(access_token, file_url, output_path):
    """
    Download the exported file and save it locally.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(file_url, headers=headers)
    response.raise_for_status()
    with open(output_path, "wb") as file:
        file.write(response.content)
    print(f"File downloaded successfully: {output_path}")

if __name__ == "__main__":
    try:
        # Step 1: Get access token
        token = get_access_token(CLIENT_ID, CLIENT_SECRET)
        print("Access token generated successfully.")

        # Step 2: Export survey responses
        progress_id = export_survey_responses(token)

        # Step 3: Monitor progress
        file_url = check_export_progress(token, progress_id)

        # Step 4: Download the exported file
        output_file = "survey_responses.csv"
        download_file(token, file_url, output_file)

    except Exception as e:
        print(f"An error occurred: {e}")
