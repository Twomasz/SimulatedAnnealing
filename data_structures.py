from typing import List, Tuple, Dict, Union

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
    Pierwotnie dodajemy naszą część, a następnie po researchu
    jestesmy w stanie zaktualizować marżę oraz informacje rynkowe
    niezależnie
    """

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price
        self.margin = None
        self.avg_of_prices = None
        self.quantity_of_auctions = None

    def update_margin(self, margin):
        self.margin = margin

    def update_market_info(self, avg_of_prices, quantity_of_auctions):
        self.avg_of_prices = avg_of_prices
        self.quantity_of_auctions = quantity_of_auctions


class Warehouse:
    """
    Klasa przechowująca informacje o zawartości magazynu
    zawartość magazynu jest listą obiektów Item, po
    dodaniu pierwotnej, można dodać pojedyńcze za
    pomocą metody add_item
    """

    def __init__(self, stored_items: list):
        self.stored_items = stored_items
        self.N = len(self.stored_items)

    def add_item(self, item: Item):
        self.stored_items.append(item)
        self.N = len(self.stored_items)


class Company:
    """
    To reprezentacja naszej firmy i czynności, jakie należy wykonać, by dojść do rozwiązania
    """

    def __init__(self, K, B, m_manual):
        self.K = K
        self.B = B
        self.m_manual = m_manual

    def update_margins_from_warehouse(self, warehouse: Warehouse,
                                   item: Item):  # metoda do obliczania marż wszystkich przedmiotów
        items_margins = dict()

        avg_of_prices = item.avg_of_prices
        quantity_of_auctions = item.quantity_of_auctions

        for i in range(warehouse.N):
            item = warehouse.stored_items[i]
            avg_of_prices, quantity_of_auctions = warehouse.stored_items[item.name]

            ingredient1 = (avg_of_prices - item.price) / item.price

            ingredient2 = quantity_of_auctions / 50

            # TODO: wymyslic zalezność kupowanej ilości od zmiejszającego się popytu

            items_margins[item.name] = self.m_manual + ingredient1 + ingredient2

        return items_margins


class Solution:
    def __init__(self, elems, K, type: str):
        self.elems = elems
        self.K = K
        self.solution = self.__find_solution(type)

    def __eq__(self, other):
        pass

    def __find_solution(self, type):
        if type == 'prob':
            pass
            # random
        elif type == 'smallest':
            pass
            # najmniejsze
        elif type == 'greatest':
            pass
            # najwieksze
        else:
            raise ValueError('Nieprawidłowy typ znalezienia rozwiązania początkowego')

    def repair_solution(self):
        pass

    def is_in_budget(self, budget):
        total_price = 0

        if total_price <= budget:
            return True
        else:
            return False

    # TODO: dodać metody porównania obiektów rozwiązań i przekazanie 75% części do kolejnego obiektu


