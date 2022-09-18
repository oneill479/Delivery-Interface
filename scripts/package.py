from datetime import timedelta
from scripts.utils import Status, Colors


# Package class to store package objects
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
        self.p_truck = 0

    # get package info
    def get_info(self, s_time):
        s_list = self.get_status(s_time)
        return f'PACKAGE #{self.p_id}  | {s_list[0]}{s_list[1]}{s_list[2]} |' \
               f' Truck Number: {self.p_truck} | Time Delivered: {s_list[3]}'

    # get package status
    def get_status(self, s_time):
        if s_time >= self.p_delivery_time:
            return [Colors.GREEN, self.p_status, Colors.DEFAULT, str(self.p_delivery_time)]
        elif self.p_departure_time < s_time < self.p_delivery_time:
            return [Colors.YELLOW, Status.EN_ROUTE, Colors.DEFAULT, 'N/A']
        else:
            return [Colors.BLUE, Status.AT_HUB, Colors.DEFAULT, 'N/A']

    # set truck number
    def set_truck(self, num):
        self.p_truck = num

    # update the address of a package
    def update_address(self, address, city, state, zipcode):
        self.p_address = address
        self.p_city = city
        self.p_state = state
        self.p_zip = zipcode
