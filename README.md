# Description

A script that would take in a CSV. The CSV contains information on the content providers and many impressions they've delivered, eCPM,
gross revenue and net revenue. The script will take that information and create individual CSVs and Excel documents for each content provider
group. These documents will contain the revenue split between VM and the content provider groups.

## Development Setup & Running Application

1. Setup a virtual enviroment with `python3 -m venv env`
2. Activate the virtual enviroment with `source ./env/bin/activate`
3. Install all the libraries within requirements.txt `pip install -r requirements.txt`
4. Run the application - `python3 app.py {PATH TO FILE}`

