import requests
from flask import Flask, jsonify, redirect, url_for
from datetime import datetime
from base.Settings import url_base

app = Flask(__name__)

@app.route('/')
def redirect_to_pemilu():
    # redirect to 
    return redirect(url_for('pemilu'))
    

@app.route('/pemilu2024')
def pemilu():
    # Fetch data from the first URL
    response1 = requests.get(f"{url_base}pemilu/hhcw/ppwp.json")
    data1 = response1.json()

    # Fetch data from the second URL
    response2 = requests.get(f"{url_base}pemilu/ppwp.json")
    data2 = response2.json()

    total_votes = sum(data1['chart'][key] for key in data1['chart'] if key != 'persen')

    # Combine the data from both URLs into a single dictionary
    combined_data = {}

    for key, value in data2.items():
        percent = data1['chart'][key] / total_votes * 100
        combined_data[key] = {
            # "ts": FormattedDate(data1["ts"]).get_formatted_date(),
            "id": f"{value["nomor_urut"]:02d}",
            "name_capres": value["nama"].split(" - ")[0],
            "name_cawapres": value["nama"].split(" - ")[1],
            "votes": f"{data1["chart"][key]:,} of {total_votes:,}",
            "percent_votes": f"{percent:.4f}%",
        }

    persen_votes = data1["progres"]["progres"] / data1["progres"]["total"] * 100
    # Add progress data
    combined_data["statistics"] = {
        "progres_tps": f"{data1["progres"]["progres"]:,}",
        "total_tps": f"{data1["progres"]["total"]:,}",
        "join_tps": f"{data1["progres"]["progres"]:,} of {data1["progres"]["total"]:,} TPS",
        "percent_tps": f"{persen_votes:.4f}% Done",
        "last_update": FormattedDate(data1["ts"]).get_formatted_date(),
        "total_votes": f"{total_votes:,}"
    }

    # Return the combined JSON as a response
    return jsonify(combined_data)

class FormattedDate:
    def __init__(self, date_string):
        self.date_string = date_string

    def get_formatted_date(self):
        try:
            date_object = datetime.strptime(self.date_string, "%Y-%m-%d %H:%M:%S")
            formatted_date = date_object.strftime("%d %B %Y %H:%M:%S WIB")
            return formatted_date
        except ValueError:
            return "Invalid date format"

if __name__ == '__main__':
    app.run()
