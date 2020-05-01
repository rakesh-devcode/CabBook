from scipy.spatial import distance as manhtn_distance
import numpy as np
import sys

class BookingEngine:
    def __init__(self):
        self.total_cars = 3
        self.booked_cars = []
        self.available_cars = []
        self.all_cars = {}
        self.create_cars()

    def create_cars(self):
        """
            Creating the cars with id and coordinates
        """
        for i in range(self.total_cars):
            self.all_cars["car_"+str(i+1)]= {
                                                "car_id": i+1,
                                                "curr_coords": (0, 0),
                                                "status": "AVLBL",
                                                "car_to_cust_loc_dist":0,
                                                "dest_distance": 0,
                                                "dest_coord": (0, 0),
                                                "tickStep": 0,
                                                "customer_loc":(0,0),
                                                "picked_customer":False
                                            }
            self.available_cars.append(i+1)

    def get_distance_between_coords(self, source_coords, dest_coords):
        """
        Getting distance between source and destination
        :param source_coords: Source co-ordinates
        :param dest_coords: Destination co-ordinate
        :return: distance between the co-ordinates in units
        """
        distance = manhtn_distance.cityblock(source_coords, dest_coords)
        return distance

    def get_nearest_available_car(self, src_coord, dest_coord):
        """
         Getting the nearest available cars
         :param src_coord: Source co-ordinates
         :param dest_coord: Destination co-ordinate
         :return: Nearest available car id and total time
         """
        try:
            available_car = None
            less_dist = sys.maxsize
            for car_index in self.available_cars:
                car = self.all_cars.get("car_"+str(car_index))
                car_curr_coord = list(car.get("curr_coords"))
                car_2_src_dist = self.get_distance_between_coords(car_curr_coord, src_coord)
                src_2_dst_dist = self.get_distance_between_coords(src_coord, dest_coord)
                if car_2_src_dist+src_2_dst_dist <= less_dist:
                    if available_car is not None and available_car[0].get("car_id") > car.get("car_id") or available_car is None:
                        available_car = [{"car_id": car_index, "total_time": int(car_2_src_dist+src_2_dst_dist)}, src_2_dst_dist, car_2_src_dist]
                    less_dist = car_2_src_dist+src_2_dst_dist
            return available_car
        except Exception as e:
            print(f'Error happened while getting nearest available cars {str(e)}')
            raise Exception

    def set_next_coords(self):
        """
        Find the manhattan distance of all the surrounding 4 points of current car position
        :return:
        """
        # print("booked_cars:")
        # print(self.booked_cars)
        try:
            tmp_booked_cars = self.booked_cars.copy()
            for car_index in tmp_booked_cars:
                car = self.all_cars.get("car_" + str(car_index))

                tickNumber = car.get("tickStep") + 1
                if tickNumber >= car.get("car_to_cust_loc_dist"):
                    car["picked_customer"] = True
                if car.get("picked_customer"):
                    if car["curr_coords"] != car.get("customer_loc"):
                        car["curr_coords"] = car.get("customer_loc")
                car["tickStep"] = tickNumber
                if tickNumber == car.get("car_to_cust_loc_dist") + car.get("dest_distance"):
                    car["curr_coords"] = car.get("dest_coord")
                    car["dest_distance"] = 0
                    car["status"] = "AVLBL"
                    car["tickStep"] = 0
                    car["customer_loc"] = (0,0)
                    car["car_to_cust_loc_dist"] = 0
                    car["picked_customer"] = False
                    self.booked_cars.remove(car_index)
                    self.available_cars.append(car_index)
                self.all_cars["car_" + str(car_index)] = car
            return "Coordinates updated after 1 unit time ..!!"
        except Exception as e:
            print(f'Error while setting next coordinates {str(e)}')
            raise Exception

    def book(self, src_coord, dest_coord):
        """
        Booking the car based upon the availability
        :return: car_id and total_time in Json

        """
        try:
            ready_car = self.get_nearest_available_car(src_coord, dest_coord)
            if ready_car is not None:
                car_id = ready_car[0].get("car_id")
                src_2_dest_dist = ready_car[1]
                car_2_src_dist = ready_car[2]
                self.available_cars.remove(car_id)
                self.booked_cars.append(car_id)
                self.all_cars.get("car_" + str(car_id))["customer_loc"] = tuple(src_coord)
                self.all_cars.get("car_" + str(car_id))["dest_coord"] = tuple(dest_coord)
                self.all_cars.get("car_" + str(car_id))["dest_distance"] = src_2_dest_dist
                self.all_cars.get("car_" + str(car_id))["car_to_cust_loc_dist"] = car_2_src_dist
                self.all_cars.get("car_" + str(car_id))["status"] = "BOOKED"
                # print("Booked cars: ")
                # print(self.booked_cars)
                # print("Available: ")
                # print(self.available_cars)
                return ready_car[0]
            else:
                "Sorry, No cars are available at the moment!!"

        except Exception as e:
            print(f'Error happened while booking available car : {str(e)}')
            raise Exception

    def tick(self):
        """
        Moving the time by 1 unit
        """
        self.set_next_coords()
        # print(self.all_cars)
        # print(self.available_cars)

    def reset(self):
        """
        Reset all cars to initial data
        """
        self.__init__()
        # print(self.all_cars)
        # print(self.available_cars)
        # print(self.booked_cars)


