from typing import Dict, List, Tuple


class IntersectionTimer():
    idx = 0
    current_timer: int = 0
    schedule: List[Tuple[str, int]] = []
    idx_schedule = 0

    def __init__(self, idx, schedule):
        self.intersection_idx = idx
        self.schedule = schedule
        self.current_timer = schedule[0]
        self.idx_schedule = 0
        self.time = 0

    def update(self):
        self.time += 1
        if self.time >= self.schedule[self.idx_schedule][1]:
            self.idx_schedule += 1
            if self.idx_schedule >= len(self.schedule):
                self.idx_schedule = 0

            self.current_timer = self.schedule[self.idx_schedule]
            self.time = 0

    def get_current_green_light_street(self):
        return self.schedule[self.idx_schedule][0]


class Car():
    travel_nbr: int = 0
    current_travel_nbr: int = 0
    street_names: List[str]
    idx: int = 0

    def __init__(self, idx: int, street_names: [str], travel_nbr: int):
        self.idx = idx
        self.street_names = street_names
        self.travel_nbr = travel_nbr

    def car_passed_intersection(self):
        self.current_travel_nbr += 1

    def check_if_win(self):
        return self.current_travel_nbr >= self.travel_nbr

    def get_street(self):
        return self.street_names[self.current_travel_nbr]


class Street():
    name: str = ""
    time: int = 0
    cars: [(Car, int)] = []
    is_green_light: bool = False
    intersection1: int = 0
    intersection2: int = 0

    def __init__(self, name, time, intersection1, intersection2, car_list: [Car]):
        self.name = name
        self.time = time
        self.intersection1 = intersection1
        self.intersection2 = intersection2
        self.cars = []
        self.place_cars(car_list)

    def print_cars(self):
        print(f"Street {self.name} has {len(self.cars)} cars: ")
        print(self.cars)

    def place_cars(self, car_list):
        last_pos = self.time - 1
        for idx, c in enumerate(car_list):
            if self.name == c.street_names[0]:
                self.cars.append((c, last_pos))
                last_pos -= 1

    def set_green_light(self, is_green_light: bool):
        self.is_green_light = is_green_light

    def add_car_to_street_start(self, c: Car):
        self.cars.append((c, 0))

    def is_car_at_pos(self, pos: int) -> int:
        max_pos = 0
        for c, p in self.cars:
            if p == pos:
                return True
        return False

    def update_cars(self) -> Car:
        car_to_return = None
        new_cars: List[(Car, int)] = []
        for idx, car_tuple in enumerate(self.cars):
            c, c_time = car_tuple

            if not self.is_car_at_pos(c_time + 1):
                c_time += 1
                if self.is_green_light and c_time >= self.time:
                    c.car_passed_intersection()
                    car_to_return = c
                    continue

            new_cars.append((c, c_time))

        self.cars = new_cars

        return car_to_return


def loop(time: int, bonus: int, streets, schedules: List[List[Tuple[str, int]]]) -> int:
    score: int = 0
    intersection_timers = [IntersectionTimer(idx, s) for idx, s in enumerate(schedules)]

    for i in range(time):
        print(i)
        # Updating timers
        for t in intersection_timers:
            t.update()
            # Updating street lights
            streets[t.get_current_green_light_street()].set_green_light(True)

        # Moving cars
        for st in streets:
            c = streets[st].update_cars()
            if not c:
                continue

            if c.check_if_win():
                score += (bonus + (time - i - 1))
                # print(score)
                # print(f"Car {c.idx} scored {bonus} + {time - i} points")
                continue

            car_wanted_street = c.get_street()
            streets[car_wanted_street].add_car_to_street_start(c)

    return score