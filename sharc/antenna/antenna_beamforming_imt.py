# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 15:35:51 2017

@author: Calil
"""

import numpy as np

from sharc.antenna.antenna_element_imt import AntennaElementImt
from sharc.antenna.antenna import Antenna
from sharc.parameters.parameters_antenna_imt import ParametersAntennaImt

class AntennaBeamformingImt(Antenna):
    """
    Implements an antenna array
    
    Attributes
    ----------
        element (AntennaElementImt): antenna element
        n_rows (int): number of rows in array
        n_cols (int): number of columns in array
        dh (float): horizontal element spacing over wavelenght (d/lambda)
        dv (float): vertical element spacing over wavelenght (d/lambda)
        beams (list): vertical and horizontal tilts of beams
    """
    
    def __init__(self,param: ParametersAntennaImt, azimuth: float, elevation: float, station_type: str, txrx: str):
        """
        Constructs an AntennaBeamformingImt object.
        Does not receive angles in local coordinate system.
        
        Parameters
        ---------
            param (ParametersAntennaImt): antenna IMT parameters
            azimuth (float): antenna's physical azimuth inclination
            elevation (float): antenna's physical elevation inclination
            station_type (srt): type of station. Possible values are "BS" and
                "UE"
            txrx (srt): indicates whether it is a transmissio or reception 
                antenna. Possible values are "TX" and "RX"
        """
        self.element = AntennaElementImt(param, station_type, txrx)
        
        self.__azimuth = azimuth
        self.__elevation = elevation
        
        par = param.get_antenna_parameters(station_type,txrx)
        
        self.__n_rows = par.n_rows
        self.__n_cols = par.n_columns
        self.__dh = par.element_horiz_spacing
        self.__dv = par.element_vert_spacing
        
        self.__beams_list = []
        self.__w_vec_list = []
        
        
    def calculate_gain(self,phi_vec: np.array, theta_vec: np.array, max_g = False) -> np.array:
        """
        Calculates the gain in the given direction.
        
        Parameters
        ----------
        phi_vec (np.array): azimuth angles [degrees]
        theta_vec (np.array): elevation angles [degrees]
        max_g (bool): if True, max beam gain in direction will be given.
            
        Returns
        -------
        gains (np.array): gain corresponding to each of the given directions.
        """
        n_direct = len(theta_vec)
        
        gains = np.zeros(n_direct)
        
        for g in range(n_direct):
            if(max_g):
                gains[g] = self.max_beam_gain(phi_vec[g],theta_vec[g])
            else:
                for b in range(len(self.__beams_list)):
                    gains[g] = gains[g] + self.beam_gain(phi_vec[g],\
                         theta_vec[g],b)
        return gains
        
    @property
    def azimuth(self):
        return self.__azimuth
    
    @property
    def elevation(self):
        return self.__elevation
    
    @property
    def n_rows(self):
        return self.__n_rows
    
    @property
    def n_cols(self):
        return self.__n_cols
    
    @property
    def dh(self):
        return self.__dh
    
    @property
    def dv(self):
        return self.__dv
    
    @property
    def beams_list(self):
        return self.__beams_list
    
    @property
    def w_vec_list(self):
        return self.__w_vec_list
    
    def add_beam(self, phi_etilt: float, theta_etilt: float):
        """
        Add new beam to antenna.
        Does not receive angles in local coordinate system.
        
        Parameters
        ----------
            phi_etilt (float): azimuth electrical tilt angle [degrees]
            theta_etilt (float): elevation electrical tilt angle [degrees]
        """
        phi, theta = self.to_local_coord(phi_etilt,theta_etilt)
        self.__beams_list.append((phi,90 - theta))
        self.__w_vec_list.append(self.weight_vector(phi,90 - theta))
    
    def super_position_vector(self,phi: float, theta: float) -> np.array:
        """
        Calculates super position vector.
        Angles are in the local coordinate system.
        
        Parameters
        ----------
            theta (float): elevation angle [degrees]
            phi (float): azimuth angle [degrees]
            
        Returns
        -------
            v_vec (np.array): superposition vector
        """
        r_phi = np.deg2rad(phi)
        r_theta = np.deg2rad(theta)
        
        n = np.arange(self.n_rows) + 1
        m = np.arange(self.n_cols) + 1
        
        exp_arg = (n[:,np.newaxis] - 1)*self.dv*np.cos(r_theta) + \
                  (m - 1)*self.dh*np.sin(r_theta)*np.sin(r_phi)
        
        v_vec = np.exp(2*np.pi*1.0j*exp_arg)
        
        return v_vec
        
    def weight_vector(self, phi_tilt: float, theta_tilt: float) -> np.array:
        """
        Calculates super position vector.
        Angles are in the local coordinate system.
        
        Parameters
        ----------
            phi_tilt (float): electrical horizontal steering [degrees]
            theta_tilt (float): electrical down-tilt steering [degrees]
            
        Returns
        -------
            w_vec (np.array): weighting vector
        """
        r_phi = np.deg2rad(phi_tilt)
        r_theta = np.deg2rad(theta_tilt)
        
        n = np.arange(self.n_rows) + 1
        m = np.arange(self.n_cols) + 1
        
        exp_arg = (n[:,np.newaxis] - 1)*self.dv*np.sin(r_theta) - \
                  (m - 1)*self.dh*np.cos(r_theta)*np.sin(r_phi)
        
        w_vec = (1/np.sqrt(self.n_rows*self.n_cols))*\
                np.exp(2*np.pi*1.0j*exp_arg)
        
        return w_vec        
    
    def beam_gain(self,phi: float, theta: float, beam: int) -> float:
        """
        Calculates gain for a single beam in a given direction.
        
        Parameters
        ----------
            phi (float): azimuth angle [degrees]
            theta (float): elevation angle [degrees]
            phi_scan (float): electrical horizontal steering [degrees]
            theta_tilt (float): electrical down-tilt steering [degrees]
            
        Returns
        -------
            gain (float): beam gain [dBi]
        """
        element_g = self.element.element_pattern(phi,theta)
        
        v_vec = self.super_position_vector(phi,theta)
        
        array_g = 10*np.log10(abs(np.sum(np.multiply(v_vec,\
                                            self.__w_vec_list[beam])))**2)
        
        gain = element_g + array_g
        
        return gain
    
    def max_beam_gain(self, phi: float, theta: float) -> float:
        """
        Calculates maximum possible beam gain in a given direction.
        Angles are in the local coordinate system.
        
        Parameters
        ----------
            phi (float): azimuth angle [degrees]
            theta (float): elevation angle [degrees]
            
        Returns
        -------
            gain (float): beam gain [dBi]
        """
        element_g = self.element.element_pattern(phi,theta)
        
        v_vec = self.super_position_vector(phi,theta)
        w_vec = self.weight_vector(phi,90-theta)
        
        array_g = 10*np.log10(abs(np.sum(np.multiply(v_vec,w_vec)))**2)
        
        gain = element_g + array_g
        
        return gain       
    
    def to_local_coord(self,phi: float, theta: float) -> tuple:
        return phi - self.azimuth, theta - self.elevation