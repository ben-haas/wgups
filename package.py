from enum import Enum, auto


class PackageStatus(Enum):
    AT_HUB = auto()
    EN_ROUTE = auto()
    DELIVERED = auto()
    DELAYED = auto()


class Package:
    def __init__(self, id, address, city, state, zip, deadline, weight, notes):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = PackageStatus.AT_HUB
        self.truck_id = None
        self.delivery_time = None
        self.en_route_time = None

    def update_status(self, new_status):
        if isinstance(new_status, PackageStatus):
            self.status = new_status
        else:
            raise ValueError("Invalid Status")

    def update_delivery_time(self, delivery_time):
        self.delivery_time = delivery_time

    def update_en_route_time(self, en_route_time):
        self.en_route_time = en_route_time
