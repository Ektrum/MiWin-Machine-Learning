# -*- coding: utf-8 -*-

"""
Created on  Mar  04 14:13:31 2017

@author:  LeticiaValle_Mac
"""

import unittest
import numpy as np
import numpy.testing as npt


from sharc.propagation.propagation_ABG import PropagationABG

class PropagationABGTest(unittest.TestCase):
    
    def setUp(self):
        self.abg = PropagationABG()
        
    def test_loss(self):
        d = 100
        f = 27000
        alpha = 3.4
        beta = 19.2
        gamma = 2.3
        shadowing = 0
        
       
        npt.assert_allclose(self.abg.get_loss(distance = d, frequency = f, ABG_alpha = alpha, ABG_beta = beta, ABG_gamma = gamma, shadowing = shadowing),
                             120.121,atol=1e-2)

        d = np.array([500, 3000])
        f = np.array([27000, 40000])
        alpha = 3.4
        beta = 19.2
        gamma = 2.3
        shadowing = 6.5
        
        loss = np.array ([155.352, 185.735])
        npt.assert_allclose(self.abg.get_loss(distance = d, frequency = f, ABG_alpha = alpha, ABG_beta = beta, ABG_gamma = gamma, shadowing = shadowing),
                           loss ,atol=1e-2)
