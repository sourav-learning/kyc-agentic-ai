# kyc-agentic-ai



python -m venv .env

.env\Scripts\activate
pip install -r requirements.txt

NOTE : PyMuPDF is trying to build from source and requires Visual Studio, which is not found on your system. This is a common issue with Python 3.13, as many packages do not yet provide pre-built wheels for this version.

# Pre Work
1. Create a folder named .streamlit under the project folder
2. Within it create file named secrets.toml for storing all API keys and other passwords
3. Make sure to have .gitignore created and add relevant folders and files particularly the secrets.toml so that your keys and passwords do not get exposed.

## Step1 : 
Download and install python 3.11.0 from python website
## Step2 : 
Run the following command to create .env. If you have already created .env using other version, delete the folder and then run the command
py -3.11 -m venv .env
## Step3 : Activate the virtual environment
.\.env\Scripts\Activate.ps1
## Step4 : Install dependency from requirements file
pip install -r requirements.txt
## Step5 : Run the following command to simulate a local mail server. (optional)
python -m aiosmtpd -n -l localhost:1025
## Step 6 : Open a new terminal, active env as before and then run the following command to open streamlit screen
streamlit run main.py

## TroubleShooting
* If the __init__.py file was missing before, Python would not recognize agents as a package, causing the import to fail.

> Create an empty file __init__.py

* If you see the error TypeError: Client.__init__() got an unexpected keyword argument 'proxies' occurs when the OpenAI() client is being initialized, and the underlying OpenAI Python library is passing a proxies argument to a class that does not accept it.

> pip install --upgrade openai httpx

# Starting the API locally
Open a new terminal and run
python account_api.py

# Deploying the API
1. Hosting the API
Streamlit Cloud does not support running background services like Flask APIs.
Your account_api.py must be hosted separately (e.g., on a cloud VM, Heroku, Render, AWS, Azure, etc.).
The API endpoint in your app must use a public URL, not localhost.
2. Update API Endpoint in account_creation_agent.py
Change the API host and port to point to your deployed API (e.g., https://your-api-service.com).
You can use environment variables or Streamlit secrets for the API URL.
3. Add API URL to Streamlit Secrets
4. CORS Support
Ensure your Flask API allows CORS (Cross-Origin Resource Sharing) so Streamlit Cloud can access it.
Add this to your Flask app:
    from flask_cors import CORS
    CORS(app)
5. Secure Your API
Use authentication or API keys if your API handles sensitive data.
6. Remove/Handle Localhost References
Any reference to localhost in your code must be replaced with the public API URL.
