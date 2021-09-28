import datetime
from ephem import *

class EphemData:

    def __init__(self):
        pass

    def get_data(self):
        now = datetime.datetime.now()
        return {
            'moon_age_fraction': self.get_moon_age_fraction(now),
            'positions': self.get_planet_positions(now),
            'sun_positions': self.get_sun_path(),
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
        for day in range(0, 365, 5):
            delta = datetime.timedelta(days = day)
            date = ref_date + delta
            sun.compute(date)
            positions.append((sun.ra / pi * 180, sun.dec / pi * 180))
        return positions
