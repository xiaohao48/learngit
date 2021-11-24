import csv
import matplotlib.pyplot as plt
from datetime import datetime

filename = 'sitka_weather_07-2018_simple.csv'
with open(filename) as f:
    reader = csv.reader(f)

    header_row = next(reader)
    print(header_row)
    # for readers in reader:
    #     print(readers)
    # for index,colum_header in enumerate(header_row):
    #     print(index,colum_header)

    # highs = [int(row[5]) for row in reader]
    # dates = [datetime.strptime(row[2], "%Y-%m-%d") for row in reader]
    highs, lows, dates = [], [], []
    for row in reader:
        try:
            high = int(row[5])
            low = int(row[6])
            current_date = datetime.strptime(row[2], "%Y-%m-%d")
        except ValueError:
            print(row[2], "missing data")
        else:
            highs.append(high)
            dates.append(current_date)
            lows.append(low)
    # x = list(range(0, len(highs)))
    fig = plt.figure(dpi=128)
    plt.plot(dates, highs, c='red')
    plt.plot(dates, lows, c='blue')
    plt.fill_between(dates, highs, lows, facecolor='green', alpha=0.1)
    fig.autofmt_xdate()
    plt.show()
