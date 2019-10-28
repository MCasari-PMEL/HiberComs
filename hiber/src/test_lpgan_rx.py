
import pytest
import datetime as dt


from hiber import LPGAN_API_Rx

#------------------------------
# Parsing Rx strings 
#------------------------------
def test_parse_api_return_should_fail_for_bad_return_string():
    # Valid returns strings start with API or Hiber API
    with pytest.raises(ValueError):
        LPGAN_API_Rx.parse_api_message2('Invalid entry')

def test_parse_api_should_split_error_codes():
    assert ['600', []] == LPGAN_API_Rx.parse_api_message2('API(600)\r\n')

def test_parse_api_should_split_error_and_single_value_return():
    assert ['600', ['20']] == LPGAN_API_Rx.parse_api_message2('API(600: 20)') 

def test_parse_api_should_split_error_and_multiple_value_returns():
    assert ['600', ['20','40','60', '80','100']] == LPGAN_API_Rx.parse_api_message2('API(600: 20; 40; 60; 80;100)\r\n')

def test_parse_api_should_split_and_ignore_funky_time_post_message_bs():
    api = 'API(600: 2019-02-25T16:13:38Z) Current date: 2019-02-25T16:13:38Z\r\n'
    results = LPGAN_API_Rx.parse_api_message2(api)

    assert ['600', ['2019-02-25T16:13:38Z']] == results

def test_set_gps_mode_should_pass_and_return_single_boolean():
    assert False == LPGAN_API_Rx.set_gps_mode('API(600: 0)\r\n')

def test_set_gps_mode_should_fail_and_raise_exception():
    with pytest.raises(ValueError):
        LPGAN_API_Rx.set_gps_mode('API(525)')

def test_do_gps_fix_should_pass_and_return_nothing():
    assert None == LPGAN_API_Rx.do_gps_fix('API(600)\r\n') 

def test_do_gps_fix_should_raise_exception_for_error():
    with pytest.raises(ValueError):
        LPGAN_API_Rx.do_gps_fix('API(136)\r\n')

def test_get_firmware_version_should_return_firmware_version():
    result =  LPGAN_API_Rx.get_firmware_version('API(600: cn-release-v1.0.0-1-gd193bbe4)')

    expected_result = 'cn-release-v1.0.0-1-gd193bbe4'

    assert expected_result == result['firmware_version']

def test_get_firmware_should_raise_expcetion_for_error():
    with pytest.raises(ValueError):
        LPGAN_API_Rx.get_firmware_version('API(136)')


def test_get_modem_info_should_return_all_modem_info():
    api = 'API(600: GAMMA; 2; 1; 27AA 0DD8; 665456088)\r\n'
    results = LPGAN_API_Rx.get_modem_info(api)

    assert 'GAMMA' == results['HW_TYPE_STR']
    assert 2 == results['HW_TYPE_INT']
    assert '1' == results['FW_VERSION']
    assert '27AA 0DD8' == results['MODEM_NO_STR']
    assert 665456088 == results['MODEM_NO_INT']

def test_get_modem_info_should_raise_exception_for_error():
    with pytest.raises(ValueError):
        LPGAN_API_Rx.get_modem_info('API(136)')

def test_set_modem_number_should_pass_and_return_none():
    assert None == LPGAN_API_Rx.set_modem_number('API(600)\r\n')

def test_get_location_should_pass_and_return_values():
    api = 'API(600: 0.000000; 0.000000; 136121891; -2147483648; 0.000000)\r\n'
    results = LPGAN_API_Rx.get_location(api)

    assert 0.0 == results['latitude']
    assert 0.0 == results['longitude']
    assert 136121891 == results['seconds_since_last_fix']
    assert -2147483648 == results['seconds_until_next_fix']
    assert 0.000000 == results['altitude']

def test_get_location_should_raise_exception_for_error():
    with pytest.raises(ValueError):
        LPGAN_API_Rx.get_location('API(136)')

def test_set_location_should_pass_and_return_values():
    api = 'API(600: 54.333229; 4.212332; -157938633; -2147483648; 0.000000)\r\n'
    results = LPGAN_API_Rx.set_location(api)

    assert 54.333229 == results['latitude']
    assert 4.212332 == results['longitude']
    assert -157938633 == results['seconds_since_last_fix']
    assert -2147483648 == results['seconds_until_next_fix']
    assert 0.000000 == results['altitude']

def test_set_location_should_raise_exceptions_for_errors():
    with pytest.raises(ValueError):
        LPGAN_API_Rx.set_location('API(225)')

def test_get_datetime_should_pass_and_return_valid_datetime():
    api = 'API(600: 2019-02-25T16:14:40Z)'
    results = LPGAN_API_Rx.get_datetime(api)
    assert '2019-02-25T16:14:40Z' == results['datetime']

def test_get_datetime_should_raise_exception_for_error():
    with pytest.raises(ValueError):
        LPGAN_API_Rx.get_datetime('API(225)')

def test_set_datetime_should_pass_and_return_valid_datetime():
    api = 'API(600: 2019-02-25T16:13:38Z) Current date: 2019-02-25T16:13:38Z\r\n'
    results = LPGAN_API_Rx.set_datetime(api)
    assert '2019-02-25T16:13:38Z' == results['datetime']

def test_set_datetime_should_raise_exception_for_errors():
    with pytest.raises(ValueError):
        LPGAN_API_Rx.set_datetime('API(225)')

def test_get_next_alarm_should_return_valid_values():
    api = 'API(600: 3; 39)\r\n'

    results = LPGAN_API_Rx.get_next_alarm(api)

    assert 3 == results['alarm_id']
    assert 39 == results['seconds_left_until_alarm']

def test_get_next_alarm_should_raise_exception_for_error():
    with pytest.raises(ValueError):
        LPGAN_API_Rx.get_next_alarm('API(225)')

def test_get_next_pass_should_return_valid_time_until_next_pass():
    api ='API(600: 1298)'
    result = LPGAN_API_Rx.get_next_pass(api)

    assert 1298 == result['seconds_left_until_pass']

def test_get_next_pass_should_raise_exception_for_error():
    with pytest.raises(ValueError):
        LPGAN_API_Rx.get_next_pass('API(225)')

def test_go_to_sleep_should_return_valid_values():
    api = 'API(602: 36; 3)\r\n'

    results = LPGAN_API_Rx.go_to_sleep(api)

    assert 36 == results['seconds_left_until_alarm']
    assert 3 == results['alarm_id']

def test_go_to_sleep_should_raise_exception_for_error():
    with pytest.raises(ValueError):
        LPGAN_API_Rx.go_to_sleep('API(225)')

def test_go_to_sleep_should_raise_warning_for_pin_high():
    with pytest.raises(Warning):
        LPGAN_API_Rx.go_to_sleep('API(603: 36; 3)')

def test_toggle_payload_over_debug_should_return_valid_values():
    api = 'API(600: 1)\r\n'

    result = LPGAN_API_Rx.toggle_payload_over_debug(api)

    assert True == result['toggle_enabled']

def test_toggle_payload_over_debug_should_raise_exception_for_errors():
    with pytest.raises(ValueError):
        LPGAN_API_Rx.toggle_payload_over_debug('API(136: 1, 12)\r\n')

def test_set_payload_should_return_valid_count():
    api = 'API(600: 140)\r\n'
    result = LPGAN_API_Rx.set_payload(api)
    assert 140 == result['payload_bytes']

def test_set_payload_should_raise_excpetion_for_error():
    with pytest.raises(ValueError):
        LPGAN_API_Rx.set_payload('API(127: 127)\r\n') 