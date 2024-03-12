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


def calc_distance(address1, address2):
    addresses = load_address_data()
    distances = load_distance_data()
    index_1 = 0
    index_2 = 0

    for row in addresses:
        if address1 in row:
            index_1 = addresses.index(row)
        if address2 in row:
            index_2 = addresses.index(row)

    if distances[index_1][index_2]:
        return distances[index_1][index_2]
    else:
        return distances[index_2][index_1]
