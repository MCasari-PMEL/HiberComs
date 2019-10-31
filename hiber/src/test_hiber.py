import pytest
import datetime as dt

from hiber import Hiber




def test_hiber_class_should_raise_exception_for_invalid_baudrate():
    with pytest.raises(ValueError):
        h=Hiber('COM1', 1234)

def test_hiber_class_should_raise_exception_for_invalid_com_port():
    with pytest.raises(ValueError):
        h=Hiber('C1',19200)

def test_hiber_class_should_raise_exception_for_invalid_com_port_string():
    with pytest.raises(ValueError):
        h=Hiber('COM12a', 9600)

def test_hiber_class_should_init_with_correct_com_and_baudrate():
    h = Hiber('COM1',57600)

    assert h._ser.port == 'COM1'
    assert h._ser.baudrate == 57600
