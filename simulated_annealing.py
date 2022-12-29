import numpy as np
from data_structures import *


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
    temp_array = [init_temp]

    if version == 'arithmetic':
        for i in range(ages-1):
            temp_array.append(temp_array[i] - cooling_rate)

    elif version == 'geometric':
        for i in range(ages-1):
            temp_array.append(temp_array[i] * cooling_rate)

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
    iter_array = [init_iterations]

    if version == 'constant':
        iter_array = [init_iterations for _ in range(ages)]

    elif version == 'linear':
        coeff = (max_iterations - init_iterations) / (ages - 1)
        for i in range(ages-1):
            iter_array.append(round(iter_array[i] + coeff))

    elif version == 'square':
        x = np.array([1, ages//2, ages])
        y = np.array([init_iterations, (max_iterations - init_iterations) * 0.25, max_iterations])

        p = np.polyfit(x, y, deg=2)  # dopasowanie wielomianu 2 stopnia do 3 punktów w przestrzeni

        for i in range(2, ages+1):
            # wyliczenie i zaokrąglenie wartości wielomianu w i-tym punkcie
            iter_array.append(round(p[0]*i**2 + p[1]*i + p[2]))

    else:
        raise ValueError('Nieprawidłowa nazwa wersji funkcji')

    return iter_array


def SimulatedAnnealing(company: Company, stored_items: List[Item], temp_array: list, iter_array: list):
    """
    Właściwy algorytm symulowanego wyżarzania
    @param company: Klasa firmy nadająca marże
    @param stored_items: Części przechowywane w magazynie
    @param temp_array: Lista temperatur w poszczególnych epokach
    @param iter_array: Lista iteracji w poszczególnych epokach
    @return: Zwraca rozwiązanie końcowe, wybrane elementy oraz 'drogę' rozwiązań, jakie wybrał algorytm
    """
    if len(temp_array) != len(iter_array):   # zabezpieczenie
        raise ValueError('Brak zgodności epok w listach iteracji i temperatury')

    S = Solution(company=company, stored_items=stored_items, solution_type='init', init_ver='uncommon')

    way_of_algorithm = [S.profit]

    for idx, curr_temp in enumerate(temp_array):
        for _ in range(iter_array[idx]):
            # tworzenie nowego rozwiązania sąsiedniego
            S_prim = Solution(company=company, stored_items=S.stored_items, solution_type='adj', adj_ver='random',
                              previous_solution=S.solution, drop_coeff=0.5)

            # jeżeli S_prim okaże się lepszym rozwiązaniem to staje się nowym rozwiązaniem branym pod uwagę
            if S_prim >= S:
                S = S_prim

            # w przeciwnym wypadku delta i prawdopodobieństwo decyduje o przyjęciu tego rozwiązania, mimo że jest gorsze
            else:
                # delta musi być ujemna!!!
                delta = S_prim - S  # im niższy zysk ma S_prim, tym wyższy jest koszt przyjęcia tego rozwiązania
                r = random.uniform(0, 1)   # losowanie liczby z przedziału (0, 1)

                if r < np.exp(delta / curr_temp):  # jeśli wylosowana liczba jest mniejsza od funkcji chłodzenia-przyjmij grosze rozwiązanie
                    S = S_prim

            # TODO: POMYSŁ: rozdzielić way_of_algorithm na listę list, aby było widać rozpoczęcia kolejnych epok
            print(S.profit)
            way_of_algorithm.append(S.profit)

    result = way_of_algorithm[-1]
    S.get_total_profit()
    chosen_items = [S.stored_items[i] for i in S.solution]

    return result, chosen_items, way_of_algorithm
