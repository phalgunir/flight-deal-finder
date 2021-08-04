from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager


flight_search = FlightSearch()
data_manager = DataManager()
notification_manager = NotificationManager()

# for each destination row in Google Sheet
for destination in data_manager.sheet_data:

    # find the cheapest flight in the next 6 months to the destination. send notification.
    cheapest_flight_details = flight_search.find_cheapest_flights(destination)
    if cheapest_flight_details is not None:
        print(cheapest_flight_details)
        notification_manager.send_sms(sms_text=cheapest_flight_details)
        notification_manager.send_email(email_text=cheapest_flight_details)

    # find the earliest cheap flight with price below the google sheet price. send notification.
    earliest_cheap_flight_details = flight_search.find_earliest_cheap_flights(destination)
    if earliest_cheap_flight_details is not None:
        print(earliest_cheap_flight_details)
        notification_manager.send_sms(sms_text=earliest_cheap_flight_details)
        notification_manager.send_email(email_text=earliest_cheap_flight_details)
