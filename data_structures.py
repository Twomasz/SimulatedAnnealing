import random
from typing import List
from copy import deepcopy


class Item:
    """
    Klasa przechowująca informacje o i-tym przedmiocie w magazynie. Jej atrybutami są: nazwa, cena, marża.
    Zawiera także informacje rynkowe na temat przedmiotu takie jak: średnia cen, ilość aukcji i popyt.
    Pierwotnie dodajemy naszą część, a następnie po research-u jesteśmy w stanie zaktualizować marżę
    oraz informacje rynkowe.
    """

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price
        self.margin = 0    # marża jako ułamek (nie procent!)
        self.quantity = 0  # ilość w aktualnym rozwiązaniu, początkowo zero
        self.market_info = {'avg_of_prices': 0,
                            'quantity_of_other_auctions': 0,
                            'demand': 0}

    def update_market_info(self, avg_of_prices, quantity_of_other_auctions, demand):
        self.market_info['avg_of_prices'] = avg_of_prices
        self.market_info['quantity_of_other_auctions'] = quantity_of_other_auctions
        self.market_info['demand'] = demand

    def get_profit(self):
        profit = self.margin * self.price * self.quantity
        return profit

    def __repr__(self):
        return f"{self.name}: ({self.quantity}+{self.market_info['quantity_of_other_auctions']})x{self.price}zł, " \
               f"{self.margin * 100:.2f}%"

    def __str__(self):
        return f"{self.name}: \n {int(self.quantity)}x{self.price}zł, {self.margin * 100:.2f}%"


class Warehouse:
    """
    Klasa przechowująca informacje o zawartości magazynu zawartość magazynu jest listą obiektów Item,
    po dodaniu pierwotnej, można dodać pojedyncze za pomocą metody add_item
    """

    def __init__(self, stored_items=None):
        if stored_items is None:
            stored_items = []
        self.stored_items = stored_items

    def add_item(self, item: Item):
        self.stored_items.append(item)

    def __str__(self):
        return f'{self.stored_items}'


class Company:
    """
    To reprezentacja naszej firmy i czynności, jakie wykonuje firma, tj. analizuje wartości rynkowe oraz ilość
    produktów, które chce wypuścić na rynek i na tej podstawie wyznacza marżę tego produktu.
    """

    def __init__(self, quantity_of_items_to_sell, budget, manual_margin):
        self.quantity_of_items_to_sell = quantity_of_items_to_sell
        self.budget = budget
        self.m_manual = manual_margin

    def update_margins_from_warehouse(self, items_in_warehouse):  # metoda do obliczania marż wszystkich przedmiotów
        for item in items_in_warehouse:
            market_avg = item.market_info['avg_of_prices']
            market_quantity = item.market_info['quantity_of_other_auctions']
            demand = item.market_info['demand'] * 10

            # wzór został wytłumaczony w prezentacji
            item.margin = self.m_manual + (market_avg - item.price) / item.price - (
                        market_quantity + item.quantity) / demand


class Solution:
    def __init__(self, company: Company, stored_items: List[Item], solution_type, init_ver: str = 'random',
                 adj_ver: str = 'random', drop_coeff=(1/3), previous_solution=None):
        """
        @param company: Klasa przechowująca informacje o firmie
        @param stored_items: Lista elementów w magazynie
        @param solution_type: 'init' - rozwiązanie początkowe / 'adj' - rozwiązanie sąsiadujące
        @param init_ver: wersja rozwiązania początkowego (potrzebna w przypadku solution_type = 'init')
        @param adj_ver: wersja rozwiązania sąsiadującego (potrzebna w przypadku solution_type = 'adj')
        @param drop_coeff: Współczynnik wyrzucanej liczby części (potrzebny w przypadku solution_type = 'adj')
        @param previous_solution: przekazanie listy elementów z poprzedniego rozwiązania
                (potrzebny w przypadku solution_type = 'adj')
        """

        self.company = company
        self.stored_items = deepcopy(stored_items)
        self.N = len(stored_items)                  # ilość elementów w magazynie
        self.K = company.quantity_of_items_to_sell  # ilość elementów do wybrania
        self.solution = []   # solution zawiera indeksy wybranych elementów z listy stored_items
        self.profit = None   # całkowity zysk z wybranego rozwiązania

        # zaktualizuj marże produktom przed znalezieniem rozwiązania
        self.company.update_margins_from_warehouse(self.stored_items)

        if solution_type == 'init':
            self.__find_initial_solution(init_ver)

        elif solution_type == 'adj':
            if isinstance(previous_solution, list):
                self.solution = deepcopy(previous_solution)
                self.__find_adjacency_solution(adj_ver, drop_coeff)

            else:
                raise ValueError('Poprzednie rozwiązanie nie jest listą!')
        else:
            raise ValueError("Nieprawidłowy typ rozwiązania, wpisz 'init' lub 'adj'")

        # po znalezieniu rozwiązania należy sprawdzić jego poprawność
        self.__repair_solution()
        # a następnie zaktualizować zysk ze znalezionego
        self.profit = self.get_total_profit()

    def __ge__(self, other):
        return self.profit >= other.profit

    def __lt__(self, other):
        return self.profit < other.profit

    def __sub__(self, other):
        return self.profit - other.profit

    def __repair_solution(self):
        if self.not_in_budget():
            # TODO: funkcja kary do zamiany (NA RAZIE ZOSTAWMY, ALE POTEM MOŻEMY UŻYĆ GET_PROFIT DO TEGO)
            # worst_item = self.stored_items[self.solution[0]]
            # for idx in self.solution:
            #     if self.stored_items[idx].get_profit() < worst_item.get_profit():
            #         worst_item = self.stored_items[idx]
            #
            # worst_item.quantity -= 1

            for idx in self.solution:
                if self.stored_items[idx].quantity > 1:  # zabezpieczenie przed ujemną ilością
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

        return total_price

    def get_total_profit(self):
        total_profit = 0
        for idx in self.solution:
            total_profit += self.stored_items[idx].get_profit()

        return total_profit

    def __find_initial_solution(self, version='random'):
        """
        Metoda do znajdowania rozwiązania początkowego algorytmu, uruchamiana jako domyślny parametr
        w momencie inicjalizacji klasy
        @param version: Parametr decydujący o wyborze wariantu rozwiązania początkowego
                'random': wybór części, jak i ich ilości jest dobierany w sposób losowy
                'greatest': wybór części o najwyższej marży przed wprowadzeniem swoich części na rynek
                'uncommon': wybór części, które występują na rynku najrzadziej
        """

        if version not in ['random', 'greatest', 'uncommon']:   # zabezpieczenie
            raise ValueError('Nieprawidłowy typ rozwiązania początkowego')

        if version == 'random':
            # random
            elems_idx = list(range(self.N))
            self.solution = random.sample(elems_idx, k=self.K)

            for idx in self.solution:
                up_limit = self.company.budget // (2 * self.stored_items[idx].price)
                self.stored_items[idx].quantity = random.randint(1, up_limit)

        else:  # inne metody wyboru mają dużo wspólnej logiki, stąd warunek else z kolejnymi podwarunkami

            # stworzenie słownika przechowującego indeksy oraz elementy z listy stored_items
            dict_items = {i: self.stored_items[i] for i in range(self.N)}

            if version == 'greatest':
                # sortowane są elementy pod względem marży (od największej)
                sorted_tuple = sorted(dict_items.items(), key=lambda x: x[1].margin, reverse=True)

            else:  # version == 'uncommon':
                # sortowane są elementy pod względem najrzadszego występowania na rynku
                sorted_tuple = sorted(dict_items.items(),
                                      key=lambda x: x[1].market_info['quantity_of_other_auctions'], reverse=True)

            # z powstałej krotki wybieram K indeksów, pod którymi kryją się elementy z najwyższą marżą
            self.solution = [idx_item[0] for idx_item in sorted_tuple[:self.K]]

            part_of_budget = self.company.budget / self.K

            for idx in self.solution:
                quantity = part_of_budget // self.stored_items[idx].price
                self.stored_items[idx].quantity = quantity

    def __find_adjacency_solution(self, version: str = 'random', drop_coeff=(1/3)):
        """
        Metoda do znajdowania rozwiązania sąsiedniego do tego obecnego. Zawiera 3 warianty definicji sąsiedztwa
        @param version: Parametr decydujący o wyborze wariantu sąsiedztwa:
                'random': wybór części, jak i ich ilości jest dobierany w sposób losowy
                'margins': wybór części mających najwyższą marżę, ilość dobierana w sposób losowy
                'profit': wybór części dające największy zysk przy częściowo losowej ilości
        @param drop_coeff: Liczba z przedziału (0, 1) mówiąca o tym, ile procent części należy wyrzucić z nowego
                rozwiązania
        @return: Metoda zwraca nowy obiekt Solution, mający wspólny ułamek części z bieżącym rozwiązaniem
        """

        drop_times = round(self.K * drop_coeff)
        new_solution = deepcopy(self.solution)

        if version == 'random':
            # zostawienie części rozwiązania
            new_solution = random.sample(new_solution, self.K - drop_times)

            # zabezpieczenie zerujące quantity wyrzuconych przedmiotów
            for idx in range(self.N):
                if idx not in new_solution:
                    self.stored_items[idx].quantity = 0

            while len(new_solution) < self.K:
                new_elem_idx = random.randint(0, self.N-1)
                if new_elem_idx not in new_solution:
                    new_solution.append(new_elem_idx)

                    q = self.company.budget // (2 * self.stored_items[new_elem_idx].price)
                    self.stored_items[new_elem_idx].quantity = random.randint(1, q)

        elif version == 'margins':
            # sortowanie elementów od tych dających największą marżę
            new_solution.sort(key=lambda x: self.stored_items[x].margin, reverse=True)
            # wyrzucenie z rozwiązania 1/n-tej elementów dających najgorszą marżę
            new_solution = new_solution[:(self.K - drop_times)]

            # nadanie wszystkim elementom poza rozwiązaniem losowej ilości, aby zasymulować zachowanie rynku po
            # wprowadzeniu swojej ilości elementów
            for idx, item in enumerate(self.stored_items):
                if idx not in new_solution:
                    up_limit = self.company.budget // self.stored_items[idx].price
                    item.quantity = random.randint(1, up_limit)

            self.company.update_margins_from_warehouse(self.stored_items)  # UPDATE!

            # posortowanie elementów według marży przy wprowadzeniu swojej ilości na rynek
            indexes = list(range(self.N))
            sorted_idx = sorted(indexes, key=lambda x: self.stored_items[x].margin, reverse=True)

            # dodanie elementów do rozwiązania tak, aby zapełnić ilość K
            n = 0
            while len(new_solution) < self.K:
                if sorted_idx[n] not in new_solution:
                    new_solution.append(sorted_idx[n])
                n += 1

            # zresetowanie ilości pozostałym produktom
            for idx in range(self.N):
                if idx not in new_solution:
                    self.stored_items[idx].quantity = 0

        elif version == 'profit':
            # sortowanie elementów od tych dających największy zysk
            new_solution.sort(key=lambda x: self.stored_items[x].get_profit(), reverse=True)
            # wyrzucenie z rozwiązania 1/n-tej elementów dających najgorszy zysk
            new_solution = new_solution[:(self.K - drop_times)]

            # nadanie wszystkim elementom poza rozwiązaniem losowej ilości, aby zasymulować zachowanie rynku po
            # wprowadzeniu swojej ilości elementów
            for idx, item in enumerate(self.stored_items):
                if idx not in new_solution:
                    up_limit = self.company.budget // (2 * self.stored_items[idx].price)
                    item.quantity = random.randint(1, up_limit)

            self.company.update_margins_from_warehouse(self.stored_items)  # UPDATE!

            # posortowanie elementów według przynoszącego zysku przy wprowadzeniu swojej ilości na rynek
            indexes = list(range(self.N))
            sorted_idx = sorted(indexes, key=lambda x: self.stored_items[x].get_profit(), reverse=True)

            # dodanie elementów do rozwiązania tak, aby zapełnić ilość K
            n = 0
            while len(new_solution) < self.K:
                if sorted_idx[n] not in new_solution:
                    new_solution.append(sorted_idx[n])
                n += 1

            # zresetowanie ilości pozostałym produktom
            for idx in range(self.N):
                if idx not in new_solution:
                    self.stored_items[idx].quantity = 0

        else:
            raise ValueError('Nieprawidłowy typ definicji sąsiedztwa')

        self.solution = new_solution
