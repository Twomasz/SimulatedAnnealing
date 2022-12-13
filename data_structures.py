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
    def __init__(self, company: Company, stored_items: list, type: str ='prob', type2: str ='1'):
        self.company = company
        self.stored_items = stored_items
        self.solution = {'indexes': None, 'quantity': None}
        self.__find_first_solution(type)

    def __gt__(self, other):
        return self.solution > other.solution

    def __lt__(self, other):
        return self.solution < other.solution

    def __find_first_solution(self, type='prob'):
        if type == 'prob':
            # random
            elems_idx = [i for i in range(len(self.stored_items))]
            self.solution['indexes'] = random.choices(elems_idx, k=self.company.quantity_of_items_to_sell)

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


            # rekurencja
            self.repair_solution()

    def not_in_budget(self):
        total_price = 0

        if total_price > self.company.budget:  # rozwiązanie nie mieści się w budżecie
            return True
        else:
            return False

    # TODO: dodać metody porównania obiektów rozwiązań i przekazanie 75% części do kolejnego obiektu

    def __find_adjacency_solution(self, type2='1'):
        if type2 == '1':
            pass

        elif type2 == '2':
            pass

        elif type2 == '3':

            return Solution(self.company, self.stored_items)
        else:
            raise ValueError('Nieprawidłowy typ definicji sąsiedztwa')


