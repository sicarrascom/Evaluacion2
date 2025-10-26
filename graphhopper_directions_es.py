import requests
import urllib.parse

API_KEY = "6ccd5e31-6412-4801-a449-446633bcba43"

def geocodificar(ubicacion):
    while ubicacion == "":
        ubicacion = input("Por favor, ingrese una ubicación válida: ")

    url = "https://graphhopper.com/api/1/geocode?" + urllib.parse.urlencode({
        "q": ubicacion,
        "limit": 1,
        "key": API_KEY
    })

    respuesta = requests.get(url)
    datos = respuesta.json()
    estado = respuesta.status_code

    if estado == 200 and datos["hits"]:
        punto = datos["hits"][0]["point"]
        nombre = datos["hits"][0]["name"]
        pais = datos["hits"][0].get("country", "")
        estado_region = datos["hits"][0].get("state", "")
        tipo = datos["hits"][0].get("osm_value", "")
        ubicacion_completa = f"{nombre}, {estado_region}, {pais}"
        print(f"URL de geocodificación para {ubicacion_completa} (Tipo: {tipo}):\n{url}")
        return estado, punto["lat"], punto["lng"], ubicacion_completa
    else:
        print(f"Error {estado}: {datos.get('message', 'No se pudo obtener la ubicación.')}")
        return estado, None, None, ubicacion

def obtener_ruta(lat1, lng1, lat2, lng2, vehiculo):
    url = (
        "https://graphhopper.com/api/1/route?"
        f"point={lat1},{lng1}&point={lat2},{lng2}&vehicle={vehiculo}"
        f"&locale=es&instructions=true&key={API_KEY}"
    )

    respuesta = requests.get(url)
    datos = respuesta.json()
    estado = respuesta.status_code

    if estado == 200:
        ruta = datos["paths"][0]
        distancia_km = ruta["distance"] / 1000
        duracion_min = ruta["time"] / 60000
        print(f"\nDistancia total: {distancia_km:.2f} km")
        print(f"Duración estimada: {duracion_min:.2f} minutos")
        print("\nInstrucciones del viaje:")

        traducciones = {
            "Turn right": "Gire a la derecha",
            "Turn left": "Gire a la izquierda",
            "Continue": "Continúe",
            "Arrive at destination": "Ha llegado a su destino",
            "Keep left": "Manténgase a la izquierda",
            "Keep right": "Manténgase a la derecha",
            "Drive": "Conduzca",
            "Take": "Tome",
            "onto": "hacia",
            "Merge": "Incorpórese",
            "Slight right": "Giro leve a la derecha",
            "Slight left": "Giro leve a la izquierda",
            "toward": "hacia",
            "and take": "y tome",
            "and drive": "y conduzca",
            "and": "y"
        }

        for paso in ruta["instructions"]:
            texto = paso["text"]
            for en, es in traducciones.items():
                texto = texto.replace(en, es)
            distancia = paso["distance"]
            print(f"- {texto} ({distancia:.2f} metros)")
    else:
        print(f"Error {estado}: {datos.get('message', 'No se pudo obtener la ruta.')}")
        print(f"URL de ruta:\n{url}")

while True:
    print("\nBienvenido al planificador de rutas de Graphhopper.")
    print("Escriba 's' o 'salir' en cualquier momento para terminar.")

    entrada_vehiculo = input("Ingrese el tipo de vehículo (auto, bicicleta, a pie): ").lower()
    if entrada_vehiculo in ["s", "salir"]:
        break
    elif entrada_vehiculo in ["auto", "carro"]:
        vehiculo = "car"
    elif entrada_vehiculo in ["bicicleta", "bici"]:
        vehiculo = "bike"
    elif entrada_vehiculo in ["a pie", "caminando", "peatón"]:
        vehiculo = "foot"
    else:
        print("Tipo de vehículo no reconocido. Intente con auto, bicicleta o a pie.")
        continue

    origen = input("Ingrese la ubicación de origen: ")
    if origen.lower() in ["s", "salir"]:
        break

    destino = input("Ingrese la ubicación de destino: ")
    if destino.lower() in ["s", "salir"]:
        break

    estado1, lat1, lng1, ubicacion1 = geocodificar(origen)
    estado2, lat2, lng2, ubicacion2 = geocodificar(destino)

    if estado1 == 200 and estado2 == 200:
        print(f"\nCalculando ruta desde {ubicacion1} hasta {ubicacion2} en {entrada_vehiculo}...")
        obtener_ruta(lat1, lng1, lat2, lng2, vehiculo)
    else:
        print("No se pudo calcular la ruta debido a un error en la geocodificación.")