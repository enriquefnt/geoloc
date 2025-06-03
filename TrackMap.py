import pandas as pd
import gpxpy
import gpxpy.gpx
from geopy.distance import geodesic
import math
import folium
import webbrowser
import os

def main():
    # Pedir al usuario el nombre del archivo CSV
    csv_filename = input("Ingresa el nombre del archivo CSV (por ejemplo, puntos.csv): ").strip()

    # Extraer el nombre base para generar el archivo GPX
    if csv_filename.lower().endswith('.csv'):
        gpx_filename = csv_filename[:-4] + '.gpx'
    else:
        gpx_filename = csv_filename + '.gpx'

    # Pedir al usuario el valor mínimo de cambio de rumbo en grados
    while True:
        try:
            min_bearing_change = float(input("Ingresa el cambio de rumbo mínimo en grados (por ejemplo, 1): "))
            if min_bearing_change < 0:
                print("Por favor ingresa un valor positivo.")
                continue
            break
        except ValueError:
            print("Por favor ingresa un número válido.")

    # Pedir al usuario la distancia mínima en kilómetros
    while True:
        try:
            min_distance_km = float(input("Ingresa la distancia mínima entre puntos en kilómetros (por ejemplo, 20): "))
            if min_distance_km < 0:
                print("Por favor ingresa un valor positivo.")
                continue
            break
        except ValueError:
            print("Por favor ingresa un número válido.")

    # Carga del CSV
    df = pd.read_csv(csv_filename)
    df.columns = df.columns.str.strip()  # elimina espacios

    # Asegúrate de que estas columnas existan (ajustá si tienen otros nombres)
    latitudes = df['lat']
    longitudes = df['lon']

    # Función para calcular el rumbo entre dos puntos
    def calculate_bearing(lat1, lon1, lat2, lon2):
        dLon = math.radians(lon2 - lon1)
        lat1 = math.radians(lat1)
        lat2 = math.radians(lat2)

        x = math.sin(dLon) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(dLon))
        bearing = math.atan2(x, y)
        return (math.degrees(bearing) + 360) % 360

    # Crear archivo GPX
    gpx = gpxpy.gpx.GPX()

    # Crear una ruta y una lista de waypoints
    gpx_route = gpxpy.gpx.GPXRoute()
    gpx.routes.append(gpx_route)

    # Agregar primer punto como waypoint de salida
    first_lat = latitudes[0]
    first_lon = longitudes[0]
    gpx_route.points.append(gpxpy.gpx.GPXRoutePoint(first_lat, first_lon))

    prev_bearing = None
    prev_lat = first_lat
    prev_lon = first_lon

    # Crear un mapa centrado en el primer punto
    m = folium.Map(location=[first_lat, first_lon], zoom_start=10)

    # Lista para almacenar los waypoints añadidos para la capa polylínea en el mapa
    filtered_points = [(first_lat, first_lon)]

    # Agregar marcador en el primer punto
    folium.Marker([first_lat, first_lon], popup=f'Lat: {first_lat}, Lon: {first_lon}').add_to(m)

    for i in range(1, len(df)-1):
        lat2, lon2 = latitudes[i], longitudes[i]

        # Calcular el rumbo
        bearing = calculate_bearing(prev_lat, prev_lon, lat2, lon2)

        # Calcular la distancia
        distance = geodesic((prev_lat, prev_lon), (lat2, lon2)).kilometers

        # Verificar si el cambio de rumbo es mayor al mínimo y la distancia mayor al mínimo
        if (prev_bearing is None or abs(bearing - prev_bearing) >= min_bearing_change) and distance > min_distance_km:
            # Añadir al GPX
            gpx_route.points.append(gpxpy.gpx.GPXRoutePoint(lat2, lon2))
            prev_bearing = bearing
            prev_lat = lat2
            prev_lon = lon2

            # Añadir a la lista de puntos filtrados para la polilinea
            filtered_points.append((lat2, lon2))

            # Agregar marcador al mapa
            folium.Marker([lat2, lon2], popup=f'Lat: {lat2}, Lon: {lon2}').add_to(m)

    # Agregar último punto como waypoint de arribo
    last_lat = latitudes.iloc[-1]
    last_lon = longitudes.iloc[-1]
    gpx_route.points.append(gpxpy.gpx.GPXRoutePoint(last_lat, last_lon))

    # Añadir último punto a la lista filtered_points
    filtered_points.append((last_lat, last_lon))

    # Agregar marcador para el último punto
    folium.Marker([last_lat, last_lon], popup=f'Lat: {last_lat}, Lon: {last_lon}').add_to(m)

    # Dibujar una única PolyLine que conecta todos los puntos filtrados (waypoints)
    folium.PolyLine(locations=filtered_points, color='blue').add_to(m)

    # Guardar archivo GPX con codificación UTF-8
    with open(gpx_filename, "w", encoding="utf-8") as f:
        f.write(gpx.to_xml())

    # Guardar el mapa en un archivo HTML
    map_filename = gpx_filename[:-4] + '.html'
    m.save(map_filename)

    print(f"Archivo GPX generado: {gpx_filename}")
    print(f"Mapa generado: {map_filename}")

    # Abrir el mapa generado en el navegador por defecto
    abs_path = os.path.abspath(map_filename)
    import webbrowser
    webbrowser.open(f"file://{abs_path}")

if __name__ == "__main__":
    main()

