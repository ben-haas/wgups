from enum import Enum, auto
from datetime import timedelta
import routes


class TruckStatus(Enum):
    AT_HUB = auto()
    LOADED = auto()
    DELAYED = auto()
    DELIVERING = auto()
    RETURNING = auto()


class Truck:
    max_cargo = 16
    avg_speed = 18

    def __init__(self, truck_id, max_cargo=max_cargo, avg_speed=avg_speed):
        self.id = truck_id
        self.pkg_id_list = []
        self.driver_id = None
        self.status = TruckStatus.AT_HUB
        self.max_cargo = max_cargo
        self.avg_speed = avg_speed
        self.miles_traveled = 0
        self.time_obj = timedelta(hours=8, minutes=0, seconds=0)
        self.traveled_timestamps = []
        self.route = []
        self.at_hub = True

    def load_package(self, pkg):
        if len(self.pkg_id_list) < self.max_cargo:
            self.pkg_id_list.append(pkg.id)
            pkg.update_truck(self.id)
        else:
            return False

    def assign_driver(self, driver):
        self.driver = driver.id
        driver.assign_truck(self.id)

    def remove_driver(self, driver):
        self.driver = None
        driver.unassign_truck()

    def update_status(self, new_status):
        if isinstance(new_status, TruckStatus):
            self.status = new_status
        else:
            raise ValueError("Invalid Status")

    def update_traveled_miles(self, miles):
        self.miles_traveled += miles

    def deliver_package(self, pkg_id, miles_traveled, time_elapsed):
        self.pkg_id_list.remove(pkg_id)
        # TODO: figure this out

    def calculate_route(self, pkg_id_list, ht, address_list, distance_list):
        if self.status == TruckStatus.LOADED:
            from_address = "4001 S 700 E"
            while len(pkg_id_list) != 0:
                next_address = routes.min_distance_from(
                    from_address, self.pkg_id_list, ht, address_list, distance_list
                )
                self.route.append(next_address)
                pkg_id_list.remove(next_address)
                from_address = next_address
