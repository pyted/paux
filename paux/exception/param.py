from paux.exception._base import AbstractEXP


class ParamException(AbstractEXP):
    def __init__(self, msg):
        self.error_msg = msg



class DatePatternException(AbstractEXP):
    def __init__(self,date,date_patterns):
        msg = 'Unable to convert date to timestamp, date={date}, Supported patterns are {date_pattern}'.format(
            date=date,
            date_pattern='\n\t'.join(
                [fmt for fmt, pattern in date_patterns]
            )
        )
        self.error_msg = msg


class DateTypeException(AbstractEXP):
    def __init__(self,date):
        msg = 'Param date type error, date = {date}, Supported type are [int, float, datetime.date, datetime.datetime, str]'.format(
            date=str(date)
        )
        self.error_msg = msg




class ParamBarException(AbstractEXP):
    def __init__(self, bar, pmt="bar must like ['1m','3m','5m','30m','1h','2h','4h','6h','1d'...]"):
        pmt = "bar must like ['1m','3m','5m','30m','1h','2h','4h','6h','1d'...]"
        self.error_msg = 'bar = {bar} \n {pmt}'.format(
            bar=str(bar),
            pmt=pmt,
        )


class PosSideException(AbstractEXP):
    def __init__(self, posSide, pmt="posSide must in ['LONG','SHORT']"):
        self.error_msg = 'posSide= {posSide} \n {pmt}'.format(
            posSide=str(posSide),
            pmt=pmt,
        )
