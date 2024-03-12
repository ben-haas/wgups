class Driver:
    def __init__(self, driver_id):
        self.driver_id = driver_id
        self.assigned_truck_id = None

    def assign_truck(self, truck_id):
        self.assigned_truck_id = truck_id

    def unassign_truck(self):
        self.assigned_truck_id = None
