import requests
import zipfile
import json
import io
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()


def export_survey(api_token: str, survey_id: str, data_center: str, file_format: str) -> str:
    """
    Export survey responses from Qualtrics API.
    Returns the path to the downloaded CSV file.
    """
    base_url = f"https://{data_center}.qualtrics.com/API/v3/surveys/{survey_id}/export-responses/"
    headers = {
        "Content-Type": "application/json",
        "X-API-TOKEN": api_token,
    }

    # Step 1: Initiating data export
    download_request_payload = {
        "format": file_format,
        "useLabels": True  # Use human-readable labels
    }

    response = requests.post(base_url, json=download_request_payload, headers=headers)
    response.raise_for_status()
    progress_id = response.json()["result"]["progressId"]

    # Step 2: Checking export progress
    progress_status = "inProgress"
    while progress_status not in ["complete", "failed"]:
        progress_url = f"{base_url}{progress_id}"
        progress_response = requests.get(progress_url, headers=headers)
        progress_response.raise_for_status()

        progress_status = progress_response.json()["result"]["status"]
        progress_percent = progress_response.json()["result"]["percentComplete"]
        print(f"Export progress: {progress_percent}% complete")

        if progress_status == "failed":
            raise Exception("Export failed.")

    file_id = progress_response.json()["result"]["fileId"]

    # Step 3: Downloading the exported file
    download_url = f"{base_url}{file_id}/file"
    download_response = requests.get(download_url, headers=headers, stream=True)
    download_response.raise_for_status()

    # Step 4: Unzipping the downloaded file
    output_dir = "MyQualtricsDownload"
    os.makedirs(output_dir, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(download_response.content)) as zf:
        zf.extractall(output_dir)

    print(f"Export complete. Files extracted to '{output_dir}'.")
    return os.path.join(output_dir, "response.csv")


def convert_to_xlsx(csv_file: str, output_xlsx: str) -> None:
    """
    Convert CSV to XLSX for better usability.
    """
    df = pd.read_csv(csv_file)
    df.to_excel(output_xlsx, index=False)
    print(f"File converted to XLSX: {output_xlsx}")


def main():
    """
    Main function to execute the Qualtrics export and conversion process.
    """
    api_token = os.getenv("APIKEY")
    data_center = os.getenv("DATACENTER")
    survey_id = os.getenv("SURVEYID")  # Survey ID from .env
    file_format = os.getenv("FILEFORMAT", "csv")  # Default to CSV if not specified

    if not api_token or not data_center or not survey_id:
        print("Environment variables 'APIKEY', 'DATACENTER', and 'SURVEYID' are required.")
        return

    try:
        # Export survey responses
        csv_file = export_survey(api_token, survey_id, data_center, file_format)

        # Convert CSV to XLSX
        output_xlsx = "MyQualtricsDownload/cleaned_responses.xlsx"
        convert_to_xlsx(csv_file, output_xlsx)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()


