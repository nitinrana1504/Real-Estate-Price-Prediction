from flask import Flask, request, jsonify
import util

app = Flask(__name__)

@app.route('/get_Locality_name', methods=['GET'])
def get_Locality_name():
    response = jsonify({
        'Locality': util.get_Locality_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/get_Furnishing', methods=['GET'])
def get_Furnishing():
    response = jsonify({
        'Furnishing': util.get_Furnishing()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/get_Type', methods=['GET'])
def get_Type():
    response = jsonify({
        'Type': util.get_Type()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/get_Predict_Price', methods=['POST'])
def get_Predict_Price():
    Area = float(request.form['Area'])
    Locality = request.form['Locality']
    Furnishing = request.form['Furnishing']
    Type = request.form['Type']
    BHK = int(request.form['BHK'])
    Bathroom = int(request.form['Bathroom'])
    Parking = int(request.form['Parking'])

    response = jsonify({
        'estimated_price': util.get_estimated_price(Locality, Furnishing, Type, Area, BHK, Bathroom, Parking)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run()
