from datetime import timedelta

from package import PackageStatus


class Hub:
    def __init__(self, address="4001 S 700 E"):
        self.address = address
        self.trucks = []
        self.deliverable_packages = []
        self.delayed_packages = []
        self.hub_time = timedelta(hours=7)

    def add_truck(self, truck):
        self.trucks.append(truck)

    def add_deliverable_package(self, pkg_id):
        self.deliverable_packages.append(pkg_id)

    def add_delayed_package(self, pkg_id):
        self.delayed_packages.append(pkg_id)

    def update_hub_time(self, hours, minutes=0, seconds=0):
        self.hub_time = timedelta(hours=hours, minutes=minutes, seconds=seconds)

    def update_delayed_status(self, ht):
        for id in self.delayed_packages:
            pkg = ht.lookup(id)

            if pkg.at_hub_time >= self.hub_time:
                pkg.update_status(PackageStatus.AT_HUB)
                self.delayed_packages.remove(id)
                self.deliverable_packages.append(id)
