# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 17:12:38 2018

@author: Calil
"""

from abc import ABC, abstractmethod

class Reward(ABC):
    """
    Abstract class to serve as super-class for all rewards.
    Attributes:
        self.description (str): description of the rewards. All rewards must
            have a description
    Methods:
        self.pay(): returns the current reward value.
    """
    def __init__(self,description: str):
        """
        Class constructor.
        
        Parameters:
            description (str): reward description
        """
        self.description = description
        
    @abstractmethod
    def pay(self):
        """
        Calculates and returns the current reward value.
        Return:
            payment (float): current reward value
        """
        pass
    
    def __str__(self):
        return self.description