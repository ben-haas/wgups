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

    def merge_grouped_packages(self, pkg_sets):
        # convert the list of lists to a list of sets
        pkg_sets = [set(pkgs) for pkgs in pkg_sets]
        merged = True

        while merged:
            merged = False
            for i in range(len(pkg_sets)):
                for j in range(i + 1, len(pkg_sets)):
                    # If 2 sets overlap, merge them
                    # isdisjoint() is False if at least one element is common to both sets
                    if not pkg_sets[i].isdisjoint(pkg_sets[j]):
                        # Union to merge the sets
                        pkg_sets[i] |= pkg_sets[j]
                        # Empty the set that was merged into the other set
                        pkg_sets[j] = set()
                        merged = True

            # remove any empty sets by checking each one for a truthy value
            pkg_sets = [s for s in pkg_sets if s]

        # convert the sets back to lists
        return [list(s) for s in pkg_sets]

    def parse_grouped_packages(self, pkg_list, pkg_ht):
        pkg_sets = []
        for id in pkg_list:
            grouped_ids = pkg_ht.lookup(id).notes.replace("GROUPED -", "").split("+")
            grouped_ids.append(id)
            int_list = [int(id) for id in grouped_ids]

            pkg_sets.append(int_list)

        merged_sets = self.merge_grouped_packages(pkg_sets)
        print(merged_sets)

        return merged_sets

    def sort_packages(self, pkg_list, pkg_ht, address_list, distance_list):

        temp_list = pkg_list
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

    def load_available_trucks(self, pkg_ht, truck_ht, address_list, distance_list):
        grouped_list = []
        for pkg in self.constrained_packages:
            if pkg_ht.lookup(pkg[0]).notes.startswith("GROUPED -"):
                grouped_list.append(pkg[0])
        self.parse_grouped_packages(grouped_list, pkg_ht)

    def dispatch_truck(self, truck_id, truck_ht):
        # TODO: trigger truck delivery
        print("Deliver Packages on Truck", truck_id)

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
