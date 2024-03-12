# Benjamin Haas Student ID: 11196046

import csv
import routes
from package import Package
from hashtable import HashTable
from truck import Truck
from driver import Driver


class Main:
    pkg_table = HashTable()

    address_list = routes.load_address_data()
    distance_list = routes.load_distance_data()

    truck_1 = Truck(1)
    truck_2 = Truck(2)
    truck_3 = Truck(3)

    driver_1 = Driver(1)
    driver_2 = Driver(2)

    with open(
        "./data/packages.csv", mode="r", encoding="utf-8-sig", newline=""
    ) as file:
        reader = csv.reader(file)
        for row in reader:
            pkg = Package(row)
            pkg_table.insert(pkg.id, pkg)

    # Pre-load packages with constraints
    truck_2_constraint = [3, 18, 36, 39]
    delayed_constraint = [6, 9, 25, 28, 32]
    grouped_constraint = [13, 14, 15, 16, 19]
