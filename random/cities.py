from city import City
import pickle

with open('random/cities.pkl', 'rb') as f:
    list_cities = pickle.load(f)