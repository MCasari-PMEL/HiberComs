import pytest
import datetime as dt

from hiber import LPGAN_API

def test_set_gps_mode_return_valid_string():
    l = LPGAN_API()

    expected_string = 'set_gps_mode(true)\r\n'

    assert expected_string == l.set_gps_mode(True)

def test_set_gps_mode_raise_exception_for_non_boolean():
    with pytest.raises(ValueError):
        LPGAN_API.set_gps_mode('Failure')

def test_do_gps_fix_no_input_string():
    expected_string = 'do_gps_fix\r\n'

    assert expected_string == LPGAN_API.do_gps_fix()

def test_do_gps_fix_with_input_string():
    input_string = '12345,223452'
    expected_string = f'do_gps_fix(\"{input_string}\")\r\n'

    assert expected_string == LPGAN_API.do_gps_fix(input_string)

def test_do_gps_fix_with_input_int_instead_of_string_should_fail():
    input_value = 1234.5

    with pytest.raises(ValueError):
        LPGAN_API.do_gps_fix(input_value)

def test_get_firmware_version_should_create_valid_string():
    assert 'get_firmware_version\r\n' == LPGAN_API.get_firmware_version()

def test_get_modem_info_should_create_valid_string():
    assert 'get_modem_info\r\n' == LPGAN_API.get_modem_info()

def test_set_modem_number_should_create_valid_string():
    modem_number = 'ABCD 1234'
    expected_string = f'set_modem_number({modem_number})\r\n'
    assert expected_string == LPGAN_API.set_modem_number(modem_number)

def test_set_modem_number_fails_if_non_string_passed():
    modem_number = 12345678
    with pytest.raises(ValueError):
        LPGAN_API.set_modem_number(modem_number)

def test_set_modem_number_should_fail_for_invalid_string_missing_middle_space():
    modem_number = 'ABCD1234'
    with pytest.raises(ValueError):
        LPGAN_API.set_modem_number(modem_number)

def test_get_location_should_create_valid_string():
    assert 'get_location\r\n' == LPGAN_API.get_location()

def test_set_location_should_create_valid_string():
    lat = 52.333233
    lon = 4.212332
    elev = 0.0


    expected_string = f'set_location(\"{lat}\",\"{lon}\",\"{elev}\")\r\n'

    assert expected_string == LPGAN_API.set_location(lat,lon,elev)

def test_set_location_should_fail_for_non_numeric_latitudes():
    lat = 'A3'
    lon = 4.212332
    elev = 0.0

    with pytest.raises(ValueError):
        LPGAN_API.set_location(lat,lon,elev)

def test_set_location_should_fail_for_non_numeric_longitude():
    lat = 4.212332
    lon = 'B2'
    elev = 0.0

    with pytest.raises(ValueError):
        LPGAN_API.set_location(lat,lon,elev)

def test_set_location_should_fail_for_non_numeric_elevation():
    lon = 62.33232
    lat = 4.212332
    elev = 'C1'

    with pytest.raises(ValueError):
        LPGAN_API.set_location(lat,lon,elev)

def test_get_datetime_should_create_valid_string():
    assert 'get_datetime\r\n' == LPGAN_API.get_datetime()

def test_set_datetime_should_create_valid_string():
    d = dt.datetime(year=2019, month=10, day=25, hour=10, minute=59, second=48)
    assert 'set_datetime(\"2019-10-25T10:59:48Z\")\r\n' == LPGAN_API.set_datetime(d)

def test_set_datetime_should_fail_for_non_datetime_value_input():
    with pytest.raises(ValueError):
        LPGAN_API.set_datetime(2019)

def test_get_next_alarm_should_create_valid_string():
    assert 'get_next_alarm\r\n' == LPGAN_API.get_next_alarm()

def test_get_next_pass_should_create_a_valid_string():
    assert 'get_next_pass\r\n' == LPGAN_API.get_next_pass()

def test_go_to_sleep_should_create_a_valid_string():
    assert 'go_to_sleep\r\n' == LPGAN_API.go_to_sleep()

def test_toggle_payload_over_debug_should_create_valid_string():
    assert 'toggle_payload_over_debug(true)\r\n' == LPGAN_API.toggle_payload_over_debug(True)

def test_toggle_payload_over_debug_should_fail_for_non_boolean_input():
    with pytest.raises(ValueError):
        LPGAN_API.toggle_payload_over_debug(1)

def test_set_payload_should_create_a_valid_string():
    payload_length = 20
    assert 'set_payload(\"20\")\r\n' == LPGAN_API.set_payload(payload_length)

def test_set_payload_fails_for_non_integer_input():
    payload_length = 20.1
    with pytest.raises(ValueError):
        LPGAN_API.set_payload(payload_length)