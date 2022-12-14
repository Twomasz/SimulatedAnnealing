import random
from typing import List
"""
N = 0       # liczba części dostępnych w magazynie
K = 0       # liczba wybranych części do sprzedaży
B = 0       # budżet firmy
c_ki = 0    # cena zakupu i-tej części z magazynu
q_i = 0     # ilość zakupionej i-tej części z magazynu
c_si = 0    # średnia cena i-tej części wśród konkurencji
v_i = 0     # ilość aukcji i-tej części na rynku
m_ręczna = 0  # ręcznie ustawiana składowa marży przez kierownika
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
        self.quantity = 0   # ilość w aktualnym rozwiązaniu, początkowo zero
        # self.avg_of_prices = price*price
        # self.quantity_of_other_auctions = 10
        self.market_info = {'avg_of_prices': price*price,
                            'quantity_of_other_auctions': 20,
                            'demand': 50}

    def update_market_info(self, avg_of_prices, quantity_of_other_auctions):
        self.market_info['avg_of_prices'] = avg_of_prices
        self.market_info['quantity_of_other_auctions'] = quantity_of_other_auctions

    def get_profit(self):
        profit = self.margin * self.price * self.quantity
        return profit

    def __repr__(self):
        return f"{self.name}: {self.price}x({self.quantity}+{self.market_info['quantity_of_other_auctions']}), {self.margin:.2f}%"


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
        return f'{self.stored_items}'


class Company:
    """
    To reprezentacja naszej firmy i czynności, jakie należy wykonać, by dojść do rozwiązania
    """

    def __init__(self, quantity_of_items_to_sell, budget, manual_margin):
        # TODO: zabezpieczenie przed wybraniem K > B
        # czy posługujemy się nazwami K, B czy lepiej dać dłuższe bardziej opisowe nazwy?
        self.quantity_of_items_to_sell = quantity_of_items_to_sell
        self.budget = budget
        self.m_manual = manual_margin

    def update_margins_from_warehouse(self, items_in_warehouse):  # metoda do obliczania marż wszystkich przedmiotów
        for item in items_in_warehouse:
            market_avg = item.market_info['avg_of_prices']
            market_quantity = item.market_info['quantity_of_other_auctions']
            demand = item.market_info['demand']

            # wzór został wytłumaczony w prezentacji
            item.margin = self.m_manual + (market_avg-item.price)/item.price - (market_quantity+item.quantity)/demand


class Solution:
    def __init__(self, company: Company, stored_items: List[Item], solution_type, sol_from_last_object=None,
                 init_ver: str = 'random'):
        """
        :param company: Klasa przechowująca informacje o firmie
        :param stored_items: Lista elementów w magazynie
        :param solution_type: 'init' - rozwiązanie początkowe / 'adj' - rozwiązanie sąsiadujące
        :param sol_from_last_object: przekazanie listy elementów z poprzedniego rozwiązania
        :param init_ver: 'random' - losowo wybierane elementy w rozwiązaniu początkowym
        """

        self.company = company
        self.stored_items = stored_items
        self.solution = []   # solution zawiera indeksy wybranych elementów z listy stored_items

        if solution_type == 'init':
            self.__find_initial_solution(init_ver)
        elif solution_type == 'adj':
            if isinstance(sol_from_last_object, list):
                self.solution = sol_from_last_object
            else:
                raise ValueError('cos sie schrzaniło wewnątrz klasy')
        else:
            raise ValueError("Nieprawidłowy typ rozwiązania, wpisz 'init' lub 'adj'")

    def __gt__(self, other):
        return self.total_profit() > other.total_profit()

    def __lt__(self, other):
        return self.total_profit() < other.total_profit()

    def __repair_solution(self):
        if self.not_in_budget():
            # print(1)
            # TODO: funkcja kary do zamiany (NA RAZIE ZOSTAWMY, ALE POTEM MOŻEMY UŻYĆ GET_PROFIT DO TEGO)
            for idx in self.solution:
                self.stored_items[idx].quantity -= 1

            # po każdej zmianie ilości produktu należy zrobić update jego marży
            self.company.update_margins_from_warehouse(self.stored_items)
            # rekurencja
            self.__repair_solution()

    def not_in_budget(self):
        if self.total_price() > self.company.budget:  # rozwiązanie nie mieści się w budżecie
            return True
        else:
            return False

    def total_price(self):
        total_price = 0
        for idx in self.solution:
            total_price += self.stored_items[idx].price * self.stored_items[idx].quantity
        # print(total_price)
        return total_price

    def __find_initial_solution(self, version='random'):
        K = self.company.quantity_of_items_to_sell

        if version == 'random':
            # random
            elems_idx = [i for i in range(len(self.stored_items))]
            self.solution = random.sample(elems_idx, k=K)

            for idx in self.solution:
                up_limit = self.company.budget // (2 * self.stored_items[idx].price)
                self.stored_items[idx].quantity = random.randint(1, up_limit)

            # gdy nie mieścimy się w budżecie firmy należy zmniejszyć ilość przedmiotów
            self.__repair_solution()
            # przed wywołaniem początkowego rozwiązania zaktualizuj marże produktów
            self.company.update_margins_from_warehouse(self.stored_items)

        elif version == 'smallest':
            pass
            # TODO: POMYSŁ: wykorzystać item.price lub item.margin i 1/K-tą budżetu
        elif version == 'greatest':
            pass
            # największe
            # TODO: POMYSŁ: wykorzystać item.price lub item.margin i 1/K-tą budżetu
        else:
            raise ValueError('Nieprawidłowy typ rozwiązania początkowego')

    # TODO: UWAŻAĆ NA STARE ZAPISY W ITEM-ACH BY TO MIAŁO SENS TRZEBA JE W DOBRYM MOMENCIE UPDATE-WAĆ

    def find_adjacency_solution(self, version='random', drop_coeff=(1/3)):
        # przed wywołaniem każdego kolejnego rozwiązania zaktualizuj marże produktów
        self.company.update_margins_from_warehouse(self.stored_items)

        K = self.company.quantity_of_items_to_sell
        drop_times = round(K * drop_coeff)

        if version == 'random':
            old_solution = self.solution
            # zostawienie części rozwiązania
            self.solution = random.sample(self.solution, K-drop_times)

            # zabezpieczenie zerujące quantity wyrzuconych przedmiotów, możliwe, że okaże się niepotrzebne
            drop_elems_idx = []
            for idx in old_solution:
                if idx not in self.solution:
                    drop_elems_idx.append(idx)
            for idx in drop_elems_idx:
                self.stored_items[idx].quantity = 0
            # koniec zabezpieczenia

            while len(self.solution) < K:
                new_elem_idx = random.randint(0, K-1)
                if new_elem_idx not in self.solution:
                    self.solution.append(new_elem_idx)

                    Q = self.company.budget // (2 * self.stored_items[new_elem_idx].price)
                    self.stored_items[new_elem_idx].quantity = random.randint(1, Q)

            # gdy nie mieścimy się w budżecie firmy należy zmniejszyć ilość przedmiotów
            self.__repair_solution()
            # przed wywołaniem początkowego rozwiązania zaktualizuj marże produktów
            self.company.update_margins_from_warehouse(self.stored_items)

            return Solution(self.company, self.stored_items, solution_type='adj', sol_from_last_object=self.solution)

        elif version == '2':
            pass

        elif version == '3':
            pass
        else:
            raise ValueError('Nieprawidłowy typ definicji sąsiedztwa')

    def total_profit(self):
        total_profit = 0

        for idx in self.solution:
            total_profit += self.stored_items[idx].get_profit()

        return total_profit

