from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager


flight_search = FlightSearch()
data_manager = DataManager()
notification_manager = NotificationManager()


# find the cheapest flights in the next 6 months and notify
for destination in data_manager.price_sheet_data:
    # start by checking flights with 0 stop-overs
    flight_search.stop_overs = 0
    cheapest_flight_details = flight_search.find_cheapest_flights(destination)

    if cheapest_flight_details is None:
        # check flights with 1 stop-over
        flight_search.stop_overs = 1
        cheapest_flight_details = flight_search.find_cheapest_flights(destination)
        if cheapest_flight_details is not None:
            print(cheapest_flight_details)
            notification_manager.send_sms(sms_text=cheapest_flight_details)
            notification_manager.send_email(email_text=cheapest_flight_details, to_email_list=data_manager.to_email_list)
    else:
        print(cheapest_flight_details)
        notification_manager.send_sms(sms_text=cheapest_flight_details)
        notification_manager.send_email(email_text=cheapest_flight_details, to_email_list=data_manager.to_email_list)


print('\n\n')


# find the earliest cheap flights and notify
for destination in data_manager.price_sheet_data:
    # start by checking flights with 0 stop-overs
    flight_search.stop_overs = 0
    earliest_cheap_flight_details = flight_search.find_earliest_cheap_flights(destination)

    if earliest_cheap_flight_details is None:
        # check flights with 1 stop-over
        flight_search.stop_overs = 1
        earliest_cheap_flight_details = flight_search.find_earliest_cheap_flights(destination)
        if earliest_cheap_flight_details is not None:
            print(earliest_cheap_flight_details)
            notification_manager.send_sms(sms_text=earliest_cheap_flight_details)
            notification_manager.send_email(email_text=earliest_cheap_flight_details, to_email_list=data_manager.to_email_list)
    else:
        print(earliest_cheap_flight_details)
        notification_manager.send_sms(sms_text=earliest_cheap_flight_details)
        notification_manager.send_email(email_text=earliest_cheap_flight_details, to_email_list=data_manager.to_email_list)
