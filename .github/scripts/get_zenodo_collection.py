import requests
import os
import re

ZENODO_SANDBOX = os.environ['ZENODO_SANDBOX']
DOI = os.environ['DOI']
ZENODO_URL = 'https://zenodo.org/api'

if ZENODO_SANDBOX.lower() == 'true':
    ZENODO_URL = 'https://sandbox.zenodo.org/api'

def parse_doi(doi: str):
    pattern = r'zenodo\.(\d+)'
    match = re.search(pattern, doi)
    if match:
        identifier = match.group(1)
        return identifier
    raise Exception('Invalid DOI.')

def get_zenodo_record(identifier: str):
    try:
        response = requests.get(f'{ZENODO_URL}/records/{identifier}')
        response.raise_for_status()
        collection = response.json().get('conceptrecid')
        if response.status_code == 200 and collection is not None:
            return collection
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return ''
    
try:
    identifier = parse_doi(DOI)
    print(get_zenodo_record(identifier))
except Exception as e:
    print(f"An unexpected error occurred: {e}")
