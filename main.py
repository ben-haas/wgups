# Benjamin Haas Student ID: 11196046

import csv
from package import Package
from hashtable import HashTable


class Main:
    ht = HashTable()

    with open(
        "./data/packages.csv", mode="r", encoding="utf-8-sig", newline=""
    ) as file:
        reader = csv.reader(file)
        for row in reader:
            pkg = Package(row)
            ht.insert(pkg.id, pkg)
            print(ht.lookup(pkg.id))
