import iso8601


class TimeHandler:
    """
        This class is used for time handling operations only
    """
    def convert_to_utc(self, time, return_as_string=True):
        try:
            converted_time = iso8601.parse_date(time).strftime("%s")
            return str(converted_time) if return_as_string else converted_time
        except Exception:
            print('Error in Converting time')
            raise ArithmeticError
