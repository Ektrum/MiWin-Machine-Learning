#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 09:26:03 2017

@author: carlosrodriguez
"""

import unittest
import numpy as np
import numpy.testing as npt

from sharc.antenna.antenna_s1855 import AntennaS1855
from sharc.parameters.parameters_fss_es import ParametersFssEs


class AntennaS1855Test(unittest.TestCase):

    def setUp(self):
        # Earth Station Antenna parameters
        params = ParametersFssEs()
        params.diameter = 9.1
        params.frequency = 27200
        params.antenna_gain = 62
        params.azimuth = 0
        params.elevation = 0

        # Create antenna FSS Earth Station objects
        self.antenna = AntennaS1855(params)

    def test_get_gain(self):
        # phi = 7
        # phi = 8 with second part of equation
        # phi = 15, the third part of the equation
        # phi = 15, the third part of the equation
        phi = np.array([7, 8, 15, 100])
        theta = np.array([90, 45, 45, 45])
        expected_result = np.array([0, 0, 0, 0])
        gain = self.antenna.calculate_gain(phi_vec=phi, theta_vec=theta)
        # npt.assert_array_almost_equal(gain, expected_result)


if __name__ == '__main__':
    unittest.main()
