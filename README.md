# Flask API with Logging and Load Testing
This is a simple RESTful API built with Flask to simulate a small tech business. The API supports basic operations like retrieving general information, listing available products, and adding new ones. It also includes built-in logging and a PowerShell script to test endpoints using [Fortio](https://github.com/fortio/fortio).


## Features
- **Flask API** with structured routes for info, products, and contact.
- **Logging**: All requests are logged to a `.txt` file using Python's `logging` module.
- **UUID-based request IDs** to track each individual request.
- **Load testing (still developing)**: Automated PowerShell script using `fortio` to test API endpoints (GET and POST).


## Project Structure
FlaskAPI\
&emsp;├── app.py            # Main Flask application \
&emsp;├── api_log.txt       # Automatically created log file for all requests \
&emsp;├── fortio_test.ps1   # PowerShell script for testing the API with Fortio \
&emsp;└── README.md         # This documentation file

## Endpoints
### Root
Returns a health check response to verify the API is running.

### Business Info
Returns a simple description of the business.

### Product Listing & Adding
- Returns a list of available tech products.
- Adds a new product to the list if it doesn't already exist.

- If the field is missing or the product already exists, the API returns an error message.

### Contact Info
Returns business contact details including phone number and email.


## Logging
All request details including endpoint, method, date, status code, and a unique request ID are logged to `api_log.txt` in the following format:


## Load Testing with Fortio
### Prerequisites:
- [Download Fortio (Windows)](https://github.com/fortio/fortio/releases/download/v1.69.1/fortio_win_1.69.1.zip)
- Place the `fortio.exe` in the same directory or adjust the `$fortioPath` variable in the script.

### Running the script:
1. Ensure the Flask API is running on `http://127.0.0.1:5000`.
2. Open PowerShell and execute:

```powershell
.\fortio_test.ps1
```
