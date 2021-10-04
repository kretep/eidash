import datetime
from ephem import *
import math
from math import sin, cos, acos, asin, pi

class EphemData:

    def __init__(self):
        pass

    def get_data(self):
        now = datetime.datetime.now()
        return {
            'moon_age_fraction': self.get_moon_age_fraction(now),
            'positions': self.get_planet_positions(now),
            'sun_positions': self.get_sun_path(),
            'horizon': self.get_horizon(now)
        }

    def get_moon_age_fraction(self, date):
        """ Gets the "age" of the Moon as a fraction of the lunar cycle.
            New moon = 0.0, full moon = 0.5.
            Uses the 2 * 4 previous and next "quarter" phases provided by ephem
            to interpolate between the closest two quarters.
        """
        date = Date(date)
        prev_dates = [previous_new_moon(date), previous_first_quarter_moon(date),
            previous_full_moon(date), previous_last_quarter_moon(date)]
        max_prev_date = max(prev_dates)
        max_prev_index = prev_dates.index(max_prev_date)
        min_next_index = (max_prev_index + 1) % 4
        min_next_date = [next_new_moon, next_first_quarter_moon,
            next_full_moon, next_last_quarter_moon][min_next_index](date)
        between_quarters_fraction = (date - max_prev_date) / (min_next_date - max_prev_date)
        moon_age_fraction = 0.25 * (max_prev_index + between_quarters_fraction)
        return moon_age_fraction

    def get_planet_positions(self, date):
        date = Date(date)
        bodies = [Sun(), Mercury(), Venus(), Moon(), Mars(), Jupiter(), Saturn()]
        positions = {}
        for body in bodies:
            body.compute(date)
            positions[body.name] = (body.ra / pi * 180, body.dec / pi * 180)
        return positions

    def get_sun_path(self):
        ref_date = datetime.date(2021, 3, 21)
        sun = Sun()
        positions = []
        for day in range(0, 365, 10):
            delta = datetime.timedelta(days = day)
            date = ref_date + delta
            sun.compute(date)
            positions.append((sun.ra / pi * 180, sun.dec / pi * 180))
        return positions

    def get_horizon(self, date):
        horizon = []
        for i in range(36):
            ra, dec = self.horizontal_to_equatorial(i * 10.0 - 180, 0.0)
            horizon.append((ra, dec))
        return horizon

    def horizontal_to_equatorial(self, az, el):
        latitude = 52.0
        longitude = 4.5
        now = datetime.datetime.utcnow()

        julian_date = self.get_julian_datetime(now)

        T = ((julian_date - 2451545.0) / 36525)
        theta0 = 280.46061837 + 360.98564736629 * (julian_date - 2451545.0) + (0.000387933 * T * T) - (T * T * T / 38710000.0)
        angle = theta0 % 360
        
        # utc_time = now.hour + 1.0 * now.minute / 60 + 1.0 * now.second / 3600
        # day_of_year = now.timetuple().tm_yday
        # # Equation of time
        # # Duffie and Beckmann, Solar Engineering of Thermal Processes, 4th Edition
        # B = (day_of_year - 1) / 365.0 * 2.0 * math.pi
        # E = 229.2 * (0.000075 + 0.001868 * math.cos(B) - 0.032077 * math.sin(B) - 0.014615 * math.cos(2 * B) - 0.04089 * math.sin(2 * B))
        # # E is in minutes
        # print("solar time", utc_time + 4.0 * longitude / 60 + E / 60)
        # solar_time_angle = (15.0 * utc_time + longitude + E / 4) * pi / 180

        angle = angle * math.pi / 180
        az = az * math.pi / 180
        el = el * math.pi / 180
        lat = latitude * math.pi / 180
        lon = longitude * math.pi / 180

        dec = asin(sin(el) * sin(lat) + cos(el) * cos(lat) * cos(az))
        w = (sin(el) - sin(dec) * sin(lat)) / (cos(dec) * cos(lat))
        w = min(1.0, max(-1.0, w)) # clamp to -1.0, 1.0 if outside
        H = acos( w )
        if sin(az) > 0:
            H = 2 * pi - H
        ra = (angle - H) % (2 * pi)


        # dec = asin(sin(el) * sin(lat) + cos(el) * cos(lat) * cos(az))
        # H = 0
        # if dec < 0:
        #     H = asin(-1.0 * sin(az) * cos(el) / cos(dec))
        # else:
        #     w = (sin(el) - sin(dec) * sin(lat)) / (cos(dec) * cos(lat))
        #     if w < -1.0:
        #         w = -1.0
        #     if w > 1.0:
        #         w = 1.0
        #     H = acos( w )
        # ra = (angle - H) % (2 * pi)

        return (ra / pi * 180.0, dec / pi * 180)

    def get_julian_datetime(self, date):
        """
        Convert a datetime object into julian float.
        Args:
            date: datetime-object of date in question

        Returns: float - Julian calculated datetime.
        Raises: 
            TypeError : Incorrect parameter type
            ValueError: Date out of range of equation
        """

        # Ensure correct format
        if not isinstance(date, datetime.datetime):
            raise TypeError('Invalid type for parameter "date" - expecting datetime')
        elif date.year < 1801 or date.year > 2099:
            raise ValueError('Datetime must be between year 1801 and 2099')

        # Perform the calculation
        julian_datetime = 367 * date.year - int((7 * (date.year + int((date.month + 9) / 12.0))) / 4.0) + int(
            (275 * date.month) / 9.0) + date.day + 1721013.5 + (
                            date.hour + date.minute / 60.0 + date.second / math.pow(60,
                                                                                    2)) / 24.0 - 0.5 * math.copysign(
            1, 100 * date.year + date.month - 190002.5) + 0.5

        return julian_datetime
