import math
from typing import List


# My functions
def get_coordinates(data: str) -> List:
    """Function converts string into list of lists with coordinates"""

    coordinates = []
    data = data.strip()
    data = data.strip('</coordinates>')
    data = data.split(' ')
    for element in data:
        if element != '':
            coordinates.append(element.split(','))
    return coordinates


def longtitude_corrector(longtitude: float) -> float:
    """The function corrects the distance in meters depending on latitude."""

    equator_degree_meters = 111321.377778   # The number of meters in 1 degree at the equator
    current_longtitude_meters = math.cos(math.radians(longtitude)) * equator_degree_meters
    current_longtitude_radius = radius / current_longtitude_meters
    return current_longtitude_radius


def create_circles(coordinates: List) -> str:
    """Function generates circles coordinates"""

    latitude_radius = radius / 111134.861111
    longitude_radius = longtitude_corrector(float(coordinates[1]))
    latitude = float(coordinates[1])
    longitude = float(coordinates[0])
    result = []
    for angle in range(0, 360, 10):
        dx = latitude_radius * math.cos(math.radians(angle))
        dy = longitude_radius * math.sin(math.radians(angle))
        new_latitude = latitude + dx
        new_longitude = longitude + dy
        coordinate = f'{new_longitude},{new_latitude},0'
        result.append(coordinate)
    result.append(result[0])
    result = ' '.join(result)
    return result


# Main code
radius = 1500  # Enter the required circle radius

with open('input.kml', 'r') as border_file:  # Finding string with coordinates
    for i_string in border_file:
        if '<coordinates>' in i_string:
            border = i_string

coordinates = get_coordinates(border)

with open('result.kml', 'w') as result_file:
    result_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    result_file.write('<kml xmlns="http://earth.google.com/kml/2.2">\n')
    result_file.write('  <Document>\n')
    for coordinate in coordinates:
        with open('round_start.txt', 'r') as round_start:
            for string in round_start:
                result_file.write(string)
        result_file.write('            <coordinates>')
        result_file.write(create_circles(coordinate))
        result_file.write(' </coordinates>\n')
        with open('round_stop.txt', 'r') as round_stop:
            for i_string in round_stop:
                result_file.write(i_string)
    result_file.write('  </Document>\n')
    result_file.write('</kml>')
