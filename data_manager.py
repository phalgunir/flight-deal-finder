import requests
from flight_search import FlightSearch
from variables import *


# This class is responsible for interacting with the Google Sheet using Sheety API
class DataManager:

    def __init__(self):
        """Fetches all Google Sheet data. Updates IATA code if it is missing."""
        self.request_headers = {
            'Authorization': f'Basic {SHEETY_AUTHORIZATION}'
        }

        for destination in self.get_price_sheet_data():
            if destination['iataCode'] == '':
                self.update_iata_codes_in_sheet(destination)

        self.price_sheet_data = self.get_price_sheet_data()
        self.user_sheet_data = self.get_user_sheet_data()
        self.to_email_list = self.get_emails_in_user_sheet()


    def get_price_sheet_data(self):
        """Returns the 'prices' google sheet data using Sheety API."""
        get_sheet = requests.get(f'{SHEETY_ENDPOINT}/prices', headers=self.request_headers)
        if not get_sheet.raise_for_status():
            sheet_data = get_sheet.json()['prices']
            return sheet_data
        return MY_SHEET_PRICES_DATA


    def get_user_sheet_data(self):
        """Returns the 'users' google sheet data using Sheety API."""
        get_sheet = requests.get(f'{SHEETY_ENDPOINT}/users', headers=self.request_headers)
        if not get_sheet.raise_for_status():
            sheet_data = get_sheet.json()['users']
            return sheet_data
        return MY_SHEET_USERS_DATA


    def get_emails_in_user_sheet(self):
        """Returns the list of emails in the 'users' sheet"""
        to_emails = [user['email'] for user in self.user_sheet_data]
        return to_emails


    def update_iata_codes_in_sheet(self, destination):
        """Requires a destination row from Google Sheets as argument.
        Calls the get_iata_code method from FlightSearch and updates the Google Sheet with IATA Codes of cities."""
        flight_search_object = FlightSearch()
        iata_code = flight_search_object.get_iata_code(city_name=destination['city'])
        request_params = {
            'price': {
                'iataCode': iata_code,
            }
        }
        response = requests.put(f'{SHEETY_ENDPOINT}/{destination["id"]}', json=request_params, headers=self.request_headers)
        if not response.raise_for_status():
            print(f'Updated iata for city {destination["city"]}: {iata_code}')
