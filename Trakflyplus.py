import pandas as pd
import gpxpy
import gpxpy.gpx
from geopy.distance import geodesic
import math

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

    # Inicializar variables previas para control de filtros y para calcular distancia y rumbo entre waypoints adicionados
    prev_bearing = None
    prev_lat = latitudes[0]
    prev_lon = longitudes[0]

    # Agregar primer punto como waypoint de salida con descripción vacía o nula (no hay distancia ni rumbo previo)
    first_point = gpxpy.gpx.GPXRoutePoint(prev_lat, prev_lon, description="Inicio del recorrido")
    gpx_route.points.append(first_point)

    # Recorrer el dataframe para agregar waypoints con filtros y descripciones
    for i in range(1, len(df)-1):
        lat = latitudes[i]
        lon = longitudes[i]
        bearing = calculate_bearing(prev_lat, prev_lon, lat, lon)
        distance = geodesic((prev_lat, prev_lon), (lat, lon)).kilometers

        if (prev_bearing is None or abs(bearing - prev_bearing) >= min_bearing_change) and distance > min_distance_km:
            desc = f"Bearing: {bearing:.2f}°\nDistance: {distance:.2f} km"
            waypoint = gpxpy.gpx.GPXRoutePoint(lat, lon, description=desc)
            gpx_route.points.append(waypoint)
            prev_bearing = bearing
            prev_lat = lat
            prev_lon = lon

    # Agregar último punto como waypoint de arribo con descripción calculada respecto al previo agregado
    lat_end = latitudes.iloc[-1]
    lon_end = longitudes.iloc[-1]
    bearing_end = calculate_bearing(prev_lat, prev_lon, lat_end, lon_end)
    distance_end = geodesic((prev_lat, prev_lon), (lat_end, lon_end)).kilometers
    desc_end = f"Bearing: {bearing_end:.2f}°\nDistance: {distance_end:.2f} km (último punto)"
    last_point = gpxpy.gpx.GPXRoutePoint(lat_end, lon_end, description=desc_end)
    gpx_route.points.append(last_point)

    # Guardar archivo GPX con el nombre generado y codificación UTF-8
    with open(gpx_filename, "w", encoding="utf-8") as f:
        f.write(gpx.to_xml())

    print(f"Archivo GPX generado: {gpx_filename}")

if __name__ == "__main__":
    main()
