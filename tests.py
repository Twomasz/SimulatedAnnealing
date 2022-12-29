from data_structures import *
from simulated_annealing import *
import pandas as pd
"""
zwiększać liczbę iteracji w coraz niższej temperaturze
schematy chłodzenia (liniowo, wykładniczo zmieniana) ???
sąsiedztwo na zasadzie różnych parametrów
np. na postawie zysku lub ilości??
wyrzucenie elementów na zasadzie parametru!!!

"""
# TODO: testy lepiej będą wyglądały w notebooku

# 5 przykładowych części oraz przykładowy obiekt Warehouse

df = pd.read_csv('data/Items-SmallList.csv')

warehouse = Warehouse()

for i in range(df.shape[0]):
    info = df.iloc[i]
    name = info['Nazwa części']  # info['Marka'] + ' ' + info['Model'] + ' ' +
    item = Item(name, info['Cena zakupu [zł]'])
    item.update_market_info(info['Średnia cena rynkowa'], info['Ilość aukcji na rynku'], info['Popyt'])

    warehouse.add_item(item)


print(warehouse)

company = Company(4, 10000, 0.2)

# s = Solution(company, warehouse.stored_items, 'init', init_ver='smallest')

# temps = TemperatureFunction(1000, 0.95, 5, version='geometric')
# iters = IterationsFunction(100, 200, 5, version='square')
temps = [1000, 900, 800, 700, 600]
iters = [1, 1, 1, 1, 1]

print(SimulatedAnnealing(company, warehouse.stored_items, temps, iters)[:2])
