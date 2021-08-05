import requests
import datetime
import dateutil.relativedelta
from variables import *


# This class is responsible for talking to the Flight Search API.
class FlightSearch:

    def __init__(self):
        """Fetches the date for today and six months later"""
        self.today = datetime.date.today()
        self.six_months_later = self.today + dateutil.relativedelta.relativedelta(months=6)
        self.my_city = MY_CITY
        self.my_city_code = self.get_iata_code(self.my_city)
        self.stop_overs = 0


    def get_iata_code(self, city_name):
        """Requires a city name as argument. Returns the IATA code of the city."""
        endpoint = 'https://tequila-api.kiwi.com/locations/query'
        request_headers = {'apikey': FLIGHT_SEARCH_API_KEY}
        request_params = {'term': city_name}
        response = requests.get(endpoint, params=request_params, headers=request_headers)
        iata_code = response.json()['locations'][0]['code']
        return iata_code


    def find_cheapest_flights(self, destination):
        """Finds cheapest flights to the destination. Takes in a destination row of Google Sheet as argument.
        If flights are found, returns a string with the flight details. Else returns None."""
        endpoint = 'https://tequila-api.kiwi.com/v2/search'
        request_headers = {'apikey': FLIGHT_SEARCH_API_KEY}
        request_params = {
            'fly_from': self.my_city_code,
            'fly_to': destination['iataCode'],
            'date_from': self.today.strftime('%d/%m/%Y'),
            'dateTo': self.six_months_later.strftime('%d/%m/%Y'),
            'one_for_city': 1,
            'max_stopovers': self.stop_overs,
            'limit': 1,  # fetch only 1 result
            'curr': MY_CURRENCY,
            'sort': 'price',  # sorted by lowest price first
            'price_to': destination['highestPriceInr'],     # fetches flight details only if price is below hard limit in Google Sheet
        }
        response = requests.get(endpoint, params=request_params, headers=request_headers)
        return self.send_flight_details(response.json(), destination, 'Cheapest Flight')


    def find_earliest_cheap_flights(self, destination):
        """Finds earliest flights to the destination that are priced below hard limit in Sheets.
        Takes in a destination row of Google Sheet as argument.
        If flights are found, returns a string with the flight details. Else returns None."""
        endpoint = 'https://tequila-api.kiwi.com/v2/search'
        request_headers = {'apikey': FLIGHT_SEARCH_API_KEY}
        request_params = {
            'fly_from': self.my_city_code,
            'fly_to': destination['iataCode'],
            'date_from': self.today.strftime('%d/%m/%Y'),
            'dateTo': self.six_months_later.strftime('%d/%m/%Y'),
            'one_for_city': 1,
            'max_stopovers': self.stop_overs,
            'curr': MY_CURRENCY,
            'sort': 'date',  # sorted date wise
            'price_to': destination['highestPriceInr'],     # fetches flight details only if price is below hard limit in Google Sheet
        }
        response = requests.get(endpoint, params=request_params, headers=request_headers)
        return self.send_flight_details(response.json(), destination, 'Earliest Cheap Flight')


    def send_flight_details(self, response_json, destination, print_string):
        """Takes in response.json(), destination row and a print string as arguments.
        If flights are found, returns a string with the flight details. Else returns None."""
        try:
            item = response_json['data'][0]
        except IndexError:
            print(f'No {print_string} found for {destination["city"]} with {self.stop_overs} stop-overs.')
            return None
        else:
            price = item['price']
            travel_date = item['route'][0]['local_departure'].split('T')[0]
            origin_city = item['route'][0]['cityFrom']
            origin_airport = item['route'][0]['flyFrom']

            if self.stop_overs == 1:
                via_city = item['route'][0]['cityTo']
                via_city_airport = item['route'][0]['flyTo']
                destination_city = item['route'][1]['cityTo']
                destination_airport = item['route'][1]['flyTo']
                flight_details = f'{print_string} found: ' \
                                 f'Only INR {price} ' \
                                 f'to fly from {origin_city}-{origin_airport} ' \
                                 f'to {destination_city}-{destination_airport} ' \
                                 f'on {travel_date} ' \
                                 f'with {self.stop_overs} stop-over in {via_city}-{via_city_airport}.' \
                                 f'\nhttps://www.google.co.in/flights?hl=en#flt={origin_airport}.{destination_airport}.{travel_date}'
            else:
                destination_city = item['route'][0]['cityTo']
                destination_airport = item['route'][0]['flyTo']
                flight_details = f'Alert! {print_string} found: ' \
                                 f'Only INR {price} ' \
                                 f'to fly from {origin_city}-{origin_airport} ' \
                                 f'to {destination_city}-{destination_airport} ' \
                                 f'on {travel_date} ' \
                                 f'with {self.stop_overs} stop-overs.' \
                                 f'\nhttps://www.google.co.in/flights?hl=en#flt={origin_airport}.{destination_airport}.{travel_date}'

            return flight_details
