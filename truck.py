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
        self.pkg_list = []
        self.status = TruckStatus.AT_HUB
        self.max_cargo = max_cargo
        self.avg_speed = avg_speed
        self.miles_traveled = 0
        self.depart_time = depart_time
        self.truck_time = depart_time
        self.hub_address = hub_address
        self.traveled_timestamps = []

    def load_packages(self, pkg_id_list, ht):
        for id in pkg_id_list:
            if len(self.pkg_list) < self.max_cargo:
                self.pkg_list.append(id)
                pkg = ht.lookup(id)
                pkg.truck_id = self.id
                self.status = TruckStatus.LOADED
            else:
                raise ValueError("Truck is full")

    def update_status(self, new_status):
        if isinstance(new_status, TruckStatus):
            self.status = new_status
        else:
            raise ValueError("Invalid Status")

    def deliver_package(self, pkg_id, ht, miles_traveled, time_elapsed):
        self.miles_traveled += miles_traveled
        self.truck_time += time_elapsed
        self.traveled_timestamps.append([self.miles_traveled, self.truck_time])
        pkg = ht.lookup(pkg_id)
        pkg.update_status(PackageStatus.DELIVERED)
        self.pkg_list.remove(pkg_id)

    def return_to_hub(self, current_address, address_list, distance_list):
        hub_index = routes.get_address_index(self.hub_address, address_list)
        last_index = routes.get_address_index(current_address, address_list)
        return_miles = routes.calc_distance(last_index, hub_index, distance_list)

        self.miles_traveled += return_miles
        self.truck_time += timedelta(hours=(return_miles / self.avg_speed))
        self.traveled_timestamps.append([self.miles_traveled, self.truck_time])
        self.status = TruckStatus.AT_HUB

    def deliver_all_packages(self, ht, address_list, distance_list):
        if self.status == TruckStatus.LOADED:
            self.update_status(TruckStatus.DELIVERING)
            for id in self.pkg_list:
                ht.lookup(id).update_status(PackageStatus.EN_ROUTE)
            from_address = self.hub_address

            while len(self.pkg_list) > 0:
                next_stop = routes.find_next_stop(
                    from_address, self.pkg_list, ht, address_list, distance_list
                )

                time_elapsed = timedelta(hours=(next_stop[0] / self.avg_speed))
                self.deliver_package(next_stop[1], ht, next_stop[0], time_elapsed)
                from_address = ht.lookup(next_stop[1]).address

            self.status = TruckStatus.RETURNING
            self.return_to_hub(from_address, address_list, distance_list)

    def __str__(self):
        return (
            f"----------------------\n"
            f"ID: {self.id}\n"
            f"Package List: {self.pkg_list}\n"
            f"Status: {self.status}\n"
            f"Miles Traveled: {self.miles_traveled}\n"
            f"Truck Time: {self.truck_time}\n"
            f"----------------------\n"
        )
