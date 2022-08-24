import statistics
import time
import csv
import numpy
import pandas as pd
import statistics

start_time = time.time()

with open("test.csv", encoding='utf-8') as r_rile:
    # Создаем объект DirectRider, указываем разделитель ";"
    file_reader = csv.DictReader(r_rile, delimiter=";")
    # Счетчик для подсчета кол-ва строк и вывода заголовков столбцов.
    count = 0
    year = []
    price = []
    mileage = []

    # Считываем данные из csv файла
    for row in file_reader:
        #year = []
        year.append(int(row["Год"]))
        price.append(int(row["Цена в $"]))
        mileage.append(int(row['Пробег'][:-7]))
        #print(year)
        #print(price)
        #print(mileage)
        #year. = row["Год"]
        #year = int(year)
        #av_year = sum(year) / len(year)
        #print(year)

    #return year

    #print(year)
    #print(len(year))
    #print(year)

#df = pd.DataFrame(year)
#res_mean = df.mean()

print(f"Посчитано {len(year)} машин.")
print(f"\n- Средний год производства: {round((sum(year) / len(year)),2)} год.")
print(f"- Средняя цена: {round((sum(price) / len(price)))} $.")
print(f"- Средняя медианная цена: {round(statistics.median(price))} $.")
print(f"- Предний пробег: {round((sum(mileage) / len(mileage)))} тыс км.")


#==================================================
print(f"\nВыполнено за: {time.time() - start_time:,.2f} секунды.")
