import requests
import json
from decouple import config


subdomain = 'vlad09vlad09'  # Subdomain of the account
link = f'https://{subdomain}.kommo.com/api/v4/leads'  # Creating URL for the request

# Getting access_token and refresh_token from your storage
ACCESS_TOKEN = config('ACCESS_TOKEN')
REFRESH_TOKEN = config('REFRESH_TOKEN')
# Creating headers
headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'User-Agent': 'Kommo-oAuth-client/1.0',
}


def add_lead(name, phone_number, job):
    try:
        response = requests.post(link, data=json.dumps([{
            "name": name,
            "pipeline_id": 7326627,
            "custom_fields_values": [
                {
                    "field_id": 116076,
                    "values": [
                        {
                            "value": phone_number
                        }
                    ]
                }, {
                    "field_id": 119498,
                    "values": [
                        {
                            "value": job
                        }
                    ]
                }
            ]
        }]), headers=headers, verify=True)

        # # Check the HTTP status code for errors
        # if response.status_code not in (200, 201):
        #     raise Exception(f'Error: {response.status_code} - {response.text}')

        # Process the response data as needed
        account_data = response.json()
        print(account_data)
    except Exception as e:
        print(f'Error: {str(e)}')

