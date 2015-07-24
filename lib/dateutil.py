from dateutil import relativedelta


class relativedelta(relativedelta.relativedelta):
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
