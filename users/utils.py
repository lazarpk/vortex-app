import requests
from django.conf import settings
# import clearbit

def validate_email(email):
    res = requests.get(f'https://api.hunter.io/v2/email-verifier?email={email}&api_key={settings.HUNTER_API_KEY}')

    res_json = res.json()
    
    if res.status_code != 200 or res_json['data']['status'] != 'valid' or res_json['data']['result'] != 'deliverable':
        return False
    
    return True

def clearbit_additional(email):
    # clearbit.key = settings.CLEARBIT_API_KEY
    # response = clearbit.Enrichment.find(email=email, stream=True)
    response = None
    if response is not None:
        return response
    else:
        return f"{email} doesn't have additional information."