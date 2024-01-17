
Historic Weather Data

Building an API's that takes in a Location (Latitude & Longitude) and Number of Days as
Input, and returns back Historic Weather Data (Hourly Temperature, Precipitation and Cloud
Cover) for those number of days in the Past.


From https://open-meteo.com/

Prerequisites
Before you begin, ensure you have met the following requirements:

Python (version 3.6 or higher)

Django (version 4.2.9)

Other project dependencies (install using pip install -r requirements.txt)

## Documentation

Register a new user by making a POST request to /api/register/.

Login with the registered user credentials by making a POST request to /api/login/.

Obtain historical weather data by making a GET request to /api/historical-data/

To get the Historical weather data from https://open-meteo.com/ user must have register and login into the application and pass Token in Headers to access secure end-points

If token is not mention in Headers it will return an following error

 {
    "detail": "Authentication credentials were not provided."
}

Custome Expiring Token Authentication is created in Authentication.py file.

Note:-Token will expire after certain seconds,Mention in settings.py file
TOKEN_EXPIRED_AFTER_SECONDS = 86400


Import the Postman collection named---> Map_my_crop.postman_collection


end-point :- http://127.0.0.1:8000/api/historical-data

params = {
    "latitude": 52.52,
    "longitude": 13.41,
    "hourly": [
        "temperature_2m",
        "precipitation",
        "cloud_cover"
    ],
    "past_days": 2
}


Encountering challenges To get Historical weather data using TestCases

## 🚀 About Me
I'm a Python-Django Developer.
Have good hands on Django and Django Rest Framework along with Automating Daily repetative task using libraries like Selenium,request,Scrapy.

Familer with

Python

Django

Machine Learning

SQL

Git

Jira