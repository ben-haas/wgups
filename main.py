# Benjamin Haas
# Student ID: 11196046

import routes
from hashtable import HashTable
from truck import Truck
from hub import Hub


pkg_table = HashTable()
truck_table = HashTable()
hub = Hub()

address_list = routes.load_address_data("./data/addresses.csv")
distance_list = routes.load_distance_data("./data/distances.csv")
routes.load_package_data("./data/packages.csv", pkg_table, hub)


def create_trucks(truck_qty):
    t_id = 1
    for id in range(t_id, truck_qty + 1):
        truck = Truck(id)
        hub.add_truck(id)
        truck_table.insert(id, truck)


class Main:
    create_trucks(3)

    print("-------------------------------------------")
    print("Western Governors University Parcel Service")
    print("                   ___")
    print("                  (o,o)")
    print('                 {`""\'}')
    print('                 -"-"-')
    print("-------------------------------------------")
    print()
