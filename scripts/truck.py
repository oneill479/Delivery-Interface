from scripts.utils import Time


class Truck:
    def __init__(self, hrs, mins, number):
        self.packages = []
        self.current_location = ''
        self.distance_traveled = 0.0
        self.speed = 18
        self.time = Time(hrs, mins)
        self.number = number

    def add_package(self, pkg):
        self.packages.append(pkg)

    def add_distance(self, dist):
        self.distance_traveled = self.distance_traveled + dist

    def get_distance(self):
        return self.distance_traveled

    def get_packages(self):
        return self.packages

    def get_travel_time(self, dist):
        return dist / (self.speed / 60)

    def get_number(self):
        return self.number
