#!/usr/local/bin/python3
import datetime
from dataclasses import dataclass

@dataclass
class Activities:
    days: int
    count: int
    distance: int
    elevation: int
    minutes: int
    eddington : int

    def feet_per_mile(self):
        blah = self.elevation / self.distance
        return round(blah)

    def miles_per_day(self):
        return round(self.distance / self.days)

    def time_per_day(self):
        return round(self.minutes / self.distance)
    

seven = Activities(7,3,23,500,600,2)

print(seven)
print('Days=' + str(seven.days))
print('Count=' + str(seven.count))
print('Distance=' + str(seven.distance))
print('Elevation=' + str(seven.elevation))
print('Minutes=' + str(seven.minutes))
print('Eddington=' + str(seven.eddington))
print('Feet per Mile=' + str(seven.feet_per_mile()))
print('Miles per Day=' + str(seven.miles_per_day()))
print('Time per Day=' + str(seven.time_per_day()))