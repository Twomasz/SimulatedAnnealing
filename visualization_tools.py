import matplotlib.pyplot as plt
from data_structures import *
import pandas as pd


def print_selected_items(selected_items):
    for item in selected_items:
        print(item)


def fill_warehouse(warehouse: Warehouse, path_to_items_list: str):
    df = pd.read_csv(path_to_items_list)

    for i in range(df.shape[0]):
        info = df.iloc[i]
        name = info['Marka'] + ' ' + info['Model'] + ' ' + info['Nazwa części']
        item = Item(name, info['Cena zakupu [zł]'])
        item.update_market_info(info['Średnia cena rynkowa'], info['Ilość aukcji na rynku'], info['Popyt'])

        warehouse.add_item(item)


def plot_algorithm(way_of_algorithm, best_point, iteration_list):
    plt.figure(figsize=(12, 5))
    plt.scatter(best_point[0], best_point[1], s=100, marker='o', c='orange')

    plt.plot(way_of_algorithm)
    plt.title('Wyniki działania algorytmu w kolejnych iteracjach')
    plt.xlabel('Numer iteracji')
    plt.ylabel('Zysk (Funkcja celu)')

    xline = 0
    for iters_in_age in iteration_list:
        plt.axvline(x=xline, color='red')
        xline += iters_in_age

    plt.legend(['Najlepsze rozwiązanie', 'Droga algorytmu', 'Początek kolejnych epok'])
    plt.show()


def plot_temperature_and_iterations(temperature_list, iteration_list):
    ages = range(1, len(temperature_list)+1)

    plt.figure(figsize=(12, 3))
    plt.subplot(1, 2, 1)
    plt.plot(ages, temperature_list, '-p', color='gray', mfc='blue', mec='blue', markersize=10)
    plt.title('Wartość temperatury w kolejnych epokach')
    plt.xlabel('Epoki')
    plt.ylabel('Wartość temperatury')
    plt.xticks(ages)
    plt.grid()

    plt.subplot(1, 2, 2)
    plt.plot(ages, iteration_list, '-p', color='gray', mfc='orange', mec='orange', markersize=10)
    plt.title('Liczba iteracji w kolejnych epokach')
    plt.xlabel('Epoki')
    plt.ylabel('Liczba iteracji')
    plt.xticks(ages)
    plt.grid()

    plt.show()


def plot_temps_versions(arithmetic_function: list, geometric_function: list):
    plt.figure(figsize=(12, 3))
    ages = range(1, len(arithmetic_function)+1)
    plt.subplot(1, 2, 1)
    plt.plot(ages, arithmetic_function, '-p', color='gray', mfc='blue', mec='blue', markersize=10)
    plt.title('Liniowy spadek temperatury')
    plt.ylabel('Wartość temperatury')
    plt.xlabel('Epoki')
    plt.xticks(ages)
    plt.grid()

    ages = range(1, len(geometric_function)+1)
    plt.subplot(1, 2, 2)
    plt.plot(ages, geometric_function, '-p', color='gray', mfc='orange', mec='orange', markersize=10)
    plt.title('Nieliniowy spadek temperatury')
    plt.ylabel('Wartość temperatury')
    plt.xlabel('Epoki')
    plt.xticks(ages)
    plt.grid()

    plt.show()


def plot_iters_versions(constant_function: list, linear_function: list, square_function: list):
    plt.figure(figsize=(12, 3))
    ages = range(1, len(constant_function) + 1)
    plt.subplot(1, 3, 1)
    plt.plot(ages, constant_function, '-p', color='gray', mfc='green', mec='green', markersize=10)
    plt.title('Stała liczba iteracji')
    plt.ylabel('Wartość temperatury')
    plt.xlabel('Epoki')
    plt.xticks(ages)
    plt.grid()

    ages = range(1, len(linear_function)+1)
    plt.subplot(1, 3, 2)
    plt.plot(ages, linear_function, '-p', color='gray', mfc='blue', mec='blue', markersize=10)
    plt.title('Liniowy wzrost iteracji')
    plt.ylabel('Wartość temperatury')
    plt.xlabel('Epoki')
    plt.xticks(ages)
    plt.grid()

    ages = range(1, len(square_function)+1)
    plt.subplot(1, 3, 3)
    plt.plot(ages, square_function, '-p', color='gray', mfc='orange', mec='orange', markersize=10)
    plt.title('Kwadratowy wzrost iteracji')
    plt.ylabel('Wartość temperatury')
    plt.xlabel('Epoki')
    plt.xticks(ages)
    plt.grid()

    plt.show()
