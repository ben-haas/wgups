import csv

with open("./data/packages.csv", mode="r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

with open("./data/addresses.csv", mode="r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

with open("./data/distances.csv", mode="r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
