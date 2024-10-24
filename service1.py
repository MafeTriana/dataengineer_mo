from flask import Flask, request, jsonify
import sqlite3
import csv
import io

app = Flask(__name__)

def connect_db():
    return sqlite3.connect('coordinates.db')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Conexión a la base de datos
        conn = connect_db()
        cursor = conn.cursor()

        # Eliminar tabla 'coordinates' si ya existe (para evitar problemas de esquema)
        cursor.execute("DROP TABLE IF EXISTS coordinates")

        # Crear la tabla nuevamente con las columnas correctas
        cursor.execute('''CREATE TABLE IF NOT EXISTS coordinates 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                          lat REAL, 
                          lon REAL)''')

        # Leer el archivo CSV
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.DictReader(stream, delimiter='|')  # Leer usando '|' como delimitador

        # Insertar datos en la base de datos
        for row in csv_reader:
            lat = row['lat'].replace("''", "").replace(",", ".").strip()  # Limpiar comillas y cambiar coma por punto
            lon = row['lon'].replace("''", "").replace(",", ".").strip()

            if lat.lower() == 'nan' or lon.lower() == 'nan':
                continue  # Saltar filas con NaN

            cursor.execute("INSERT INTO coordinates (lat, lon) VALUES (?, ?)",
                           (float(lat), float(lon)))

        conn.commit()
        conn.close()

        return jsonify({'message': 'File successfully uploaded and data inserted'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
