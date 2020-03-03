import glob
import json

'''This class represent an ingredient'''


class Ingredient:

    def __init__(self, name, price, seconds):
        self.name = name
        self.price = price
        self.seconds = seconds

    def __str__(self):
        return self.name + ' cost ' + str(self.price) + ' seconds ' + str(self.seconds)


'''This is singleton class, represent map of the ingredients, <NAME,Ingredient>'''


class Ingredient_map:


    class __Ingredient_map:
        FILE_NAME = "Ing.json"

        def __init__(self):
            self.map = dict()

        def __str__(self):
            return str(map)

        def read_from_json(self):
            ing = None
            with open(self.FILE_NAME, 'r') as file:
                for line in file:
                    ing = json.loads(line)
                    self.map[ing['name']] = Ingredient(ing['name'], ing['price'], ing['sec'])

    @staticmethod
    def get_meals_map():
        meals_map = {}
        SIZEOFEND = -4

        for f in glob.glob('*.txt'):
            with open(f, 'r') as file:
                for line in file:
                    ing = line.replace('\n','')
                    f_name = file.name[:SIZEOFEND]
                    if meals_map.get(f_name) is None:
                        meals_map[f_name] = []

                    meals_map[f_name].append(ing)
        return meals_map

    instance = None

    def __init__(self):
        if not Ingredient_map.instance:
            Ingredient_map.instance = Ingredient_map.__Ingredient_map()
            Ingredient_map.instance.read_from_json()
