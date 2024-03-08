import csv
from package import Package

with open("./data/packages.csv", mode="r", encoding="utf-8-sig", newline="") as file:
    reader = csv.reader(file)
    for row in reader:
        Package(row)

with open("./data/addresses.csv", mode="r") as file:
    reader = csv.reader(file)

with open("./data/distances.csv", mode="r") as file:
    reader = csv.reader(file)
