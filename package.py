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

    def __str__(self):
        return f"Package {self.id}, {self.address}, {self.city}, {self.state}, {self.zip}, {self.deadline}, {self.weight}, {self.notes}"
