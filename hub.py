import routes
from datetime import timedelta
from enum import Enum, auto
from truck import TruckStatus


class ConstraintType(Enum):
    TRUCK = auto()
    GROUPED = auto()


class Hub:
    def __init__(self, drivers_available, address="4001 S 700 E"):
        self.address = address
        self.trucks = []
        self.drivers_available = drivers_available
        self.drivers_delivering = 0
        self.package_list = []
        self.deliverable_packages = []
        self.delayed_packages = []
        self.constrained_packages = []
        self.hub_time = timedelta(hours=8)

    def add_truck(self, truck_id):
        self.trucks.append(truck_id)

    def add_package(self, pkg_id):
        self.package_list.append(pkg_id)

    def add_deliverable_package(self, pkg_id):
        self.deliverable_packages.append(pkg_id)

    def add_delayed_package(self, pkg_id):
        self.delayed_packages.append(pkg_id)

    def add_constrained_package(self, pkg_id, constraint_type):
        self.constrained_packages.append([pkg_id, constraint_type])

    # TODO: Cite
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
        for set in merged_sets:
            for pkg in set:
                if pkg in self.deliverable_packages:
                    self.deliverable_packages.remove(pkg)
                    self.add_constrained_package(pkg, ConstraintType.GROUPED)

        return merged_sets

    def parse_truck_constrained_packages(self, pkg_list, pkg_ht):
        truck_pkgs = []
        truck_pkg_dict = {}

        for id in pkg_list:
            truck_id = pkg_ht.lookup(id).notes.replace("TRUCK - ", "")
            truck_id = int(truck_id)
            truck_pkgs.append([truck_id, id])

        # use a dictionary to merge packages constrained to the same truck
        for t_id, p_id in truck_pkgs:
            if t_id not in truck_pkg_dict:
                truck_pkg_dict[t_id] = [p_id]
            else:
                truck_pkg_dict[t_id].append(p_id)

        merged_pkgs = [[t_id, p_id] for t_id, p_id in truck_pkg_dict.items()]

        return merged_pkgs

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

        return sorted_list

    def load_available_trucks(self, pkg_ht, truck_ht, address_list, distance_list):
        grouped_list = []
        truck_list = []

        # parse any grouping or truck constraints on packages
        for pkg in self.constrained_packages:
            if pkg_ht.lookup(pkg[0]).notes.startswith("GROUPED -"):
                grouped_list.append(pkg[0])
            elif pkg_ht.lookup(pkg[0]).notes.startswith("TRUCK -"):
                truck_list.append(pkg[0])

        group_constrained_packages = self.parse_grouped_packages(grouped_list, pkg_ht)
        truck_constrained_packages = self.parse_truck_constrained_packages(
            truck_list, pkg_ht
        )

        for truck_id in self.trucks:
            curr_truck = truck_ht.lookup(truck_id)

            if self.delayed_packages:
                for id in self.delayed_packages:
                    pkg = pkg_ht.lookup(id)
                    delay_time = pkg.at_hub_time
                    if delay_time > curr_truck.truck_time:
                        self.delayed_packages.remove(id)
                        self.deliverable_packages.append(id)

            if curr_truck.status == TruckStatus.AT_HUB:
                # add constrained packages to trucks
                if group_constrained_packages:
                    for grp in group_constrained_packages:
                        total_cargo = len(grp) + len(curr_truck.packages)

                        if total_cargo <= curr_truck.max_cargo:
                            for pkg in grp:
                                curr_truck.load_package(pkg, pkg_ht)
                            group_constrained_packages.remove(grp)
                        else:
                            print(
                                "This truck is full, this group will be loaded on the next available truck"
                            )

                if truck_constrained_packages:
                    for grp in truck_constrained_packages:
                        total_cargo = len(grp[1]) + len(curr_truck.packages)

                        if grp[0] == truck_id and total_cargo <= curr_truck.max_cargo:
                            for pkg in grp[1]:
                                curr_truck.load_package(pkg, pkg_ht)
                            truck_constrained_packages.remove(grp)
                        elif total_cargo >= curr_truck.max_cargo:
                            print(
                                "This truck is full, this group will be loaded on the next truck with id:",
                                grp[0],
                            )

                temp_pkg_list = []

                if curr_truck.packages:
                    temp_pkg_list.extend(self.deliverable_packages)
                    temp_pkg_list.extend(curr_truck.packages)
                    temp_pkg_list = self.sort_packages(
                        temp_pkg_list, pkg_ht, address_list, distance_list
                    )

                    for pkg in temp_pkg_list:
                        if (
                            pkg not in curr_truck.packages
                            and len(curr_truck.packages) < curr_truck.max_cargo
                        ):
                            curr_truck.load_package(pkg, pkg_ht)
                            self.deliverable_packages.remove(pkg)

                    curr_truck.packages = self.sort_packages(
                        curr_truck.packages, pkg_ht, address_list, distance_list
                    )
                elif self.deliverable_packages:
                    temp_pkg_list.extend(self.deliverable_packages)
                    temp_pkg_list = self.sort_packages(
                        temp_pkg_list, pkg_ht, address_list, distance_list
                    )
                    for pkg in temp_pkg_list:
                        if len(curr_truck.packages) < curr_truck.max_cargo:
                            curr_truck.load_package(pkg, pkg_ht)
                            self.deliverable_packages.remove(pkg)
                else:
                    return

            self.dispatch_truck(truck_id, truck_ht, pkg_ht, address_list, distance_list)

        self.load_available_trucks(pkg_ht, truck_ht, address_list, distance_list)

    def dispatch_truck(self, truck_id, truck_ht, pkg_ht, address_list, distance_list):
        delivered = False
        curr_truck = truck_ht.lookup(truck_id)
        if self.drivers_available > self.drivers_delivering:
            curr_truck.update_status(TruckStatus.LOADED)
            print("Truck", truck_id, "dispatched at", curr_truck.truck_time)
            delivered = curr_truck.deliver_all_packages(
                pkg_ht, address_list, distance_list
            )
            self.drivers_delivering += 1

        if delivered and curr_truck.driver_assigned:
            self.drivers_delivering -= 1
            curr_truck.driver_assigned = False
            if curr_truck.truck_time > self.hub_time:
                self.hub_time = curr_truck.truck_time
            print("Truck", truck_id, "returned at", curr_truck.truck_time)

    def __str__(self):
        return (
            f"------------------------------\n"
            f"Hub Address: {self.address}\n"
            f"Assigned Trucks: {self.trucks}\n"
            f"Drivers Available: {self.drivers_available}\n"
            f"Deliverable Packages: {self.deliverable_packages}\n"
            f"Constrained Packages: {self.constrained_packages}\n"
            f"Delayed Packages: {self.delayed_packages}\n"
            f"------------------------------\n"
        )
