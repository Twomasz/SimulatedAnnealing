import numpy as np

from data_structures import *
"""
zdefiniować obiekt rozwiązania
i dla niego metody porównawcze
i metodę naprawy rozwiązania gdzie bedziemy odrzucac elementy:
- o ujemnej marzy (mało roboty)
- przekroczenie budżetu (jakaś funkcja kary)
- za dużo elementów (wyrzucenie elementow i dodanie ich liczebnosci)


SĄSIEDZTWO
pomysł: rozwiązanie mające 75% budżetu wspólne
jak zbudować sąsiednie rozwiązanie


"""


def SimulatedAnnealing(company: Company, stored_items: List[Item], T_0, T_f, N_max, alpha=0.9):
    S = Solution(company=company, stored_items=stored_items, solution_type='init')

    T = T_0

    while T > T_f:
        i = 0

        S_prim = S.find_adjacency_solution(drop_coeff=0.5)
        print(S_prim.total_profit())

        if S_prim < S:
            S = S_prim

        else:
            delta = S_prim - S
            r = random.uniform(0, 1)
            if r < np.exp(-delta/T):
                S = S_prim

        T = alpha * T

        i += 1
        if i >= N_max:
            break


    return S.total_profit()

