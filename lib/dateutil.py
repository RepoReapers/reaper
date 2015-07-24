from dateutil import relativedelta


class relativedelta(relativedelta.relativedelta):
    def total_hours(self):
        hours = (
            self.years * 365 * 24 +
            self.months * 30 * 24 +
            self.days * 24 +
            self.hours
        )
        return hours

    def total_minutes(self):
        return self.total_hours() * 60 + self.minutes

    def total_seconds(self):
        return self.total_minutes() * 60 + self.seconds

    def __lt__(self, other):
        if self == other:
            return False

        for attr in ['years', 'months', 'days', 'hours', 'minutes', 'seconds']:
            value = getattr(self, attr)
            if value < getattr(other, attr):
                return True
            elif value > getattr(other, attr):
                return False

    def __gt__(self, other):
        if self == other:
            return False

        for attr in ['years', 'months', 'days', 'hours', 'minutes', 'seconds']:
            value = getattr(self, attr)
            if value > getattr(other, attr):
                return True
            elif value < getattr(other, attr):
                return False

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other
