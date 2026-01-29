import os
from flask import Flask, render_template, request
import requests
from wand.image import Image
from wand.color import Color

app = Flask(__name__)

def procesar_fondo():
    input_path = 'static/sol.jpeg'
    output_path = 'static/bg_procesado.jpg'

    if not os.path.exists(input_path):
        print("❌ No existe static/bg_original.jpg")
        return

    with Image(filename=input_path) as img:
        img.resize(1920, 1080)

        overlay = Image(
            width=img.width,
            height=img.height,
            background=Color('rgba(0,0,0,0.4)')
        )

        img.composite(overlay, 0, 0)
        img.save(filename=output_path)

        print("✅ Fondo generado correctamente")

# API Key
API_KEY = os.getenv('OPENWEATHER_API_KEY', 'tu_api_key_aqui')

def get_weather(city):
    if not API_KEY or API_KEY == 'tu_api_key_aqui':
        return {'error': 'Configura tu API Key en OPENWEATHER_API_KEY'}

    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'es'
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get('cod') == 200:
        return {
            'ciudad': data['name'],
            'pais': data['sys']['country'],
            'temperatura': round(data['main']['temp'], 1),
            'descripcion': data['weather'][0]['description'].capitalize()
        }

    return {'error': data.get('message', 'Ciudad no encontrada')}

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    error = ""

    if request.method == 'POST':
        city = request.form.get('city', '').strip()
        if city:
            result = get_weather(city)
            if 'error' in result:
                error = result['error']
            else:
                weather = result

    return render_template('index.html', weather=weather, error=error)

if __name__ == '__main__':
    procesar_fondo()
    app.run(debug=True)

