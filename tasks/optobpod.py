#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 11:01:44 2019
Optobpod 0.0.1
Function for controlling opto stim in bpod
Currently states with stim are manually added to the task at the relevant state
@author: ibladmin

"""
import numpy as np

def opto_switch(opto_on, opto_freq):
    if opto_on==True:
        switch = np.random.choice([0,1], p= [1 - opto_freq, opto_freq])
    else:
        switch = 0
    return switch  