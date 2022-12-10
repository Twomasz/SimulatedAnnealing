from data_structures import Item, Warehouse


# 5 przykładowych częsci oraz przykładowy obiekt Warehouse

stored_items = [Item('Wahacz przedni BMW E46', 100), Item('Wahacz tylni BMW E46', 150),
               Item('Klocki hamulcowe BMW E46', 190), Item('Dyferencjal BMW E46', 300), Item('Katalizator BMW E46', 610)]


warehouse = Warehouse(stored_items)
print(warehouse)

