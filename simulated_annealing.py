import numpy as np
import random
from typing import List
from data_structures import Item, Company, Solution


def TemperatureFunction(init_temp: int, cooling_rate: float, ages: int, version='arithmetic'):
    """
    Funkcja pozwalająca na zdefiniowanie różnej dynamiki zmian temperatury dla algorytmu symulowanego wyżarzania
    @param init_temp: Temperatura początkowa-należy ją dobrać intuicyjnie
    @param cooling_rate: Parametr opisujący dynamikę zmian, w zależności od wersji funkcji jest różnicą
                         ciągu arytmetycznego lub ilorazem ciągu geometrycznego
    @param ages: Mówi o liczbie wygenerowanych temperatur, co przekłada się na ilość epok w algorytmie
                 symulowanego wyżarzania
    @param version: Wersja 'linear' mówi o liniowym spadku temperatury, natomiast 'geom' mówi o spadku
    @return: lista kolejno wyliczonych temperatur
    """
    T_MIN = 1  # MINIMALNA TEMPERATURA, KTÓREJ NIE MOŻNA PRZEKROCZYĆ

    temp_array = [init_temp]

    if version == 'arithmetic':
        for i in range(ages-1):
            curr_temp = temp_array[i] - cooling_rate  # arithmetic sequence
            if curr_temp < T_MIN:
                curr_temp = T_MIN
            temp_array.append(curr_temp)

    elif version == 'geometric':
        for i in range(ages-1):
            curr_temp = temp_array[i] * cooling_rate  # geometric sequence
            if curr_temp < T_MIN:
                curr_temp = T_MIN
            temp_array.append(curr_temp)

    else:
        raise ValueError('Nieprawidłowa nazwa wersji spadku temperatury')

    return temp_array


def IterationsFunction(init_iterations, max_iterations, ages, version='linear'):
    """
    Funkcja umożliwiająca zadawanie zmiennej liczby iteracji dla kolejnych epok w algorytmie symulowanego wyżarzania.
    Zależy nam na zwiększaniu liczby iteracji w późniejszych epokach, co umożliwia więcej prób przyjęcia lepszego
    sąsiedniego rozwiązania (przy niskiej temperaturze prawdopodobieństwo przyjęcia gorszego rozwiązania jest małe)
    @param init_iterations: bazowa liczba iteracji, którą można zwiększyć
    @param max_iterations: ograniczenie górne liczby iteracji
    @param ages: liczba epok w algorytmie symulowanego wyżarzania
    @param version: wersja doboru liczby iteracji
            'constant': stała liczba iteracji niezależna od epoki
            'linear': liniowy wzrost liczby iteracji rosnący do maksymalnej liczby iteracji
            'square': tworzy wielomian rosnący na kształt ciągu geometrycznego zaczynającego się od początkowej
                      liczby iteracji, a kończącym się na maksymalnej liczbie iteracji
    @return: lista iteracji w poszczególnych epokach
    """
    N_MAX = 10000  # MAKSYMALNA LICZBA ITERACJI, KTÓREJ NIE MOŻNA PRZEKRACZAĆ

    if max_iterations < init_iterations:
        raise ValueError('Końcowa liczba iteracji jest mniejsza od początkowej')
    elif max_iterations > N_MAX:
        raise ValueError('Liczba iteracji większa niż 10 000')

    iter_array = [init_iterations]
    if version == 'constant':
        iter_array = [init_iterations for _ in range(ages)]

    elif version == 'linear':
        coeff = (max_iterations - init_iterations) / (ages - 1)
        for i in range(ages-1):
            iter_array.append(round(iter_array[i] + coeff))

    elif version == 'square':
        # tworzę dopasowanie do punktów funkcją kwadratową, tak by narastanie w początkowych
        # epokach było niewielkie, natomiast w końcowych było duże

        x = np.array([1, (ages+1)//2, ages])
        middle_iterations = init_iterations + (max_iterations - init_iterations) * 0.2
        y = np.array([init_iterations, middle_iterations, max_iterations])

        p = np.polyfit(x, y, deg=2)  # dopasowanie wielomianu 2 stopnia do 3 punktów w przestrzeni

        for i in range(2, ages+1):
            # wyliczenie i zaokrąglenie wartości wielomianu w i-tym punkcie
            iter_array.append(round(p[0]*i**2 + p[1]*i + p[2]))

    else:
        raise ValueError('Nieprawidłowa nazwa wersji funkcji')

    return iter_array


def SimulatedAnnealing(company: Company, stored_items: List[Item], temp_array: list, iter_array: list, drop_coeff=0.3,
                       init_version='random', adj_version='random'):
    """
    Właściwy algorytm symulowanego wyżarzania
    @param company: Klasa firmy nadająca marże
    @param stored_items: Części przechowywane w magazynie
    @param temp_array: Lista temperatur w poszczególnych epokach
    @param iter_array: Lista iteracji w poszczególnych epokach
    @param drop_coeff: Współczynnik mówiący o tym, jaki ułamek części wyrzucamy z sąsiedniego rozwiązania
    @param init_version: wersja rozwiązania początkowego
    @param adj_version: wersja rozwiązania sąsiadującego
    @return: Zwraca rozwiązanie końcowe, wybrane elementy oraz 'drogę' rozwiązań, jakie wybrał algorytm
    """
    if len(temp_array) != len(iter_array):   # zabezpieczenie
        raise ValueError('Brak zgodności epok w listach iteracji i temperatury')

    S = Solution(company=company, stored_items=stored_items, solution_type='init', init_ver=init_version)
    way_of_algorithm = [S.profit]

    best_result_point = (0, S.profit)  # w tej zmiennej będzie przechowywany najlepszy wynik znaleziony przez algorytm
    chosen_items = [S.stored_items[i] for i in S.solution]

    for idx, curr_temp in enumerate(temp_array):
        for _ in range(iter_array[idx]):
            # tworzenie nowego rozwiązania sąsiedniego
            S_prim = Solution(company=company, stored_items=S.stored_items, solution_type='adj', adj_ver=adj_version,
                              previous_solution=S.solution, drop_coeff=drop_coeff)

            # jeżeli S_prim okaże się lepszym rozwiązaniem to staje się nowym rozwiązaniem branym pod uwagę
            if S_prim >= S:
                S = S_prim

            # w przeciwnym wypadku delta i prawdopodobieństwo decyduje o przyjęciu tego rozwiązania, mimo że jest gorsze
            else:
                # delta musi być ujemna!!!
                delta = S_prim - S  # im niższy zysk ma S_prim, tym wyższy jest koszt przyjęcia tego rozwiązania
                r = random.uniform(0, 1)   # losowanie liczby z przedziału (0, 1)

                if r < np.exp(delta / curr_temp):  # jeśli wylosowana liczba jest mniejsza od funkcji chłodzenia
                    S = S_prim                     # przyjmij gorsze rozwiązanie

            # zapamiętywanie najlepszego rozwiązania
            if S.profit > best_result_point[1]:
                best_result_point = (len(way_of_algorithm), S.profit)
                chosen_items = [S.stored_items[i] for i in S.solution]

            way_of_algorithm.append(S.profit)

    final_result = way_of_algorithm[-1]

    return final_result, best_result_point, chosen_items, way_of_algorithm
