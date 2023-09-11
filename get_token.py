import requests
import json
from decouple import config

subdomain = 'vlad09vlad09'  # Subdomain of the account
link = f'https://{subdomain}.kommo.com/oauth2/access_token'  # Creating URL for the request

CLIENT_ID = config('CLIENT_ID')
CLIENT_SECRET = config('CLIENT_SECRET')
GRANT_TYPE = config('GRANT_TYPE')
REFRESH_TOKEN = config('REFRESH_TOKEN')
REDIRECT_URI = config('REDIRECT_URI')


# Gathering data for the request
data = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'grant_type': GRANT_TYPE,
    'refresh_token': REFRESH_TOKEN,
    'redirect_uri': REDIRECT_URI
}

# Setting up the request headers
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Kommo-oAuth-client/1.0',
}


def get_token():
    try:
        response = requests.post(link, data=json.dumps(data), headers=headers, verify=True)

        # Check the HTTP status code for errors
        if response.status_code not in (200, 201):
            raise Exception(f'Error: {response.status_code} - {response.text}')

        # Parse the JSON response
        response_data = response.json()

        # Extract relevant data
        access_token = response_data.get('access_token')
        refresh_token = response_data.get('refresh_token')
        token_type = response_data.get('token_type')
        expires_in = response_data.get('expires_in')

        # Use the extracted data as needed
        print(f'Access Token: {access_token}')
        print(f'Refresh Token: {refresh_token}')
        print(f'Token Type: {token_type}')
        print(f'Expires In: {expires_in} seconds')
        return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': token_type, 'expires_in': expires_in}
    except Exception as e:
        print(f'Error: {str(e)}')