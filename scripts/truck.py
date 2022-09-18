from scripts.utils import Time


# Truck class to add truck objects to store packages in
class Truck:
    # initialize truck object
    def __init__(self, hrs, mins, number):
        self.packages = []
        self.current_location = ''
        self.distance_traveled = 0.0
        self.speed = 18
        self.time = Time(hrs, mins)
        self.number = number

    # add a package to the truck
    def add_package(self, pkg):
        self.packages.append(pkg)

    # add distance to truck
    def add_distance(self, dist):
        self.distance_traveled = self.distance_traveled + dist

    # get the truck distance traveled
    def get_distance(self):
        return self.distance_traveled

    # get the packages that are on the truck
    def get_packages(self):
        return self.packages

    # get the travel time of the truck
    def get_travel_time(self, dist):
        return dist / (self.speed / 60)

    # get the truck number
    def get_number(self):
        return self.number
