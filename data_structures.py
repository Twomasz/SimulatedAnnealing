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
    Klasa przechowująca informacje o i-tym przedmiocie w magazynie
    """
    def __init__(self, name: str, price: float, quantity: int):
        self.name = name
        self.price = price
        self.quantity = quantity


class MarketInfo:
    """
    Klasa przechowująca informacje rynkowe o i-tym przedmiocie
    """
    def __int__(self):
        self.info = dict()

    def update_info(self, name, avg_of_prices, quantity_of_auctions):
        self.info[name] = (avg_of_prices, quantity_of_auctions)


class Warehouse:
    """
    Klasa przechowująca informacje o zawartości magazynu
    """

    def __int__(self, stored_items: list):
        self.stored_items = stored_items
        self.N = len(self.stored_items)


    def add_item(self, item: Item):
        self.stored_items.append(item)
        self.N = len(self.stored_items)


class Company:
    """
    To reprezentacja naszej firmy i czynności, jakie należy wykonać, by dojść do rozwiązania
    """
    def __int__(self, K, B, m_manual):
        self.K = K
        self.B = B
        self.m_manual = m_manual

    def get_margins_from_warehouse(self, warehouse: Warehouse, market_info: MarketInfo):  # metoda do obliczania marż wszystkich przedmiotów
        items_margins = dict()

        info_dict = market_info.info

        for i in range(warehouse.N):
            item = warehouse.stored_items[i]
            avg_of_prices, quantity_of_auctions = info_dict[item.name]

            ingredient1 = (avg_of_prices - item.price) / item.price

            ingredient2 = quantity_of_auctions / 50

            # TODO: wymyslic zalezność kupowanej ilości od zmiejszającego się popytu

            items_margins[item.name] = self.m_manual + ingredient1 + ingredient2

        return items_margins

