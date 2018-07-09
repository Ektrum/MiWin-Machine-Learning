# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 15:28:06 2018

@author: Calil
"""

import unittest
import numpy as np
import numpy.testing as npt
import os
import pandas as pd

from sharc.simulation_imt_vale_downlink import SimulationImtValeDownlink
from sharc.parameters.parameters import Parameters
from sharc.station_factory import StationFactory
from sharc.propagation.propagation_factory import PropagationFactory


class SimulationImtValeTest(unittest.TestCase):

    def setUp(self):
        self.our_path = os.path.dirname(__file__)
        self.param = Parameters()
        self.param.set_file_name(os.path.join("..","learning","input","parameters_general_q_testing.ini"))
        self.param.read_params()
        
        self.random_number_gen = np.random.RandomState(seed=101)
        
        self.polygon_centroid = np.array([669113.02907,7802880.51841])
        
        self.max_distance = 2500
        self.distance_increment = 500
        self.positions_num = int(np.ceil(self.max_distance/self.distance_increment))
        position_variations = np.vstack((np.arange(0,self.max_distance,self.distance_increment),
                                         np.zeros(self.positions_num)))
        self.position_variations = np.transpose(position_variations)
        
        self.allowed_positions = self.position_variations + self.polygon_centroid
        
        self.sinr_vals = list()
        self.sinr_avgs = list()
        self.sinr_max = list()

    def test_simulation_bs_positions_downlink(self):
        
        for position in self.allowed_positions:
            
#            print(position)
            bs_data_df = pd.read_excel(self.param.imt.bs_physical_data_file)
            bs_data_df['dWECoordinateMeter'] = position[0]
            bs_data_df['dSNCoordinateMeter'] = position[1]
            bs_data_df.to_excel(self.param.imt.bs_physical_data_file)
            self.param.read_params()
            
            self.simulation = SimulationImtValeDownlink(self.param)
            self.simulation.initialize()

            self.simulation.propagation_imt = PropagationFactory.create_propagation(self.param.imt.channel_model,
                                                                                    self.param,
                                                                                    self.random_number_gen)
            
            self.simulation.topology.calculate_coordinates(self.random_number_gen)
        
        
            self.simulation.ue = StationFactory.generate_imt_ue_vale_outdoor(self.param.imt,
                                                                             self.param.antenna_imt,
                                                                             self.random_number_gen,
                                                                             self.simulation.topology)  
            
            self.simulation.bs = StationFactory.generate_imt_vale_base_stations(self.param.imt,
                                                                                self.param.antenna_imt,
                                                                                self.simulation.topology,
                                                                                self.random_number_gen)
            
#            self.simulation.plot_scenario()
        
            # Associating UEs and BSs based on the RSSI
            self.simulation.connect_ue_to_bs(self.simulation.parameters.imt)

            # Calculate coupling loss
            self.simulation.coupling_loss_imt = self.simulation.calculate_coupling_loss(self.simulation.bs,
                                                                                        self.simulation.ue,
                                                                                        self.simulation.propagation_imt)
            # Allocating and activating the UEs
            self.simulation.scheduler()

            self.simulation.power_control()

            self.simulation.calculate_sinr()
            
            self.sinr_vals.append(self.simulation.ue.sinr)
            
        for sinr in self.sinr_vals:
            self.sinr_avgs.append(np.mean(sinr))
            self.sinr_max.append(np.amax(sinr))
            
        self.assertTrue(all(self.sinr_avgs[i] >= self.sinr_avgs[i+1] for i in range(len(self.sinr_avgs)-1)))
        self.assertTrue(all(self.sinr_max[i] >= self.sinr_max[i+1] for i in range(len(self.sinr_max)-1)))

if __name__ == '__main__':
    unittest.main()
