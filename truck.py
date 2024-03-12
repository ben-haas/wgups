from enum import Enum, auto

PACKAGES_MAX = 16
SPEED_MAX = 18


class TruckStatus(Enum):
    EMPTY = auto()
    DELIVERING = auto()
    RETURNING = auto()
    LOADED = auto()


class Truck:
    def __init__(self, id):
        self.truck_id = id
        self.packages = []
        self.package_count = 0
        self.traveled_miles = 0
        self.driver = "None"
        self.status = TruckStatus.EMPTY

    def load_package(self, pkg):
        if self.package_count <= PACKAGES_MAX:
            self.packages.append(pkg)
            self.package_count += 1
        else:
            print("The truck is full!")

    def update_driver(self, driver):
        self.driver = driver

    def update_status(self, new_status):
        if isinstance(new_status, TruckStatus):
            self.status = new_status
        else:
            raise ValueError("Invalid Status")

    def update_traveled_miles(self, miles):
        self.traveled_miles += miles
