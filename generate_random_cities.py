from PyQt5.QtGui import QImage, QColor
from city import City
import pickle

# couleur du bleu sur la map du dossier random: (63, 160, 255)

path = "random/map.png"
image = QImage(path)
blue = (63, 160, 255)  # Updated blue color
max_x = 1003
max_y = 760

def in_sea(image: QImage, town):
    color = image.pixelColor(town.x, town.y)
    r, g, b = color.red(), color.green(), color.blue()
    
    # Define thresholds for RGB values (adjusted for sea color matching)
    threshold = 50
    r_diff = abs(r - blue[0])
    g_diff = abs(g - blue[1])
    b_diff = abs(b - blue[2])
    
    # Check if the color is close enough to the blue sea color
    return r_diff < threshold and g_diff < threshold and b_diff < threshold

def print_city_attributes(city_instance):
    for attr, value in city_instance.__dict__.items():
        print(f"{attr}: {value}")
    print("Is the city in the Sea?", in_sea(image, city_instance))

list_cities = []

for i in range(20):
    while True:
        # Generate random cities correctly
        test = City.random(max_x, max_y, i)
        assert 0 <= test.x < image.width()
        assert 0 <= test.y < image.height()
        
        if not in_sea(image, test):  # Check if the city is not in the sea
            list_cities.append(test)
            break

# Save the list of cities
with open('cities.pkl', 'wb') as f:
    pickle.dump(list_cities, f)
