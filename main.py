# Benjamin Haas Student ID: 11196046

import csv
import datetime

from hashtable import HashTable
from package import Package, PackageStatus
import routes
from truck import Truck

pkg_table = HashTable()

address_list = routes.load_address_data("./data/addresses.csv")
distance_list = routes.load_distance_data("./data/distances.csv")

t1 = Truck(1)
t2 = Truck(2)
t3 = Truck(3)


def load_trucks():
    t1.load_packages([1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40], pkg_table)
    t2.load_packages(
        [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39], pkg_table
    )
    t3.load_packages([2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33], pkg_table)


def deliver_packages():
    t1.deliver_all_packages(pkg_table, address_list, distance_list)
    t2.deliver_all_packages(pkg_table, address_list, distance_list)
    t3.deliver_all_packages(pkg_table, address_list, distance_list)


def load_package_data(csv_file):
    with open(csv_file, mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file)

        for row in reader:
            deadline = None
            if row[5] == "EOD":
                deadline = datetime.timedelta(hours=17)
            else:
                if len(row[5]) == 4:
                    deadline = datetime.timedelta(
                        hours=int(row[5][:2]), minutes=int(row[5][-2:])
                    )
                else:
                    deadline = datetime.timedelta(
                        hours=int(row[5][:1]), minutes=int(row[5][-2:])
                    )

            pkg = Package(
                int(row[0]),
                row[1],
                row[2],
                row[3],
                row[4],
                deadline,
                int(row[6]),
                row[7],
            )

            if "Delayed" in pkg.notes:
                pkg.update_status(PackageStatus.DELAYED)
            elif "Wrong address" in pkg.notes:
                pkg.update_status(PackageStatus.DELAYED)

            pkg_table.insert(pkg.id, pkg)


# Pre-load packages with constraints
truck_2_constraint = [3, 18, 36, 39]
delayed_constraint = [6, 9, 25, 28, 32]
grouped_constraint = [13, 14, 15, 16, 19]


class Main:
    load_package_data("./data/packages.csv")
    load_trucks()
    deliver_packages()
    print(t1.traveled_timestamps)
    print("-------------------------------------------")
    print("Western Governors University Parcel Service")
    print("                   ___")
    print("                  (o,o)")
    print('                 {`""\'}')
    print('                 -"-"-')
    print("-------------------------------------------")
    print()
    print(
        "The total distance traveled by all trucks is",
        t1.miles_traveled + t2.miles_traveled + t3.miles_traveled,
        "miles.",
    )
