# kyc-agentic-ai



python -m venv .env

.env\Scripts\activate
pip install -r requirements.txt

NOTE : PyMuPDF is trying to build from source and requires Visual Studio, which is not found on your system. This is a common issue with Python 3.13, as many packages do not yet provide pre-built wheels for this version.

Step1 : Download and install python 3.11.0 from python website
Step2 : Run the following command to create .env. If you have already created .env using other version, delete the folder and then run the command
py -3.11 -m venv .env
Step3 : Activate the virtual environment
.\.env\Scripts\Activate.ps1
Step4 : Install dependency from requirements file
pip install -r requirements.txt
Step5 : Run the following command to simulate a local mail server. (optional)
python -m aiosmtpd -n -l localhost:1025
Step 6 : Open a new terminal, active env as before and then run the following command to open streamlit screen
streamlit run main.py

## TroubleShooting
* If the __init__.py file was missing before, Python would not recognize agents as a package, causing the import to fail.

> Create an empty file __init__.py

* If you see the error TypeError: Client.__init__() got an unexpected keyword argument 'proxies' occurs when the OpenAI() client is being initialized, and the underlying OpenAI Python library is passing a proxies argument to a class that does not accept it.

> pip install --upgrade openai httpx




