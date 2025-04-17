from flask import Flask, jsonify, request
from gunicorn.app.wsgiapp import run
from gunicorn.app.base import Application
from gunicorn import util
from fcntl import flock, LOCK_EX, LOCK_UN

app = Flask(__name__)
farmers = [
    {"id": 1, "name": "kartik", "crop": "rice", "location": "haryana"},
    {"id": 2, "name": "raghav", "crop": "corn", "location": "merut"}
]

# Route to handle GET request to fetch all farmer
@app.route('/farmers', methods=['GET'])
def get_farmers():
    return jsonify(farmers)

# Route to handle POST request to add a new farmer
@app.route('/farmers', methods=['POST'])
def add_farmer():
    new_farmer = request.get_json()  # Get the incoming JSON data
    farmers.append(new_farmer)  # Add new farmer to the list
    return jsonify(new_farmer), 201  # Return the newly added farmer

# Route to handle PUT request to update an existing farmer by ID
@app.route('/farmers/<int:id>', methods=['PUT'])
def update_farmer(id):
    farmer = next((f for f in farmers if f["id"] == id), None)
    if farmer:
        data = request.get_json()
        farmer.update(data)  # Update the farmer with the new data
        return jsonify(farmer)
    else:
        return jsonify({"error": "Farmer not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)