from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("index.html")

@app.route("/weatherapp", methods=["POST", "GET"])
def get_weatherdata():
    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        'q': request.form.get("city"),
        'appid': request.form.get('appid'),
        'units': request.form.get('units')
    }
    response = requests.get(url, params=params)
    data = response.json()

    # Returning JSON response using Flask's jsonify
    return jsonify(data=data, city=data['name'])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
