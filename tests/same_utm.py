import math

def euclidean_distance(utm1, utm2):
    x1, y1 = utm1
    x2, y2 = utm2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Assumindo ambos os pontos na mesma zona
distance_utm = euclidean_distance(point1, point2)
print(f"Distância euclidiana: {distance_utm:.2f} metros")
