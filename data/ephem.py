from datetime import datetime
import ephem

class EphemData:

    def __init__(self):
        pass

    def get_data(self):
        return {
            'moon_age_fraction': self.get_moon_age_fraction(datetime.now())
        }

    def get_moon_age_fraction(self, date):
        """ Gets the "age" of the Moon as a fraction of the lunar cycle.
            New moon = 0.0, full moon = 0.5.
            Uses the 2 * 4 previous and next "quarter" phases provided by ephem
            to interpolate between the closest two quarters.
        """
        date = ephem.Date(date)
        prev_dates = [ephem.previous_new_moon(date), ephem.previous_first_quarter_moon(date),
            ephem.previous_full_moon(date), ephem.previous_last_quarter_moon(date)]
        max_prev_date = max(prev_dates)
        max_prev_index = prev_dates.index(max_prev_date)
        min_next_index = (max_prev_index + 1) % 4
        min_next_date = [ephem.next_new_moon, ephem.next_first_quarter_moon,
            ephem.next_full_moon, ephem.next_last_quarter_moon][min_next_index](date)
        between_quarters_fraction = (date - max_prev_date) / (min_next_date - max_prev_date)
        moon_age_fraction = 0.25 * (max_prev_index + between_quarters_fraction)
        return moon_age_fraction
