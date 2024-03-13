import csv


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
        return [0, pkg_list[0]]

    for id in pkg_list:
        address = ht.lookup(id).address

        if from_address != address:
            dist = calc_distance(
                from_index, get_address_index(address, address_list), distance_list
            )
            if dist <= min_distance:
                min_distance = dist
                next_pkg = id

    return [min_distance, next_pkg]
