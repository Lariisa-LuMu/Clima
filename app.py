import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# API Key - configurar en docker-compose o .env
API_KEY = os.getenv('OPENWEATHER_API_KEY', '')

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    city = ""
    error = ""
    
    if request.method == 'POST':
        city = request.form.get('city', '').strip()
        
        if city:
            if not API_KEY:
                error = "ERROR: Configurar OPENWEATHER_API_KEY"
            else:
                # Llamar a la API
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=es"
                
                try:
                    response = requests.get(url)
                    data = response.json()
                    
                    if data.get('cod') == 200:
                        weather = {
                            'ciudad': data['name'],
                            'pais': data['sys']['country'],
                            'temperatura': data['main']['temp'],
                            'sensacion': data['main']['feels_like'],
                            'minima': data['main']['temp_min'],
                            'maxima': data['main']['temp_max'],
                            'humedad': data['main']['humidity'],
                            'viento': data['wind']['speed'],
                            'descripcion': data['weather'][0]['description'],
                            'icono': data['weather'][0]['icon']
                        }
                    else:
                        error = f"Error: {data.get('message', 'Ciudad no encontrada')}"
                        
                except Exception as e:
                    error = f"Error de conexión: {str(e)}"
    
    return render_template('index.html', 
                         weather=weather, 
                         city=city, 
                         error=error,
                         api_key_set=bool(API_KEY))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
