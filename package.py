from enum import Enum, auto
from datetime import timedelta


class PackageStatus(Enum):
    AT_HUB = auto()
    EN_ROUTE = auto()
    DELIVERED = auto()
    DELAYED = auto()


class Package:
    def __init__(
        self,
        id,
        address,
        city,
        state,
        zip,
        deadline,
        weight,
        notes,
        at_hub_time=timedelta(hours=7),
    ):
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
        self.at_hub_time = at_hub_time
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

    def __str__(self):
        return (
            f"------------------------------------\n"
            f"Package ID: {self.id}\n"
            f"Address: {self.address}, {self.city}, {self.state} {self.zip}\n"
            f"Deadline: {self.deadline}\n"
            f"Weight: {self.weight}\n"
            f"Notes: {self.notes}\n"
            f"Status: {self.status.name}\n"
            f"Truck ID: {self.truck_id if self.truck_id is not None else 'N/A'}\n"
            f"At Hub Time: {self.at_hub_time}\n"
            f"Delivery Time: {self.delivery_time if self.delivery_time is not None else 'N/A'}\n"
            f"En Route Time: {self.en_route_time if self.en_route_time is not None else 'N/A'}\n"
            f"------------------------------------\n"
        )
