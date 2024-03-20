import csv
import datetime
from hub import ConstraintType
from package import Package, PackageStatus


def load_package_data(csv_file, pkg_table, hub):
    with open(csv_file, mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file)

        for row in reader:
            deadline = None
            if row[5] == "EOD":
                deadline = datetime.timedelta(hours=17)
            else:
                if len(row[5]) == 4:
                    deadline = datetime.timedelta(
                        hours=int(row[5][:2]), minutes=int(row[5][-2:])
                    )
                else:
                    deadline = datetime.timedelta(
                        hours=int(row[5][:1]), minutes=int(row[5][-2:])
                    )

            pkg = Package(
                int(row[0]),
                row[1],
                row[2],
                row[3],
                row[4],
                deadline,
                int(row[6]),
                row[7],
            )

            hub.add_package(pkg.id)

            if "DELAYED" in pkg.notes:
                pkg.update_status(PackageStatus.DELAYED)

                time = pkg.notes[-4:]
                hours = int(time[:2].strip())
                minutes = int(time[-2:].strip())
                pkg.at_hub_time = datetime.timedelta(hours=hours, minutes=minutes)

                hub.add_delayed_package(pkg.id)
            elif "ADDRESS_ISSUE" in pkg.notes:
                pkg.update_status(PackageStatus.DELAYED)

                time = pkg.notes[-4:]
                hours = int(time[:2].strip())
                minutes = int(time[-2:].strip())
                pkg.at_hub_time = datetime.timedelta(hours=hours, minutes=minutes)

                hub.add_delayed_package(pkg.id)
            elif "TRUCK" in pkg.notes:
                pkg.update_status(PackageStatus.CONSTRAINED)
                hub.add_constrained_package(pkg.id, ConstraintType.TRUCK)
            elif "GROUPED" in pkg.notes:
                pkg.update_status(PackageStatus.CONSTRAINED)
                hub.add_constrained_package(pkg.id, ConstraintType.GROUPED)
            else:
                hub.add_deliverable_package(pkg.id)

            pkg_table.insert(pkg.id, pkg)


def load_distance_data(csv_file):
    with open(csv_file, mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file)
        distances = list(reader)

        return distances


def load_address_data(csv_file):
    with open(csv_file, mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file)
        address_list = list(reader)

        return address_list


def get_address_index(address, address_list):
    idx = 0

    for row in address_list:
        if address in row:
            idx = address_list.index(row)

    return idx


def calc_distance(idx_1, idx_2, distance_list):
    if distance_list[idx_1][idx_2] != "":
        return round(float(distance_list[idx_1][idx_2]), 2)
    else:
        return round(float(distance_list[idx_2][idx_1]), 2)


def find_next_stop(from_address, pkg_list, ht, address_list, distance_list):
    min_distance = float("inf")
    next_pkg = None
    from_index = get_address_index(from_address, address_list)

    if len(pkg_list) == 1:
        return pkg_list[0]

    for id in pkg_list:
        address = ht.lookup(id).address

        if from_address != address:
            dist = calc_distance(
                from_index, get_address_index(address, address_list), distance_list
            )
            if dist <= min_distance:
                min_distance = dist
                next_pkg = id

    return next_pkg
