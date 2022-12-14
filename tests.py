from data_structures import *
from simulated_annealing import SimulatedAnnealing
"""
zwiekszac liczbe iteracji w coraz nizszej temperaturze
schematy chlodzenia (liniowo, wykladniczo zmieniana) ???
sąsiedztwo na zasadzie róznych parametrów
np. na postawie zysku lub ilości??
wyrzucenie elementów na zasadzie parametru!!!

"""


# 5 przykładowych częsci oraz przykładowy obiekt Warehouse

stored_items = [Item('Wahacz przedni BMW E46', 100), Item('Wahacz tylni BMW E46', 150),
                Item('Klocki hamulcowe BMW E46', 190), Item('Dyferencjał BMW E46', 300),
                Item('Katalizator BMW E46', 610)]


warehouse = Warehouse(stored_items)
print(warehouse)

company = Company(3, 10000, 0.1)

company.update_margins_from_warehouse(warehouse.stored_items)

print(warehouse)

print(SimulatedAnnealing(company, warehouse.stored_items, 10, 1, 5))

# solution = Solution(company, warehouse.stored_items, solution_type='init')
#
#
#
# print(solution.solution)
#
# print(warehouse)
#
# solution2 = solution.find_adjacency_solution()
#
# print(solution2.solution)
#
# print(warehouse)
