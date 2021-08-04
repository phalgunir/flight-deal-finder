Use this Flight Deal Finder App to find the cheapest flight to your list of destinations, within the next 6 months.

Update the variables.py with your api keys and details.     
Update the destinations you want to visit and the highest price you are willing pay for their flights, in your Google Sheet.        
Sample Google Sheet:        
![img.png](img.png)

Link your Google Sheet to Sheety API.       
This code then uses Sheety and Flight Search API to populate your Google Sheet with International Air Transport Association (IATA) codes for each city.      
It checks for the flights with price lower than the highest price listed in the Google Sheet, from today to 6 months later, for all the cities in the sheet.  
If a flight is found, it sends an email to your ID using SMTPLib and an SMS to your number using Twilio API.
The message includes the flight price, flight date, departure city, departure airport code, arrival city and arrival airport code.      

Sample SMS:     
![img_1.png](img_1.png)     
        
Output:         
![img_2.png](img_2.png)

API's used:     
Google Sheet Data Management - https://sheety.co/   
Tequila Flight Search API Documentation - https://tequila.kiwi.com/portal/docs/tequila_api      
Twilio SMS API - https://www.twilio.com/docs/sms        

