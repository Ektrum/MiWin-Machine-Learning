# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 17:12:38 2018

@author: Calil
"""

from abc import ABC, abstractmethod

class Action(ABC):
    """
    Abstract class to serve as super-class for all actions.
    Attributes:
        self.description (str): description of the action. All actions must
            have a description
    Methods:
        self.act(): Returns True if action can be succesfully performed and 
            False otherwise. If it can be performed, then it performs the action.
    """
    def __init__(self,description: str):
        """
        Class constructor.
        
        Parameters:
            description (str): action description
        """
        self.description = description
        
    @abstractmethod
    def act(self):
        """
        Returns True if action can be succesfully performed and False 
        otherwise. If it can be performed, then it performs the action.
        
        Return:
            can_perform (bool): True if action can be performed, False 
                otherwise.
        """
        pass
    
    def __str__(self):
        return self.description