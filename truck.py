from enum import Enum, auto
from datetime import timedelta
from package import PackageStatus
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
        self.at_hub = True
        self.hub_address = "4001 S 700 E"

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

    def deliver_package(self, pkg_id, ht, miles_traveled, time_elapsed):
        self.miles_traveled += miles_traveled
        self.time_obj += time_elapsed
        self.traveled_timestamps.append([self.miles_traveled, self.time_obj])
        pkg = ht.lookup(pkg_id)
        pkg.update_status(PackageStatus.DELIVERED)
        self.pkg_id_list.remove(pkg_id)

    def return_to_hub(self, current_address, address_list, distance_list):
        hub_index = routes.get_address_index(self.hub_address, address_list)
        last_index = routes.get_address_index(current_address, address_list)
        return_miles = routes.calc_distance(last_index, hub_index, distance_list)

        self.miles_traveled += return_miles
        self.time_obj += timedelta(minutes=(return_miles / self.avg_speed * 60))
        self.traveled_timestamps.append([self.miles_traveled, self.time_obj])
        self.status = TruckStatus.AT_HUB

    def deliver_all_packages(self, ht, address_list, distance_list):
        if self.status == TruckStatus.LOADED:
            self.update_status(TruckStatus.DELIVERING)
            from_address = self.hub_address
            while len(self.pkg_id_list) != 0:
                next_stop = routes.min_distance_from(
                    from_address, self.pkg_id_list, ht, address_list, distance_list
                )

                time_elapsed = timedelta(minutes=(next_stop[1] / self.avg_speed * 60))
                self.deliver_package(next_stop[0], ht, next_stop[1], time_elapsed)
                from_address = next_stop[2]

            self.return_to_hub(from_address, address_list, distance_list)
