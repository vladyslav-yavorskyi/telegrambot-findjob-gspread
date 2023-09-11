import re


def validate_phone_number(phone_number):
    # Define the regex pattern for valid phone numbers
    pattern = r'^(?:\+48|48|\+380|380)\d{8,10}$'

    # Use re.match() to check if the phone_number matches the pattern
    if re.match(pattern, phone_number):
        return True
    else:
        return False
