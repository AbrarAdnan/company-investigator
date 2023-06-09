Company Investigator


This is a Python program designed to investigate company information. The program requires Python 3.8 or later, and has been tested on Python 3.9.0.

Installation

To install Company Investigator, clone this repository using the following command:
```
git clone https://github.com/AbrarAdnan/company-investigator.git
```
Change directory to the downloaded folder
```
cd company-investigator
```
After cloning the repository, create a virtual environment for the program by running the following command:
```
virtualenv venv
```
Activate the virtual environment using the following command (on windows):

```
venv/scripts/activate
```

Finally, install the required dependencies using the following command:
```
pip install -r requirements.txt
```
Usage

To run Company Investigator, activate your virtual environment and navigate to the cloned repository directory. Run the program using the following command:
``
python app.py
``
When the server is running you can try it out on your browser by visiting this link http://127.0.0.1:5000/ 

Or you can send a json payload through GET method to http://127.0.0.1:5000/ 
in this exaple format
```
{
  "company_name": "Microsoft",
  "country": "Uniter States of America",
  "company_website": "www.microsoft.com"
}
```
and you'll get the output with the description on company product/services, keywords related to company, naics code and sic code
the example output of the api response will be
```
{
    "keyword": [
        "Microsoft",
        "Windows"
    ],
    "naics": [
        561990
    ],
    "product_services": [
        "Windows",
        "Microsoft Office"
    ],
    "sic": [
        7389
    ]
}
```
