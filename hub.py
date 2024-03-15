import routes
from datetime import timedelta
from enum import Enum, auto
from package import PackageStatus


class ConstraintType(Enum):
    TRUCK = auto()
    GROUPED = auto()


class Hub:
    def __init__(self, drivers_available, address="4001 S 700 E"):
        self.address = address
        self.trucks = []
        self.drivers_available = drivers_available
        self.drivers_delivering = 0
        self.deliverable_packages = []
        self.delayed_packages = []
        self.constrained_packages = []
        self.hub_time = timedelta(hours=8)

    def add_truck(self, truck_id):
        self.trucks.append(truck_id)

    def add_deliverable_package(self, pkg_id):
        self.deliverable_packages.append(pkg_id)

    def add_delayed_package(self, pkg_id):
        self.delayed_packages.append(pkg_id)

    def add_constrained_package(self, pkg_id, constraint_type, constraint):
        self.constrained_packages.append([pkg_id, constraint_type, constraint])

    def update_hub_time(self, hours, minutes=0, seconds=0):
        self.hub_time = timedelta(hours=hours, minutes=minutes, seconds=seconds)

    def update_delayed_status(self, ht):
        for id in self.delayed_packages:
            pkg = ht.lookup(id)

            if pkg.at_hub_time >= self.hub_time:
                pkg.update_status(PackageStatus.AT_HUB)
                self.delayed_packages.remove(id)
                self.deliverable_packages.append(id)

    def load_available_trucks(self, pkg_ht, address_list, distance_list):
        temp_list = self.deliverable_packages
        sorted_list = []
        from_address = self.address
        while len(temp_list) > 0:
            next_stop = routes.find_next_stop(
                from_address,
                temp_list,
                pkg_ht,
                address_list,
                distance_list,
            )
            from_address = pkg_ht.lookup(next_stop).address
            temp_list.remove(next_stop)
            sorted_list.append(next_stop)

        print(sorted_list)
        print(
            len(sorted_list)
            + len(self.delayed_packages)
            + len(self.constrained_packages)
        )

    def __str__(self):
        return (
            f"------------------------------\n"
            f"Hub Address: {self.address}\n"
            f"Assigned Trucks: {self.trucks}\n"
            f"Drivers Available: {self.drivers_available}\n"
            f"Deliverable Packages: {self.deliverable_packages}\n"
            f"Constrained Packages: {self.constrained_packages}\n"
            f"Delayed Packages: {self.delayed_packages}\n"
            f"Hub Time: {self.hub_time}\n"
            f"------------------------------\n"
        )
