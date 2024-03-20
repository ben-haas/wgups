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

    def __init__(
        self,
        id,
        depart_time=timedelta(hours=8),
        max_cargo=max_cargo,
        avg_speed=avg_speed,
        hub_address="4001 S 700 E",
    ):
        self.id = id
        self.packages = []
        self.status = TruckStatus.AT_HUB
        self.max_cargo = max_cargo
        self.avg_speed = avg_speed
        self.miles_traveled = 0
        self.depart_time = depart_time
        self.truck_time = depart_time
        self.hub_address = hub_address
        self.traveled_timestamps = []
        self.driver_assigned = False

    def load_package(self, pkg_id, pkg_ht):
        if len(self.packages) < self.max_cargo:
            self.packages.append(pkg_id)
            pkg = pkg_ht.lookup(pkg_id)
            pkg.truck_id = self.id
        else:
            self.update_status(TruckStatus.LOADED)
            raise ValueError("Truck is full")

    def update_status(self, new_status):
        if isinstance(new_status, TruckStatus):
            self.status = new_status
        else:
            raise ValueError("Invalid Status")

    def deliver_package(self, pkg_id, pkg_ht, miles_traveled, time_elapsed):
        self.miles_traveled += miles_traveled
        self.truck_time += time_elapsed
        self.traveled_timestamps.append([self.miles_traveled, self.truck_time])
        pkg = pkg_ht.lookup(pkg_id)
        pkg.update_status(PackageStatus.DELIVERED)
        pkg.update_delivery_time(self.truck_time)

    def return_to_hub(self, current_index, address_list, distance_list):
        hub_index = routes.get_address_index(self.hub_address, address_list)
        return_miles = routes.calc_distance(current_index, hub_index, distance_list)

        self.miles_traveled += return_miles
        self.truck_time += timedelta(hours=(return_miles / self.avg_speed))
        self.traveled_timestamps.append([self.miles_traveled, self.truck_time])
        self.status = TruckStatus.AT_HUB
        self.packages = []

    def deliver_all_packages(self, pkg_ht, address_list, distance_list):
        if self.status == TruckStatus.LOADED:
            self.update_status(TruckStatus.DELIVERING)
            from_index = routes.get_address_index(self.hub_address, address_list)

            for id in self.packages:
                pkg = pkg_ht.lookup(id)
                pkg.update_status(PackageStatus.EN_ROUTE)
                next_index = routes.get_address_index(pkg.address, address_list)
                distance_traveled = routes.calc_distance(
                    from_index, next_index, distance_list
                )

                time_elapsed = timedelta(hours=(distance_traveled / self.avg_speed))
                self.deliver_package(id, pkg_ht, distance_traveled, time_elapsed)
                from_index = routes.get_address_index(pkg.address, address_list)

            self.status = TruckStatus.RETURNING
            self.return_to_hub(from_index, address_list, distance_list)

        return True

    def __str__(self):
        return (
            f"----------------------\n"
            f"ID: {self.id}\n"
            f"Package List: {self.packages}\n"
            f"Status: {self.status}\n"
            f"Miles Traveled: {self.miles_traveled}\n"
            f"Truck Time: {self.truck_time}\n"
            f"----------------------\n"
        )
