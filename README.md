# Description

A script that would take in a CSV. The CSV contains information on the content providers and many impressions they've delivered, eCPM,
gross revenue and net revenue. The script will take that information and create individual CSVs and Excel documents for each content provider
group. These documents will contain the revenue split between VM and the content provider groups.

## Actions

1. A Excel template is supplied with row formatting the script can read (screenshot below). Fill in the data, save as CSV. This file when running the application.
<img width="954" alt="Screenshot 2022-02-18 at 09 20 09" src="https://user-images.githubusercontent.com/4954209/154654507-72e7fc00-678b-4b59-84cd-af1220744c25.png">
2. Two groups of files are returned (CSV and formatted Excel documents).


## Development Setup & Running Application

1. Setup a virtual enviroment with `python3 -m venv env`
2. Activate the virtual enviroment with `source ./env/bin/activate`
3. Install all the libraries within requirements.txt `pip install -r requirements.txt`
4. Run the application - `python3 app.py {PATH TO FILE}`

