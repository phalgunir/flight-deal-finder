import requests
from flight_search import FlightSearch
from variables import *


# This class is responsible for interacting with the Google Sheet using Sheety API
class DataManager:

    def __init__(self):
        """Calls get_sheet_data to fetch Google Sheet data. Updates IATA code if it is missing."""
        self.sheet_endpoint = SHEETY_ENDPOINT
        self.request_headers = {
            'Authorization': f'Basic {SHEETY_AUTHORIZATION}'
        }
        for destination in self.get_sheet_data():
            if destination['iataCode'] == '':
                self.update_iata_codes_in_sheet(destination)

        self.sheet_data = self.get_sheet_data()


    def get_sheet_data(self):
        """Fetches Google Sheet data using Sheety API."""
        get_sheet = requests.get(self.sheet_endpoint, headers=self.request_headers)
        if not get_sheet.raise_for_status():
            sheet_data = get_sheet.json()['prices']
            return sheet_data


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
        response = requests.put(f'{self.sheet_endpoint}/{destination["id"]}', json=request_params, headers=self.request_headers)
        if not response.raise_for_status():
            print(f'Updated iata for city {destination["city"]}: {iata_code}')
