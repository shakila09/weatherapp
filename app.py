from flask import Flask, render_template, request, jsonify
import requests
import os  # for accessing environment variables

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("index.html")

@app.route("/weatherapp", methods=["POST", "GET"])
def get_weatherdata():
    try:
        # Validate form data
        city = request.form.get("city")
        appid = request.form.get('appid')
        units = request.form.get('units')

        if not city or not appid or not units:
            return jsonify(error="Missing required data"), 400

        # Make API request
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city,
            'appid': appid,
            'units': units
        }
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse JSON response
        data = response.json()

        # Check for errors in the API response
        if 'name' not in data:
            return jsonify(error="Invalid response from OpenWeatherMap API"), 500

        # Return JSON response using Flask's jsonify
        return jsonify(data=data, city=data['name'])

    except requests.RequestException as e:
        return jsonify(error=f"Error connecting to OpenWeatherMap API: {str(e)}"), 500

if __name__ == '__main__':
    # Use environment variables for sensitive information
    app.run(host="0.0.0.0", port=5000)
