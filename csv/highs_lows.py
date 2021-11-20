import csv
import matplotlib.pyplot as plt

filename = 'sitka_weather_07-2018_simple.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)

    # for index,colum_header in enumerate(header_row):
    #     print(index,colum_header)

    highs = [int(row[5]) for row in reader]
    # for row in reader:
    #     highs.append(row[5])

    print(highs)
    x = list(range(0, len(highs)))
    plt.plot(highs)
    plt.show()
