import re
import datetime


class LPGAN_API_Tx:
    def __init__(self):
        pass

    @staticmethod
    def set_gps_mode(enabled):
        if not isinstance(enabled, bool):
            raise ValueError("enabled must be a boolean value")
        if enabled:
            param = "true"
        else:
            param = "false"

        return f"set_gps_mode({param})\r\n"

    @staticmethod
    def do_gps_fix(input_string=None):
        if input_string == None:
            return "do_gps_fix\r\n"
        else:
            if not isinstance(input_string, str):
                raise ValueError("input_string must be a string")
            return f'do_gps_fix("{input_string}")\r\n'

    @staticmethod
    def get_firmware_version():
        return "get_firmware_version\r\n"

    @staticmethod
    def get_modem_info():
        return "get_modem_info\r\n"

    @staticmethod
    def set_modem_number(modem_number):
        if not isinstance(modem_number, str):
            raise ValueError(
                "modem_number must be string value with format 'XXXX XXXX'"
            )
        pattern = re.compile(r"^\w\w\w\w \w\w\w\w$")
        if not pattern.match(modem_number):
            raise ValueError("modem_number must have format 'XXXX XXXX'")
        return f"set_modem_number({modem_number})\r\n"

    @staticmethod
    def get_location():
        return "get_location\r\n"

    @staticmethod
    def set_location(latitude, longitude, elevation):
        return (
            f'set_location("{latitude:0.6f}","{longitude:0.6f}","{elevation:0.1f}")\r\n'
        )

    @staticmethod
    def get_datetime():
        return "get_datetime\r\n"

    @staticmethod
    def set_datetime(dt):
        """
        Create the set_datetime string.
        
        Args:
            dt: Datetime 
        """
        if not isinstance(dt, datetime.datetime):
            raise ValueError("dt must be a datetime.datetime object")
        dt_str = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        return f'set_datetime("{dt_str}")\r\n'

    @staticmethod
    def get_next_alarm():
        return "get_next_alarm\r\n"

    @staticmethod
    def get_next_pass():
        return "get_next_pass\r\n"

    @staticmethod
    def go_to_sleep():
        return "go_to_sleep\r\n"

    @staticmethod
    def toggle_payload_over_debug(is_enabled):
        if not isinstance(is_enabled, bool):
            raise ValueError("is_enable must be a boolean value")
        if is_enabled:
            return "toggle_payload_over_debug(true)\r\n"
        else:
            return "toggle_payload_over_debug(false)\r\n"

    @staticmethod
    def set_payload(payload):
        if not isinstance(payload, int):
            raise ValueError("payload must be an integer (number of bytes to be sent)")
        return f'set_payload("{payload}")\r\n'


ERROR_CODES = {
    "125": "Buffer Overflow",
    "126": "Space found in command name",
    "127": "No command name specified",
    "128": "Generic unexpected character while parsing command name",
    "129": "Invalid HEX value entered",
    "130": "Unexpected character after space",
    "131": "Unexpected character before HEX specifier",
    "132": "Unexpected whitespace after HEX specifier",
    "133": "Generic unexpected character found in keyword",
    "134": "Unexpected character after keyword after space",
    "135": "Generic unexpected character found parsing keyword",
    "136": "Argument count exceeded",
    "137": "Generic unexpected character found while parsing character",
    "138": "Generic unexpected character found while parsing character",
    "139": "End of command contained unexpected character",
    "140": "Generic unexpected character error",
    "141": "(internal) Unexpected string state",
    "142": "(internal) Unexpected number state",
    "143": "(internal) Unexpected keyword state",
    "144": "(internal) Unexpected argument state",
    "145": "(internal) Unexpected arguments finished state",
    "146": "(internal) Unexpected state",
    "147": "(internal) Unexpected hex number state",
    "150": "Debug Message (Command parsing)",
    "225": "HEX value not valid",
    "226": "Unknown escape character",
    "325": "Unknown keyword",
    "350": "Debug Message (Argument conversion)",
    "425": "Unknown command",
    "426": "Too many or too little arguments passed to command",
    "525": "Buffer overflow",
    "600": "OK, input has been processed successfully",
    "602": "Modem starting to sleep",
    "603": "Cannot sleep (Wakeup pin is high)",
    "625": "Invalid input",
    "626": "(help command only) Unknown command",
    "632": "GPS is disabled",
    "633": "GPS is enabled",
    "634": "Command not implemented",
    "635": "Not going to sleep (wakeup within 2 seconds)",
    "636": "Generic error code",
}


class LPGAN_API_Rx:
    def __init__(self):
        pass

    # @staticmethod
    # def parse_api_message(message):
    #     if message.startswith("API"):
    #         message = message[:message.find(')')]
    #         result = message[message.find("API(") + 4 :].strip().strip(")").split(":",1)
    #         if len(result) > 1:
    #             result[1] = result[1].split(";")
    #             result[1] = [result.lstrip() for result in result[1]]
    #         else:
    #             result = [result[0], []]
    #     elif message.startswith("Hiber API "):
    #         pass
    #     else:
    #         raise ValueError("Invalid API Rx string")
    #     print(result)
    #     return result

    @staticmethod
    def parse_api_message2(message, error_handling=False):
        if message.startswith("API"):
            message = message[:message.find(')')]
            result = message[message.find("API(") + 4 :].strip().strip(")").split(":",1)
            if len(result) > 1:
                result[1] = result[1].split(";")
                result[1] = [result.lstrip() for result in result[1]]
            else:
                result = [result[0], []]
        elif message.startswith("Hiber API "):
            pass
        else:
            raise ValueError("Invalid API Rx string")
        print(result)

        if error_handling:
            if "600" != result[0]:
                print(result)
                raise ValueError(ERROR_CODES[result[0]])
            else:
                return result[1]
        else:
            return [result[0], result[1]]

    @classmethod
    def set_gps_mode(cls, message):
        # [error, results] = cls.parse_api_message(message)
        # if "600" != error:
        #     raise ValueError(ERROR_CODES[error])
        results = cls.parse_api_message2(message, True)
        if results[0].strip() == "0":
            return False
        else:
            return True

    @classmethod
    def do_gps_fix(cls, message):
        # [error, results] = cls.parse_api_message(message)
        # if "600" != error:
        #     raise ValueError(ERROR_CODES[error])
        results = cls.parse_api_message2(message, True)
    @classmethod
    def get_firmware_version(cls, message):
        # [error, results] = cls.parse_api_message(message)
        # if "600" != error:
        #     raise ValueError(ERROR_CODES[error])
        results = cls.parse_api_message2(message, True)
        return {'firmware_version':results[0]}

    @classmethod
    def get_modem_info(cls, message):
        # [error, results] = cls.parse_api_message(message)
        # if "600" != error:
        #     raise ValueError(ERROR_CODES[error])
        results = cls.parse_api_message2(message, True)
        results = {
            'HW_TYPE_STR':results[0],
            'HW_TYPE_INT':int(results[1]),
            'FW_VERSION':results[2],
            'MODEM_NO_STR':results[3],
            'MODEM_NO_INT':int(results[4])
        }
        return results

    @classmethod
    def set_modem_number(cls, message):
        # [error, results] = cls.parse_api_message(message)
        # if "600" != error:
        #     raise ValueError(ERROR_CODES[error])
        cls.parse_api_message2(message, True)

    @classmethod
    def get_location(cls, message):
        # [error, results] = cls.parse_api_message(message)
        # if "600" != error:
        #     raise ValueError(ERROR_CODES[error])
        results = cls.parse_api_message2(message, True)
        results = {
            'latitude':float(results[0]),
            'longitude':float(results[1]),
            'seconds_since_last_fix':int(results[2]),
            'seconds_until_next_fix':int(results[3]),
            'altitude':float(results[4])
        }

        return results

    @classmethod
    def set_location(cls, message):
        # [error, results] = cls.parse_api_message(message)
        # if "600" != error:
        #     raise ValueError(ERROR_CODES[error])
        results = cls.parse_api_message2(message, True)
        results = {
            'latitude':float(results[0]),
            'longitude':float(results[1]),
            'seconds_since_last_fix':int(results[2]),
            'seconds_until_next_fix':int(results[3]),
            'altitude':float(results[4])
        }

        return results
    @classmethod
    def get_datetime(cls, message):
        # [error, results] = cls.parse_api_message(message)
        # if "600" != error:
        #     raise ValueError(ERROR_CODES[error])
        results = cls.parse_api_message2(message, True)
        return {'datetime':results[0]}

    @classmethod
    def set_datetime(cls, message):
        # [error, results] = cls.parse_api_message(message)
        # if "600" != error:
        #     raise ValueError(ERROR_CODES[error])
        results = cls.parse_api_message2(message, True)
        return {'datetime':results[0]}

    @classmethod
    def get_next_alarm(cls, message):
        # [error, results] = cls.parse_api_message(message)
        # if "600" != error:
        #     raise ValueError(ERROR_CODES[error])
        results = cls.parse_api_message2(message, True)
        results = {
            'alarm_id':int(results[0]),
            'seconds_left_until_alarm':int(results[1])
        }
        return results

    @classmethod
    def get_next_pass(cls, message):
        # [error, results] = cls.parse_api_message(message)
        # if "600" != error:
        #     raise ValueError(ERROR_CODES[error])
        results = cls.parse_api_message2(message, True)
        return {'seconds_left_until_pass':int(results[0])}
        

    @classmethod
    def go_to_sleep(cls, message):
        # [error, results] = cls.parse_api_message(message)
        [error, results] = cls.parse_api_message2(message, False)
        if "603" == error:
            raise Warning(error)
        elif ("600" != error) and ("602" != error):
            raise ValueError(ERROR_CODES[error])
        results = {
            'seconds_left_until_alarm':int(results[0]),
            'alarm_id':int(results[1])
        }
        return results

    @classmethod
    def toggle_payload_over_debug(cls, message):
        # [error, results] = cls.parse_api_message(message)
        # if "600" != error:
        #     raise ValueError(ERROR_CODES[error])
        results = cls.parse_api_message2(message, True)
        return {'toggle_enabled':bool(results[0])}

    @classmethod
    def set_payload(cls, message):
        results = cls.parse_api_message2(message, True)
        print(results)

        return {'payload_bytes':int(results[0])}

        # [error, results] = cls.parse_api_message(message)
        # if "600" != error:
        #     raise ValueError(ERROR_CODES[error])
        # return {'payload_bytes':int(results[0])}