from enum import Enum, auto


class PackageStatus(Enum):
    AT_HUB = auto()
    EN_ROUTE = auto()
    DELIVERED = auto()
    DELAYED = auto()


class Package:
    def __init__(self, pkg):
        self.id = int(pkg[0])
        self.address = pkg[1]
        self.city = pkg[2]
        self.state = pkg[3]
        self.zip = pkg[4]
        self.deadline = pkg[5]
        self.weight = int(pkg[6])
        self.notes = pkg[7]
        self.status = PackageStatus.AT_HUB
        self.location = "Hub: 4001 S 700 E"

    def update_status(self, new_status):
        if isinstance(new_status, PackageStatus):
            self.status = new_status
        else:
            raise ValueError("Invalid Status")

    def update_location(self, new_location):
        self.location = new_location

    def __str__(self):
        return f"Package {self.id} is at {self.location} and scheduled for delivery to {self.address} by {self.deadline}."
