import csv


def load_distance_data():
    with open(
        "./data/distances.csv", mode="r", encoding="utf-8-sig", newline=""
    ) as file:
        reader = csv.reader(file)
        distance_matrix = []
        temp_row = []
        for row in reader:
            temp_row = []
            for dist in row:
                if dist != "":
                    temp_row.append(float(dist))
                else:
                    temp_row.append(False)
            distance_matrix.append(temp_row)

        return distance_matrix


def load_address_data():
    with open(
        "./data/addresses.csv", mode="r", encoding="utf-8-sig", newline=""
    ) as file:
        reader = csv.reader(file)
        address_list = []
        for row in reader:
            address_list.append(row)

        return address_list


def get_address_index(address, address_list):
    idx = 0

    for row in address_list:
        if address in row:
            idx = address_list.index(row)

    return idx


def calc_distance(idx_1, idx_2, distance_list):
    if distance_list[idx_1][idx_2]:
        return distance_list[idx_1][idx_2]
    else:
        return distance_list[idx_2][idx_1]


def min_distance_from(from_address, truck_pkg_id_list, ht, address_list, distance_list):
    min_distance = float("inf")
    min_address = None
    from_index = get_address_index(from_address, address_list)

    for id in truck_pkg_id_list:
        address = ht.lookup(id).address

        if from_address != address:
            dist = calc_distance(
                from_index, get_address_index(address, address_list), distance_list
            )
            if dist < min_distance:
                min_distance = dist
                min_address = address

    return min_address
