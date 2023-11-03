import csv
import os
import requests
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

app.static_folder = 'static'

# OpenWeatherMap API Key
API_KEY = '0a84c32ffb40e99cf8e9908652c005a0'

# Read itinerary data from CSV file
def read_itinerary_from_csv():
    itinerary = []
    csv_file_path = os.path.join('data', 'itinerary.csv')
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            itinerary.append(row)
    return itinerary

itinerary_data = read_itinerary_from_csv()

# Function to get weather data for a specific location
def get_weather(latitude, longitude):
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=metric&appid={API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html', locations=itinerary_data, enumerate=enumerate)

# Route for handling form submissions
@app.route('/weather', methods=['POST'])
def weather():
    location_index = int(request.form['location'])
    latitude = itinerary_data[location_index]['Latitude']
    longitude = itinerary_data[location_index]['Longitude']
    weather_data = get_weather(latitude, longitude)

    if weather_data['cod'] == 200:
        # Process weather_data and display it
        return render_template('weather.html', location=itinerary_data[location_index]['Location'], weather=weather_data)
    else:
        error_message = weather_data['message']
        return render_template('error.html', error_message=error_message)

# Route for the map page
@app.route('/map')
def map():
    return render_template('map.html', locations=itinerary_data)

# Route for the user preferences page
@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    if request.method == 'POST':
        # Handles form submission for saving user preferences
        # Retrieve form data using request.form dictionary
        temperature_unit = request.form['temperature_unit']
        notification_enabled = request.form.get('notification_enabled')
        # Process the form data (e.g., saving it to a database)
        # ...
        # Redirect to a success page or the preferences page itself
        return redirect('/preferences')
    else:
        # Handles GET request to display the user preferences form
        return render_template('preferences.html')

if __name__ == '__main__':
    app.run(debug=True)




