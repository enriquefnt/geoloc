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
    gpx_route.points.append(gpxpy.gpx.GPXRoutePoint(latitudes[0], longitudes[0]))

    prev_bearing = None

    for i in range(1, len(df)-1):
        lat1, lon1 = latitudes[i-1], longitudes[i-1]
        lat2, lon2 = latitudes[i], longitudes[i]

        # Calcular el rumbo
        bearing = calculate_bearing(lat1, lon1, lat2, lon2)

        # Calcular la distancia
        distance = geodesic((lat1, lon1), (lat2, lon2)).kilometers

        # Verificar si el cambio de rumbo es mayor a 1 grado y la distancia es mayor a 20 km
        if (prev_bearing is None or abs(bearing - prev_bearing) >= 1) and distance > 20:
            gpx_route.points.append(gpxpy.gpx.GPXRoutePoint(lat2, lon2))
            prev_bearing = bearing

    # Agregar último punto como waypoint de arribo
    gpx_route.points.append(gpxpy.gpx.GPXRoutePoint(latitudes.iloc[-1], longitudes.iloc[-1]))

    # Guardar archivo GPX con el nombre generado
    with open(gpx_filename, "w") as f:
        f.write(gpx.to_xml())

    print(f"Archivo GPX generado: {gpx_filename}")

if __name__ == "__main__":
    main()

