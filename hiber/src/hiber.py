import re
import datetime

class LPGAN_API:
    def __init__(self):
        pass

    @staticmethod
    def set_gps_mode(enabled):
        if not isinstance(enabled, bool):
            raise ValueError('enabled must be a boolean value')
        if enabled:
            param = 'true'
        else:
            param = 'false'

        return f'set_gps_mode({param})\r\n'

    @staticmethod
    def do_gps_fix(input_string=None):
        if input_string == None:
            return 'do_gps_fix\r\n'
        else:
            if not isinstance(input_string, str):
                raise ValueError('input_string must be a string')
            return f'do_gps_fix(\"{input_string}\")\r\n'

    @staticmethod
    def get_firmware_version():
        return 'get_firmware_version\r\n'

    @staticmethod
    def get_modem_info():
        return 'get_modem_info\r\n'

    @staticmethod
    def set_modem_number(modem_number):
        if not isinstance(modem_number, str):
            raise ValueError('modem_number must be string value with format \'XXXX XXXX\'')
        pattern = re.compile(r'^\w\w\w\w \w\w\w\w$')
        if not pattern.match(modem_number):
            raise ValueError('modem_number must have format \'XXXX XXXX\'')
        return f'set_modem_number({modem_number})\r\n'

    @staticmethod
    def get_location():
        return 'get_location\r\n'

    @staticmethod
    def set_location(latitude, longitude, elevation):
        return f'set_location(\"{latitude:0.6f}\",\"{longitude:0.6f}\",\"{elevation:0.1f}\")\r\n'

    @staticmethod
    def get_datetime():
        return 'get_datetime\r\n'

    def set_datetime(dt):
        '''
        Create the set_datetime string.
        
        Args:
            dt: Datetime 
        '''
        if not isinstance(dt, datetime.datetime):
            raise ValueError("dt must be a datetime.datetime object")
        dt_str = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        return f'set_datetime(\"{dt_str}\")\r\n'

    @staticmethod
    def get_next_alarm():
        return 'get_next_alarm\r\n'

    @staticmethod
    def get_next_pass():
        return 'get_next_pass\r\n'

    @staticmethod
    def go_to_sleep():
        return 'go_to_sleep\r\n'

    @staticmethod
    def toggle_payload_over_debug(is_enabled):
        if not isinstance(is_enabled, bool):
            raise ValueError('is_enable must be a boolean value')
        if is_enabled:
            return 'toggle_payload_over_debug(true)\r\n'
        else:
            return 'toggle_payload_over_debug(false)\r\n'

    @staticmethod
    def set_payload(payload):
        if not isinstance(payload, int):
            raise ValueError('payload must be an integer (number of bytes to be sent)')
        return f'set_payload(\"{payload}\")\r\n'