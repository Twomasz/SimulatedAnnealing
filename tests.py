from data_structures import *


# 5 przykładowych częsci oraz przykładowy obiekt Warehouse

stored_items = [Item('Wahacz przedni BMW E46', 100), Item('Wahacz tylni BMW E46', 150),
                Item('Klocki hamulcowe BMW E46', 190), Item('Dyferencjał BMW E46', 300),
                Item('Katalizator BMW E46', 610)]


warehouse = Warehouse(stored_items)
print(warehouse)

company = Company(4, 10000, 0.1)

company.update_margins_from_warehouse(warehouse)

print(warehouse)

solution = Solution(company, warehouse.stored_items)

print(solution.solution)
print(solution.repair_solution())


lst = [1,2,3,4]

print(lst[1,3])