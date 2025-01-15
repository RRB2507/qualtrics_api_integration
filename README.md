

# **Qualtrics API Integration**

## **Overview**

This project provides a robust Python-based solution to interact with the **Qualtrics API** for exporting survey responses. It implements **OAuth 2.0** for secure authentication, automates data exports, and handles common API issues such as rate limits and transient failures.

---

## **Features**

- **Secure Authentication**: Utilizes **OAuth 2.0** to generate access tokens dynamically using `Client ID` and `Client Secret`.
- **Automated Data Export**: Fetches survey responses programmatically in CSV format.
- **Robust Error Handling**: Handles token expiration, rate limits (`429 Too Many Requests`), and server errors gracefully.
- **Polling Mechanism**: Monitors the export progress until data is ready for download.
- **Logging**:
  - Cloud-based logs via **AWS CloudWatch**.
  - Local log file (`qualtrics_workflow.log`) for easy debugging.

---

## **How It Works**

### **1. Generate Access Token**
The script fetches a token dynamically using the **Client ID** and **Client Secret**:
- A POST request is sent to the Qualtrics OAuth endpoint:
  ```
  https://{data_center}.qualtrics.com/oauth2/token
  ```
- The token is valid for a limited time (e.g., 1 hour) and is used to authenticate subsequent API calls.

---

### **2. Export Survey Responses**
- A POST request is sent to the `export-responses` endpoint to initiate the export process:
  ```
  https://{data_center}.qualtrics.com/API/v3/surveys/{survey_id}/export-responses
  ```
- The server responds with a `progressId` to track the status of the export.

---

### **3. Monitor Export Progress**
- The script polls the server periodically to check the status of the export:
  - **inProgress**: Wait and retry.
  - **complete**: Retrieve the file URL.
  - **failed**: Log the error and terminate.

---

### **4. Download the Exported File**
- Once the export is complete, the script downloads the file from the provided `fileUrl` and saves it locally in CSV format.

---

## **Installation**

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/qualtrics-api-integration.git
cd qualtrics-api-integration
```

### **2. Install Dependencies**
- Install the required Python packages:
```bash
pip install -r requirements.txt
```

### **3. Configure Environment Variables**
- Set up environment variables for your **Client ID** and **Client Secret**:
```bash
export QUALTRICS_CLIENT_ID="your_client_id"
export QUALTRICS_CLIENT_SECRET="your_client_secret"
export QUALTRICS_DATA_CENTER="sjc1"  # Replace with your data center (e.g., iad1, sjc1)
```

---

## **Usage**

Run the script to export survey responses and save them locally:
```bash
python qualtrics_integration.py
```

### **Expected Output**
1. The script generates an access token and initiates the export process.
2. It logs progress in the console and writes detailed logs to:
   - **CloudWatch** (for admins).
   - **qualtrics_workflow.log** (local log file).
3. The exported CSV file is saved to the local directory.

---

## **Error Handling and Retries**

### **Implemented Scenarios**
- **Token Expiration (`401 Unauthorized`)**:
  - Automatically regenerates the token.
- **Rate Limits (`429 Too Many Requests`)**:
  - Retries with exponential backoff (e.g., 1s, 2s, 4s).
- **Server Errors (`500 Internal Server Error`)**:
  - Retries up to 3 times before failing gracefully.
- **Export Failures**:
  - Logs the failure and notifies the user.

### **Notifications**
- Add support for email or Slack notifications for critical failures (optional).

---

## **Project Structure**

```
qualtrics-api-integration/
│
├── qualtrics_api_integration.py    # Main script for Qualtrics API workflow
├── requirements.txt            # Python dependencies
├── qualtrics_workflow.log      # Local log file for end-users
└── README.md                   # Project documentation
```

---

## **Improvements for Future Releases**
1. **Real-Time Data Fetching**:
   - Use Qualtrics Webhooks for instant processing of survey responses.
2. **Data Privacy**:
   - Implement regex-based redaction for sensitive data (PII) if required.
3. **Deployment**:
   - Dockerize the script for deployment in production environments.
4. **Notifications**:
   - Add email or Slack notifications for critical events (e.g., failures).

---

## **License**
This project is licensed under the MIT License.

---

## **Contributing**
1. Fork the repository.
2. Create a new branch for your feature/bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and create a pull request.

---

## **Contact**
For questions or support, feel free to reach out:
- **Email**: rashmi.oca@gmail.com
- **GitHub**: https://github.com/RRB2507


