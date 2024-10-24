from flask import Flask, jsonify
import requests
import sqlite3

app = Flask(__name__)

def connect_db():
    return sqlite3.connect('coordinates.db')

@app.route('/process', methods=['GET'])
def process_coordinates():
    conn = connect_db()
    cursor = conn.cursor()

    # Obtener las coordenadas de la base de datos
    cursor.execute("SELECT lat, lon FROM coordinates")
    rows = cursor.fetchall()
    results = []

    for lat, lon in rows:
        if lat is None or lon is None:
            results.append({'lat': lat, 'lon': lon, 'error': "Invalid coordinates"})
            continue

        try:
            # Hacer la solicitud a la API con lat y lon
            response = requests.get(f"https://api.postcodes.io/postcodes?lat={lat}&lon={lon}")
            if response.status_code == 200:
                data = response.json()
                if data['result']:
                    postcode = data['result'][0]['postcode']
                    results.append({'lat': lat, 'lon': lon, 'postcode': postcode})
                else:
                    results.append({'lat': lat, 'lon': lon, 'error': "No postcode found"})
            else:
                results.append({'lat': lat, 'lon': lon, 'error': "API request failed"})

        except Exception as e:
            results.append({'lat': lat, 'lon': lon, 'error': str(e)})

    conn.close()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
