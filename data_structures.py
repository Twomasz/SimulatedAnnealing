import random
"""
N = 0       # liczba części dostępnych w magazynie
K = 0       # liczba wybranych części do sprzedaży
B = 0       # budżet firmy
c_ki = 0    # cena zakupu i-tej części z magazynu
q_i = 0     # ilość zakupionej i-tej części z magazynu
c_si = 0    # średnia cena i-tej części wśród konkurencji
v_i = 0     # ilość aukcji i-tej części na rynku
m_recz = 0  # ręcznie ustawiana składowa marży przez kierownika
"""



class Item:
    """
    Klasa przechowująca informacje o i-tym przedmiocie w magazynie.
    Jej atrybutami są: nazwa, cena, marża. Oraz informacje rynkowe
    na temat przedmiotu takie jak: średnia cen, ilość aukcji.
    Pierwotnie dodajemy naszą część, a następnie po research-u
    jesteśmy w stanie zaktualizować marżę oraz informacje rynkowe
    niezależnie
    """

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price
        self.margin = 0
        self.avg_of_prices = price*price
        self.quantity_of_other_auctions = 10

    # def update_margin(self, margin):
    #     self.margin = margin

    def update_market_info(self, avg_of_prices, quantity_of_other_auctions):
        self.avg_of_prices = avg_of_prices
        self.quantity_of_other_auctions = quantity_of_other_auctions

    def __str__(self):
        return f'{self.name}: {self.price}, ({self.margin:.2f}%)'


class Warehouse:
    """
    Klasa przechowująca informacje o zawartości magazynu
    zawartość magazynu jest listą obiektów Item, po
    dodaniu pierwotnej, można dodać pojedyncze za
    pomocą metody add_item
    """

    def __init__(self, stored_items: list):
        self.stored_items = stored_items

    def add_item(self, item: Item):
        self.stored_items.append(item)

    def __str__(self):
        string = ''
        for item in self.stored_items:
            string += f'{item}' + ', '
        return string


class Company:
    """
    To reprezentacja naszej firmy i czynności, jakie należy wykonać, by dojść do rozwiązania
    """

    def __init__(self, quantity_of_items_to_sell, budget, manual_margin):
        # TODO: zabezpieczenie przed wybraniem K > B
        self.quantity_of_items_to_sell = quantity_of_items_to_sell
        self.budget = budget
        self.m_manual = manual_margin

    def update_margins_from_warehouse(self, warehouse: Warehouse):  # metoda do obliczania marż wszystkich przedmiotów
        for item in warehouse.stored_items:
            avg_of_prices, quantity_of_auctions = item.avg_of_prices, item.quantity_of_other_auctions

            item.margin = self.m_manual + (avg_of_prices - item.price) / item.price + quantity_of_auctions / 50


class Solution:
    def __init__(self, company: Company, stored_items: list, solution=dict(), type: str ='random', type2: str ='random'):
        self.company = company
        self.stored_items = stored_items
        self.solution = {'indexes': [], 'quantity': []}

        if solution is {}:
            self.__find_initial_solution(type)
        elif len(solution) > 0:
            self.solution = solution
        else:
            raise ValueError('Nieprawidłowy typ')

    def __gt__(self, other):
        return self.solution > other.solution

    def __lt__(self, other):
        return self.solution < other.solution

    def __find_initial_solution(self, type='random'):
        K = self.company.quantity_of_items_to_sell

        if type == 'random':
            # random
            elems_idx = [i for i in range(len(self.stored_items))]
            self.solution['indexes'] = random.sample(elems_idx, k=K)
            first_random_idx = self.solution['indexes'][0]
            Q = self.company.budget // (2*self.stored_items[first_random_idx].price)
            self.solution['quantity'] = [random.randint(1, Q) for _ in range(K)]

        elif type == 'smallest':
            pass
            # najmniejsze
        elif type == 'greatest':
            pass
            # największe
        else:
            raise ValueError('Nieprawidłowy typ rozwiązania początkowego')

    def repair_solution(self):
        if self.not_in_budget():
            self.solution['quantity'] = [x-1 for x in self.solution['quantity']]

            # rekurencja
            self.repair_solution()

    def __total_price(self):
        indexes = self.solution['indexes']
        quantity = self.solution['quantity']

        total_price = 0
        for i in range(self.company.quantity_of_items_to_sell):
            idx = indexes[i]
            total_price += self.stored_items[idx].price * quantity[i]

    def not_in_budget(self):
        if self.__total_price > self.company.budget:  # rozwiązanie nie mieści się w budżecie
            return True
        else:
            return False

    # TODO: przekazanie 66% części do kolejnego obiektu

    def find_adjacency_solution(self, type2='random'):
        K = self.company.quantity_of_items_to_sell
        drop_times = round(K * (2/3))

        if type2 == 'random':
            same_elems_idx = random.sample([i for i in range(K)], K-drop_times)
            self.solution['indexes'] = [self.solution['indexes'][i] for i in same_elems_idx]
            self.solution['quantity'] = [self.solution['quantity'][i] for i in same_elems_idx]

            while len(self.solution['indexes']) < K:
                new_elem_idx = random.randint(0, K)
                if new_elem_idx not in self.solution['indexes']:
                    self.solution['indexes'].append(new_elem_idx)

                    Q = self.company.budget // (2 * self.stored_items[new_elem_idx].price)
                    self.solution['quantity'].append(random.randint(1, Q))

            self.repair_solution()

        elif type2 == '2':
            pass

        elif type2 == '3':

            return Solution(self.company, self.stored_items)
        else:
            raise ValueError('Nieprawidłowy typ definicji sąsiedztwa')


