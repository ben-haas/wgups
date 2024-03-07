import csv
from package import Package

with open("./data/packages.csv", mode="r") as file:
    reader = csv.reader(file)
    for row in reader:
        Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        print(Package)
with open("./data/addresses.csv", mode="r") as file:
    reader = csv.reader(file)

with open("./data/distances.csv", mode="r") as file:
    reader = csv.reader(file)
