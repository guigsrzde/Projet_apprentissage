from PyQt5.QtGui import QImage, QColor
from city import City
import pickle

#couleur du bleu sur la map du dossier random: (66, 113, 169)

path = "random/map.png"
image = QImage(path)
color = image.pixelColor(0, 0)
blue = (color.red(), color.green(), color.blue())
max_x = 1003
max_y = 760
print(image.size())

def in_sea(image:QImage, town):
    color = image.pixelColor(town.x, town.y)
    r, g, b = color.red(), color.green(), color.blue()
    if abs(r-blue[0])+abs(g-blue[1])+abs(b-blue[2]) < 20:
        return True
    return False

def print_city_attributes(city_instance):
    for attr, value in city_instance.__dict__.items():
        print(f"{attr}: {value}")
    print("Is the city in the Sea ?", in_sea(image, city_instance))


list_cities = []

for i in range (20):
    test = City.random(max_x, max_y, i)
    while True:
        if not in_sea(image, test):
            break
        test = City.random(max_x, max_y, i)
    list_cities.append(test)


with open('cities.pkl', 'wb') as f:
    pickle.dump(list_cities, f)