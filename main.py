# Caleb O'Neill
# Student ID: 001092382

# import modules
import csv
import time
from datetime import timedelta

from scripts.hash import HashTable
from scripts.package import Package
from scripts.truck import Truck
from scripts.utils import Status
# matrix to store delivery locations and distances
dist_matrix = []
# global truck 3 start bool
truck_three_start = False
# debug
debug = False


# PART A - Nearest Neighbor Algorithm
# This algorithm traverses the matrix to find the nearest location of delivery sites and delivers those packages
# TIME COMPLEXITY: N^2 * M^2
# SPACE COMPLEXITY: O(1) // points to package objects
def deliver(hash_table, truck):
    current_location = 'HUB, HUB'
    delivery_location = ''
    truck_finished = False
    special_complete = False

    # set all package statuses to en route
    for pkg in truck.get_packages():
        pkg[1].p_status = Status.EN_ROUTE
        pkg[1].p_departure_time = truck.time.get_time()
        pkg[1].set_truck(truck.get_number())

    # deliver next package
    while truck.get_packages():
        dist_min = 0.0
        found_row = False
        move_down = False
        column = 2
        # go through each row in matrix
        for row in dist_matrix:

            # special case for packages 6 and 25
            if not special_complete:
                if truck.time.get_time() > timedelta(hours=9, minutes=5) and (
                        truck.get_number() == 1 or truck.get_number() == 2):
                    t_row = 0
                    hub_distance = 0.0

                    # package 6
                    if truck.get_number() == 1:
                        for item in dist_matrix:
                            if item[0] == current_location.split(",")[0]:
                                hub_distance = float(item[2])
                                break
                        # drive back to hub to pick up package 6
                        truck.add_distance(hub_distance)
                        truck.time.add_time(truck.get_travel_time(hub_distance))
                        # picked up package 6. Now deliver it
                        dist_min = float(dist_matrix[13][2])
                        delivery_location = dist_matrix[13][0] + ', ' + dist_matrix[13][1]
                        special_complete = True

                    # package 7
                    if truck.get_number() == 2:
                        for item in dist_matrix:
                            if item[0] == current_location.split(",")[0]:
                                hub_distance = float(item[2])
                                break
                        # drive back to hub to pick up package 6
                        truck.add_distance(hub_distance)
                        truck.time.add_time(truck.get_travel_time(hub_distance))
                        # picked up package 6. Now deliver it
                        dist_min = float(dist_matrix[13][2])
                        delivery_location = dist_matrix[24][0] + ', ' + dist_matrix[24][1]
                        special_complete = True

                    break
            # see if row has location
            if not found_row:
                if current_location != (row[0] + ', ' + row[1]):
                    continue
                else:
                    found_row = True

            # traverse down matrix if 0.0 is found
            if move_down:
                for pkg in truck.get_packages():
                    if (pkg[0] == 6 or pkg[0] == 25) and truck.time.get_time() < timedelta(hours=9, minutes=5):
                        continue

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
                        if (pkg[0] == 6 or pkg[0] == 25) and truck.time.get_time() < timedelta(hours=9, minutes=5):
                            continue

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

        # add time it took to make delivery
        d_time = truck.get_travel_time(dist_min)
        # add time in minutes
        truck.time.add_time(d_time)
        # add distance
        truck.add_distance(dist_min)

        # deliver package
        for pkg in truck.get_packages()[:]:
            dp_address = pkg[1].p_address + ', ' + pkg[1].p_zip
            # time.sleep(0.1)
            if delivery_location == dp_address:
                p_d = hash_table.search(pkg[0])
                p_d.p_status = Status.DELIVERED
                truck.get_packages().remove([pkg[0], p_d])
                p_d.p_delivery_time = truck.time.get_time()
                # debug
                global debug
                if debug:
                    print('Truck Number: ' + str(truck.get_number()))
                    print('\tThis package was delivered: ' + str(pkg[0]))
                    print('\tDelivery time: ' + str(truck.time.get_time()))
                    print('\tDelivery Location: ' + delivery_location + '\n')
                    print('\tCurrent Location: ' + current_location + '\n')
        # see if truck is finished delivering packages
        if not truck.get_packages():
            truck_finished = True
        # set truck 3 to go with truck 2 driver
        if truck.get_number() == 2 and truck_finished:
            hub_distance = 0.0
            for item in dist_matrix:
                if item[0] == delivery_location.split(",")[0]:
                    hub_distance = float(item[2])
            truck.add_distance(hub_distance)
            truck.time.add_time(truck.get_travel_time(hub_distance))
            # set truck 3 boolean to true to start truck 3
            global truck_three_start
            truck_three_start = True

        # set delivery location to current
        current_location = delivery_location

# TIME COMPLEXITY: O(N^2)
# SPACE COMPLEXITY: O(1)
# load packages onto trucks
def load_packages(p_hash, tr_one, tr_two, tr_three):
    for bucket in p_hash.table:
        for pkg in bucket:
            p = pkg[0]
            # special package cases
            if p == 13 or p == 14 or p == 15 or p == 16 or p == 19 or p == 20 or p == 6 or p == 37:
                tr_one.add_package(pkg)
            elif p == 3 or p == 18 or p == 36 or p == 38 or p == 31 or p == 29 or p == 25:
                tr_two.add_package(pkg)
            elif p == 6 or p == 25 or p == 26 or p == 28 or p == 32 or p == 2 or p == 4 or p == 5:
                tr_three.add_package(pkg)
            # fill up trucks one and two until full
            else:
                if len(tr_one.get_packages()) < 10:
                    tr_one.add_package(pkg)
                elif len(tr_two.get_packages()) < 12:
                    tr_two.add_package(pkg)
                else:
                    tr_three.add_package(pkg)
    global debug
    if debug:
        print('Truck One total packages: ' + str(len(tr_one.get_packages())))
        print('Truck Two total packages: ' + str(len(tr_two.get_packages())))
        print('Truck Three total packages: ' + str(len(tr_three.get_packages())) + '\n\n')


# main function
# This function asks the user to select an option to see status of packages or trucks
# Once the selection is made and the time is entered, the user will get feedback displayed on the info
# that they are inquiring
if __name__ == '__main__':
    # initialize objects
    package_hash = HashTable()

    # csv reader for packages file
    with open('inputs/packages.csv', newline='') as packages_file:
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
    with open('inputs/locations.csv', newline='') as locations_file:
        packages = csv.reader(locations_file, delimiter=',')
        for row in packages:
            dist_matrix.append(row)

    # create the first 2 trucks
    truck_one = Truck(8, 0, 1)
    truck_two = Truck(8, 0, 2)
    truck_three = Truck(0, 0, 3)
    # load the packages onto the trucks
    load_packages(package_hash, truck_one, truck_two, truck_three)
    # deliver all packages
    deliver(package_hash, truck_one)
    deliver(package_hash, truck_two)
    while not truck_three_start:
        continue
    # truck 2 arrives to Hub 10:42:40a. Package #9 needs to be updated on truck 3
    package_hash.search(9).update_address('410 S State St', 'Salt Lake City', 'UT', '84111')

    # truck 2 driver will take truck 3
    truck_three.time.set_start_time(truck_two.time.get_time())
    deliver(package_hash, truck_three)
    # user interface
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
                        print(package_hash.search(pkg_input).get_info(user_time))
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
                time_input = input("Type a time to see all package status ex.(8:30): ").split(':')
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
        # print out truck info
        elif user_input == 3:
            print('\nTotal distance traveled by Truck 1: ' + str('%.2f' % truck_one.distance_traveled) + ' Miles.')
            print('Total distance traveled by Truck 2: ' + str('%.2f' % truck_two.distance_traveled) + ' Miles.')
            print('Total distance traveled by Truck 3: ' + str('%.2f' % truck_three.distance_traveled) + ' Miles.')

            print('\nTotal miles for ALL trucks: ' + str('%.2f' % (truck_one.distance_traveled + truck_two.distance_traveled +
                                                         truck_three.distance_traveled)) + ' Miles.\n\n')
            time.sleep(2)
        # exit program
        elif user_input == 4:
            print("\nGoodbye!")
            time.sleep(1)
            break
        # invalid selection
        else:
            print("\nPlease input a valid selection.\n\n")
            time.sleep(2)
