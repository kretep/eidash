import datetime
import ephem

class EphemData:

    def __init__(self):
        pass

    def get_data(self):
        return {
            'moon_age_fraction': self.get_moon_age_fraction()
        }

    def get_moon_age_fraction(self):
        date = ephem.Date(datetime.datetime.now())
        nnm = ephem.next_new_moon(date)
        pnm = ephem.previous_new_moon(date)
        lunation = (date - pnm) / (nnm - pnm)
        return lunation