# Caleb O'Neill
# Student ID: 001092382

import csv
import enum
import time
from datetime import timedelta

# global distances to be used
dist_matrix = []


# package status
class Status(enum.Enum):
    AT_HUB = 1
    EN_ROUTE = 2
    DELIVERED = 3


# colors for print-outs
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = Blue = '\033[94m'
    GREY = '\033[90m'
    DEFAULT = '\033[0m'


# PART E.
# Develop a hash table, without using any additional libraries or classes,
# that has an insertion function that takes the following components as input
# and inserts the components into the hash table.


class HashTable:
    def __init__(self, init_capacity=10):
        self.table = []
        for i in range(init_capacity):
            self.table.append([])

    # insert function for package object
    def insert(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for obj in bucket_list:
            if obj[0] == key:
                obj[1] = item
                return True

        key_list = [key, item]
        bucket_list.append(key_list)

        return True

    # PART F.
    # Develop a look-up function that takes the following components as input
    # and returns the corresponding data elements:

    # search function for package object
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for key_list in bucket_list:
            if key_list[0] == key:
                return key_list[1]

        return None

    # search function for package object
    def update(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for key_list in bucket_list:
            if key_list[0] == key:
                return key_list[1]

        return None

    # remove function for package object
    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # remove the item from the bucket list if it is present.
        for key_list in bucket_list:
            if key_list[0] == key:
                bucket_list.remove([key_list[0], key_list[1]])


class Truck:
    def __init__(self, hrs, mins):
        self.packages = []
        self.current_location = ''
        self.distance_traveled = 0.0
        self.speed = 18
        self.time = Time(hrs, mins)

    def add_package(self, pkg):
        self.packages.append(pkg)

    def add_distance(self, dist):
        self.distance_traveled = self.distance_traveled + dist

    def get_distance(self):
        return self.distance_traveled

    def get_packages(self):
        return self.packages


class Package:
    def __init__(self, p_id, p_address, p_city, p_state, p_zip, p_deadline, p_weight, p_special):
        self.p_id = p_id
        self.p_address = p_address
        self.p_city = p_city
        self.p_state = p_state
        self.p_zip = p_zip
        self.p_deadline = p_deadline
        self.p_weight = p_weight
        self.p_special = p_special
        self.p_status = Status.AT_HUB
        self.p_miles = 0.0
        self.p_departure_time = timedelta(hours=0, minutes=0)
        self.p_delivery_time = timedelta(hours=0, minutes=0)

    def get_info(self, s_time):
        s_list = self.get_status(s_time)
        return f'PACKAGE #{self.p_id}  | {s_list[0]}{s_list[1]}{s_list[2]} | Time Delivered: {s_list[3]}'

    def get_status(self, s_time):
        if s_time >= self.p_delivery_time:
            return [Colors.GREEN, self.p_status, Colors.DEFAULT, str(self.p_delivery_time)]
        elif self.p_departure_time < s_time < self.p_delivery_time:
            return [Colors.YELLOW, Status.EN_ROUTE, Colors.DEFAULT, 'NONE']
        else:
            return [Colors.BLUE, Status.AT_HUB, Colors.DEFAULT, 'NONE']


class Time:
    def __init__(self, hrs, mins):
        self.time = timedelta(
            hours=hrs,
            minutes=mins
        )

    def get_time(self):
        return self.time

    def add_time(self, t_min):
        self.time = self.time + timedelta(
            minutes=t_min
        )
        return True


# divide distance by truck speed in minutes
def get_travel_time(dist, truck):
    return dist / (truck.speed / 60)


# delivery algorithm
def deliver(hash_table, truck):
    # truck 1
    current_location = 'HUB, HUB'
    delivery_location = ''

    # set all package statuses to en route
    for pkg in truck.get_packages():
        pkg[1].p_status = Status.EN_ROUTE
        pkg[1].p_departure_time = truck.time.get_time()

    # deliver next package
    while truck.get_packages():
        dist_min = 0.0
        found_row = False
        move_down = False
        column = 2

        for row in dist_matrix:
            if not found_row:
                if current_location != (row[0] + ', ' + row[1]):
                    continue
                else:
                    found_row = True

            # traverse down matrix if 0.0 is found
            if move_down:
                for pkg in truck.get_packages():
                    d_location = row[0] + ', ' + row[1]
                    d_address = pkg[1].p_address + ', ' + pkg[1].p_zip

                    if d_location == d_address:
                        if dist_min == 0.0:
                            dist_min = float(row[column])
                            delivery_location = d_address
                        else:
                            if float(row[column]) < dist_min:
                                dist_min = float(row[column])
                                delivery_location = d_address

            # move across a row until 0.0 reached
            if not move_down:
                # matrix row
                r = 0

                for idx, col in enumerate(row):
                    if idx < 2:
                        continue

                    if float(col) == 0.0:
                        move_down = True
                        break

                    for pkg in truck.get_packages():
                        d_address = pkg[1].p_address + ', ' + pkg[1].p_zip
                        d_location = dist_matrix[r][0] + ', ' + dist_matrix[r][1]

                        if d_location == d_address:
                            if dist_min == 0.0:
                                dist_min = float(col)
                                delivery_location = d_address
                            else:
                                if float(col) < dist_min:
                                    dist_min = float(col)
                                    delivery_location = d_address

                    # increase row
                    r = r + 1
                    column = column + 1

        print('|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||')
        # add time it took to make delivery
        d_time = get_travel_time(dist_min, truck)
        # add time in minutes
        truck.time.add_time(d_time)
        # add distance
        truck.add_distance(dist_min)
        #time.sleep(0.2)
        print(truck.get_packages())
        print(current_location)

        # deliver package
        for pkg in truck.get_packages()[:]:
            dp_address = pkg[1].p_address + ', ' + pkg[1].p_zip
            # time.sleep(0.1)
            if delivery_location == dp_address:
                p_d = hash_table.search(pkg[0])
                p_d.p_status = Status.DELIVERED
                truck.get_packages().remove([pkg[0], p_d])
                p_d.p_delivery_time = truck.time.get_time()
                print('This package was delivered: ' + str(pkg[0]))
                print('Delivery time: ' + str(truck.time.get_time()))

        # set delivery location to current
        current_location = delivery_location


def load_packages(p_hash, tr_one, tr_two, tr_three):
    # load packages onto trucks
    for bucket in p_hash.table:
        for pkg in bucket:
            p = pkg[0]
            # special package cases
            if p == 13 or p == 14 or p == 15 or p == 16 or p == 19 or p == 20:
                tr_one.add_package(pkg)
            elif p == 3 or p == 18 or p == 36 or p == 38:
                tr_two.add_package(pkg)
            elif p == 6 or p == 25 or p == 26 or p == 28 or p == 31 or p == 32:
                truck_three.add_package(pkg)
            # fill up trucks one and two until full
            else:
                if len(truck_one.get_packages()) < 10:
                    tr_one.add_package(pkg)
                elif len(truck_two.get_packages()) < 12:
                    tr_two.add_package(pkg)
                else:
                    tr_three.add_package(pkg)


# TODO - create log for users
# def log_data():


# main function
if __name__ == '__main__':
    # initialize objects
    package_hash = HashTable()

    # csv reader for packages file
    with open('/home/legato/C950/packages.csv', newline='') as packages_file:
        packages = csv.reader(packages_file, delimiter=',')
        for row in packages:
            # p is package details list used to create package object
            p = []
            for box in row:
                p.append(box)
            # create package object with all details
            package = Package(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7])
            # insert each object into hash table
            package_hash.insert(int(package.p_id), package)

    # csv reader for packages file
    with open('/home/legato/C950/locations.csv', newline='') as locations_file:
        packages = csv.reader(locations_file, delimiter=',')
        for row in packages:
            dist_matrix.append(row)

    # create the three trucks
    truck_one = Truck(8, 0)
    truck_two = Truck(8, 0)
    truck_three = Truck(9, 5)
    # load the packages onto the trucks
    load_packages(package_hash, truck_one, truck_two, truck_three)
    # deliver all packages
    deliver(package_hash, truck_one)
    # deliver(package_hash, truck_two)
    # deliver(package_hash, truck_three)

    while True:
        user_input = int(input(
            "WGUPS DELIVERY INTERFACE\n\n" +
            "Please select an option:\n" +
            "\t1 - See delivery time of a specific package.\n"
            "\t2 - See delivery times of all packages.\n"
            "\t3 - See total distance traveled by all trucks.\n"
            "\t4 - EXIT PROGRAM.\n\n"
            "SELECTION: "
        ))

        # option 1
        if user_input == 1:
            while True:
                try:
                    pkg_input = int(input("Type in package number(1 - 40): "))
                except ValueError:
                    print("ERROR: Not a valid number.\n")
                    continue

                if 1 <= pkg_input <= 40:
                    while True:
                        print("\nMILITARY TIME FORMAT (24:00)")
                        time_input = input("Type a time to see package status ex.(8:30): ").split(':')
                        try:
                            t_hour = int(time_input[0])
                            t_minute = int(time_input[1])
                        except:
                            print("ERROR: Not a valid time format.\n")
                            continue
                        user_time = timedelta(hours=t_hour, minutes=t_minute)
                        print('\n' + package_hash.search(pkg_input).get_info(user_time) + '\n\n')
                        time.sleep(2)
                        break
                else:
                    print("ERROR: Please put in a number from 1 - 40.\n")
                    continue
                break

        # option 2
        elif user_input == 2:
            while True:
                print("\nMILITARY TIME FORMAT (24:00)")
                time_input = input("Type a time to see package status ex.(8:30): ").split(':')
                try:
                    t_hour = int(time_input[0])
                    t_minute = int(time_input[1])
                except:
                    print("ERROR: Not a valid time format.\n")
                    continue
                user_time = timedelta(hours=t_hour, minutes=t_minute)
                print('\n')
                break
            for pkg in range(1, 41):
                print(package_hash.search(pkg).get_info(user_time))

            print('\n\n')
            time.sleep(2)

        elif user_input == 3:
            print('\nTotal distance traveled by Truck 1: ' + str('%.2f' % truck_one.distance_traveled) + ' Miles.')
            print('Total distance traveled by Truck 2: ' + str('%.2f' % truck_two.distance_traveled) + ' Miles.')
            print('Total distance traveled by Truck 3: ' + str('%.2f' % truck_three.distance_traveled) + ' Miles.')

            print('\nTotal miles for ALL trucks: ' + str('%.2f' % (truck_one.distance_traveled + truck_two.distance_traveled +
                                                         truck_three.distance_traveled)) + ' Miles.\n\n')
            time.sleep(2)

        elif user_input == 4:
            print("\nGoodbye!")
            break

        else:
            print("\nPlease input a valid selection.\n\n")
            time.sleep(2)
