N = 0       # liczba części dostępnych w magazynie
K = 0       # liczba wybranych części do sprzedaży
B = 0       # budżet firmy
c_ki = 0    # cena zakupu i-tej części z magazynu
q_i = 0     # ilość zakupionej i-tej części z magazynu
c_si = 0    # średnia cena i-tej części wśród konkurencji
v_i = 0     # ilość aukcji i-tej części na rynku
m_recz = 0  # ręcznie ustawiana składowa marży przez kierownika



class Item:
    """
    Klasa przechowująca informacje o i-tym przedmiocie w magazynie
    """
    def __init__(self, price: float, quantity: int):
        self.price = price
        self.quantity = quantity


class Warehouse:
    """
    Klasa przechowująca informacje o zawartości magazynu
    """
    def __int__(self, stored_items: list):
        self.stored_items = stored_items



