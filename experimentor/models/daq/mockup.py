# -*- coding: utf-8 -*-
"""
    ni6251.py
    ---------
    Class for comunicating with the NI-6251 DAQ. It requires to have installed the DAQmx (provided by NI) and the
    pyDAQmx package (from pypy). It does not check for dependencies automatically, so it is up to the user to have them.
    This model is far from complete; the place to start is the
    `DAQmx C Reference <http://zone.ni.com/reference/en-XX/help/370471AA-01/>`_

     .. sectionauthor:: Aquiles Carattino <aquiles@uetke.com>
"""
import logging
import time

import numpy as np

from experimentor import Q_
from ._skeleton import Daq
from ...config.config_mockup import ConfigMockup as Config
from ...lib.general_functions import from_units_to_volts, from_volts_to_units
logger = logging.getLogger(__name__)


class NI(Daq):
    model = "6251"
    def __init__(self, daq_num=1):
        self.daq_num = daq_num
        self.monitorNum = []
        self.tasks = []
        self.logger = logging.getLogger(__name__)
        self.logger.info('Started NI instrument with number: {}'.format(daq_num))

    def apply_value(self, actuator, value):
        pass

    def read_value(self, sensor):
        pass

    def analog_input_setup(self, conditions):
        self.conditions = conditions
        return 1

    def trigger_analog(self, task=None):
        pass

    def read_analog(self, task, conditions):
        points = self.conditions['points']
        data = np.random.random(self.conditions['points'])
        x = np.linspace(-10, 10, points)
        y = np.exp(-x**2)
        return points, y

    def from_volt_to_units(self, value, dev):
        pass

    def from_units_to_volts(self, value, dev):
        """ Converts a value from specific actuator units into volts to pass to a DAQ.

        :param value: The output value
        :param dev: The calibration of the device, including units.
        :type value: Quantity
        :type dev: dict.
        """
        units = Q_(dev.properties['calibration']['units'])
        slope = dev.properties['calibration']['slope'] * units
        offset = dev.properties['calibration']['offset'] * units
        value = value.to(units)
        value = value.m
        slope = slope.m
        offset = offset.m
        return (value - offset) / slope

    def analog_output_dc(self, conditions):
        pass

    def analog_output_samples(self, conditions):
        pass

    def is_task_complete(self, task=None):
        return True

    def stop_task(self, task):
        pass

    def clear_task(self, task):
        pass

    def reset_device(self):
        pass