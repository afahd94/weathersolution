import csv
import os
import requests
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

app.static_folder = 'static'

# OpenWeatherMap API Key
API_KEY = '0a84c32ffb40e99cf8e9908652c005a0'

# Dummy user data (for project purposes)
USER_DATA = {
    'anthony_fahd': 'password1'
}

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

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USER_DATA and USER_DATA[username] == password:
            # Successful login, redirect to the home page
            return redirect('/')
        else:
            # Invalid credentials, display an error message
            return render_template('login.html', error='Invalid username or password')
    else:
        # Display the login form for GET requests
        return render_template('login.html')

# Route for the user preferences page
@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    if request.method == 'POST':
        # Handle form submission for saving preferences
        # For example, save the form data to a database
        # After processing the form data, redirect to the save_preferences route
        return redirect('/save_preferences')
    else:
        # Display the preferences form for GET requests
        return render_template('preferences.html')

# Route for the save preferences page
@app.route('/save_preferences', methods=['GET', 'POST'])
def save_preferences():
    if request.method == 'POST':
        # Handle form submission for saving preferences
        # After processing the form data, redirect to the preferences route
        return redirect('/preferences')
    else:
        # Display the save_preferences form for GET requests
        return render_template('save_preferences.html')

if __name__ == '__main__':
    app.run(debug=True)







