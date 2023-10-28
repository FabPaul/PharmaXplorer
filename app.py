#!/usr/bin/python3
""" App module for PharmaXplorer website"""

import json
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)


# Load the pharmacies from the JSON file
with open("pharmacies.json", "r") as f:
    pharmacies_data = json.load(f)


# Define the routes for the application
@app.route("/")
def index():
    current_time = datetime.now().strftime("%H:%M:%S")
    return render_template("index.html", current_time=current_time)


@app.route("/pharmacies")
def display_pharmacies():
    return render_template("pharmacies.html",
                           pharmacies=pharmacies_data["pharmacies"])


@app.route("/pharmacy_details/<int:pharmacy_id>")
def pharmacy_details(pharmacy_id):
    pharmacy = pharmacies_data["pharmacies"][pharmacy_id - 1]
    return render_template("pharmacy.html", pharmacy=pharmacy,
                           pharmacy_id=pharmacy_id)


@app.route("/medications/<int:pharmacy_id>")
def medications(pharmacy_id):
    pharmacy = pharmacies_data["pharmacies"][pharmacy_id - 1]
    return render_template("medications.html", pharmacy=pharmacy,
                           pharmacy_id=pharmacy_id)


@app.route("/location/<int:pharmacy_id>")
def location(pharmacy_id):
    pharmacy = pharmacies_data["pharmacies"][pharmacy_id - 1]
    return render_template("location.html", pharmacy=pharmacy,
                           pharmacy_id=pharmacy_id)


@app.route("/contact/<int:pharmacy_id>")
def contact(pharmacy_id):
    pharmacy = pharmacies_data["pharmacies"][pharmacy_id - 1]
    return render_template("contact.html", pharmacy=pharmacy,
                           pharmacy_id=pharmacy_id)


@app.route("/on_call")
def on_call():
    current_day = datetime.now().strftime('%A')
    pharmacies_on_call = []
    for pharmacy in pharmacies_data["pharmacies"]:
        if current_day in pharmacy["on_call_days"]:
            pharmacies_on_call.append(pharmacy)
    return render_template("on_call.html",
                           pharmacies_on_call=pharmacies_on_call,
                           current_day=current_day)


@app.route("/search", methods=["GET"])
def search_medications():
    query = request.args.get("query")
    search_results = []
    if query:
        for pharmacy in pharmacies_data["pharmacies"]:
            for medication in pharmacy["medications"]:
                if query.lower() in medication["name"].lower():
                    search_results.append({"pharmacy": pharmacy["name"],
                                           "medication": medication})
    return render_template("search.html", query_results=search_results)


# Start the Flask app
if __name__ == "__main__":
    app.run(debug=True)
