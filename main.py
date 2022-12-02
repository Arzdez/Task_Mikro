import numpy as np
import matplotlib.pyplot as plt
from gsf_read import gsf_read
from scipy import interpolate


# Функция закрашивания артефактов
def smothi(data_Bad):
    # Массив средним значений пикселя по строкам и расчёт этих значений
    sdvig_data = []

    for i in range(len(data_Bad) - 1):
        tmp = 0
        for j in range(len(data_Bad)):
            tmp += data_Bad[i][j] - data_Bad[i + 1][j]

        sdvig_data.append(tmp)

    # расчёт матожидания
    means = np.std(sdvig_data)**2

    # Поиск артефактов за основу взято матожидание, если отличие между средними значениями яркости пикселя выше медианы то вырезаем участок и заменяем средним между рядомстоящими
    for i in range(len(sdvig_data) - 1):
        if abs(sdvig_data[i] - sdvig_data[i + 1]) > means:
            for j in range(len(sdvig_data)):
                data_Bad[i][j] = (data_Bad[i - 1][j] + data_Bad[i + 1][j]) / 2

    return data_Bad


# Функция замены пикселей, но унжно цветовую гамму и сдвиг отработать
def change_pixel(data_Bad, data_good):

    sdvig_data = []

    for i in range(len(data_Bad) - 1):
        tmp = 0
        for j in range(len(data_Bad)):
            tmp += data_Bad[i][j] - data_Bad[i + 1][j]

        sdvig_data.append(tmp)

    # Расчёт медианного значения разности
    means = np.std(sdvig_data) * 5

    for i in range(len(sdvig_data) - 1):
        if abs(sdvig_data[i] - sdvig_data[i + 1]) > means:
            for j in range(len(sdvig_data)):
                data_Bad[i][j] = data_good[i][j]

    return data_Bad


# Функция сглаживания по более широкому окну, тестовый вариант
# w - окно сравнения
def sdvig(data_Bad, w):

    # Поиск артефактов за основу взято матожидание, если отличие между средними значениями яркости пикселя выше медианы то вырезаем участок и заменяем средним между рядомстоящими
    for i in range(w, len(data_Bad) - w):
        tmp_mean = 0
        mean_mass = []

        for k in range(i - w, i + w):
            for j in range(len(data_Bad)):
                tmp_mean += data_Bad[k][j] - data_Bad[k + 1][j]

            mean_mass.append(tmp_mean)

        means = np.std(mean_mass)

        for z in range(len(mean_mass) - 1):
            if abs(mean_mass[z] - mean_mass[z + 1]) > means:
                for j2 in range(len(data_Bad)):
                    data_Bad[i][j2] = (data_Bad[i - 1][j2] + data_Bad[i + 1][j2]) / 2

    return data_Bad


if __name__ == "__main__":
    # Окно для тестового метода
    W = 5
    # Загрузка данных указать пути
    (meta_Bad, data_Bads) = gsf_read(
        "C:\\Users\\insec\\Desktop\\Задача браташова\\Data\\bad.gsf"
    )

    (meta_good, data_good) = gsf_read(
        "C:\\Users\\insec\\Desktop\\Задача браташова\\Data\\notbad.gsf"
    )

    # Выходной массив неизменяемый, потому создаём копию временный костыль пока не разобрались форматом до конца
    data_Badk = np.zeros(np.shape(data_Bads))

    for i in range(len(data_Badk)):
        for j in range(len(data_Badk)):
            data_Badk[i][j] = data_Bads[i][j]

    # прмиеняем метод
    '''
    # data_goode = sdvig(data_Badk,20)

    # data_goode = sdvig(data_Badk, w)
    # data_goode2 = test2(data_Badk)
    # data_goode3 = change_pixel(data_goode2, data_good)
    # data_goode4 = data_goode = test2(data_goode3)
    '''
    
    # графики

    plt.subplot(2, 1, 1)
    plt.title("Исходный вариант")
    plt.imshow(data_Bads, cmap="magma")
    """
    plt.subplot(3, 1, 2)
    plt.title("Хорошее изображение} ")
    plt.imshow(data_good,cmap="magma")
    """
    plt.subplot(2, 1, 2)
    plt.title("исправленное")
    plt.imshow(data_goode2, cmap="magma")
    plt.show()
