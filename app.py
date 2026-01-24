import os
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# API Key
API_KEY = os.getenv('OPENWEATHER_API_KEY', 'tu_api_key_aqui')

def get_weather(city):
    """Obtiene el clima de una ciudad"""
    if not API_KEY or API_KEY == 'tu_api_key_aqui':
        return {'error': 'Configura tu API Key en OPENWEATHER_API_KEY'}
    
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric',
            'lang': 'es'
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get('cod') == 200:
            return {
                'ciudad': data['name'],
                'pais': data['sys']['country'],
                'temperatura': round(data['main']['temp'], 1),
                'sensacion': round(data['main']['feels_like'], 1),
                'minima': round(data['main']['temp_min'], 1),
                'maxima': round(data['main']['temp_max'], 1),
                'humedad': data['main']['humidity'],
                'viento': data['wind']['speed'],
                'descripcion': data['weather'][0]['description'].capitalize(),
                'icono': data['weather'][0]['icon']
            }
        else:
            return {'error': data.get('message', 'Ciudad no encontrada')}
            
    except requests.exceptions.Timeout:
        return {'error': 'Tiempo de espera agotado'}
    except requests.exceptions.ConnectionError:
        return {'error': 'Error de conexión'}
    except Exception as e:
        return {'error': f'Error: {str(e)}'}

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    city = ""
    error = ""
    
    if request.method == 'POST':
        city = request.form.get('city', '').strip()
        if city:
            result = get_weather(city)
            if 'error' in result:
                error = result['error']
            else:
                weather = result
    
    return render_template('index.html', 
                         weather=weather, 
                         city=city, 
                         error=error,
                         api_key=API_KEY)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)