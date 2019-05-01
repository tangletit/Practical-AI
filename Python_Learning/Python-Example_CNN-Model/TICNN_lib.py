# ======================================================================================
# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """
# Created on Mon Nov  5 11:33:59 2018
# @author: Masterarbeit_Junning_Zhang
# Function library of for TICNN 
# log:
# -> 15.10.2018, overlap function
# -> 05.11.2018, DataSegment function
# -> 01.11.2018, First Version DE_time_train
# -> 08.11.2018, new Version according to the Dataloader code by Jose
# -> 13.11.2018, OverlapDeg funtion
# -> 14.11.2018, Dataloader supports multiple Datasets as input(exp. DatatestA + DatasetB)  
# ======================================================================================
#import scipy.io as sio
import os
import torch
import torch.utils.data as data
import numpy as np
import h5py
# ======================================================================================
# Dataloader
class TICNN_DataloaderCWRU(data.Dataset):
#Input var range:
# sH5File: dir of hdf5 file
# lDataset: [], input value contains:‘A’,‘B’,‘C’,‘D’. Example: [‘A’,‘B’,‘D’]
# iBatch_size: batch size
# bFlagTrain: True, False(True:for training, False: for test)
# bshuffle: 
    def __init__(self, sH5File, lDataset, bFlagTrain):
        # Input vars check
        if os.path.exists(str(sH5File)) == False:
            raise AssertionError('The input file was not found.')
            return
        for i in lDataset:
            if str.upper(i) not in ['A','B','C','D']:
                raise AssertionError("Dataset index should be the element in ['A','B','C'.'D']")
                return
        
        self.f = h5py.File(sH5File, "r")
        # list of selected Datasets
        self.Dataset = []
        for i in range(len(lDataset)):
            DatasetName = 'Dataset' + str.upper(lDataset[i])
            self.Dataset.append(DatasetName)
        # Training or Test
        if bFlagTrain == True:
            self.lSignalName = ['DE_time_train','FE_time_train']
        elif bFlagTrain == False:
            self.lSignalName = ['DE_time_test','FE_time_test']
        
        self.length = 0
        self.length_group = 0
        self.SampleIndex = list() # list of sample's Info(Group, Subgroup, index)
        
        for Group in self.Dataset:
            self.lSubgroup = list(self.f[Group].keys())
            for Subgroup in self.lSubgroup:
                 # get total sample's number in Subgroup and SampleIndex 
                length_subgroup = len(self.f[Group][Subgroup][self.lSignalName[0]])
                self.length_group = self.length_group + length_subgroup
                
                # list of sample's Info(Group, Subgroup, index)
                for j in range(length_subgroup):
                    # for attribute list.append, there is no return value of attribute 
                    self.SampleIndex.append([Group, Subgroup, j])
                    
            self.length = self.length + self.length_group
            self.length_group = 0 # ready accumulative calculation for next group
                  
        self.data = np.zeros(shape=(self.length, 2, 2048))
        self.classes = np.zeros(shape=(self.length))
        
        # assign all samples&class data to self.data & self.classes 
        for i in range(self.length):
            index = self.SampleIndex[i]
            self.data[i,0,:] = self.f[index[0]][index[1]][self.lSignalName[0]][index[2],:]
            self.data[i,1,:] = self.f[index[0]][index[1]][self.lSignalName[1]][index[2],:]
            self.classes[i] = self.f[index[0]][index[1]][self.lSignalName[0]].attrs['class']
        self.f.close()
        
    def __len__(self):
        return int(self.length)
    
    def __getitem__(self, SampleIndex):          
        if SampleIndex > self.length:
            raise AssertionError('Perhaps, you should reduce the values of input var: SampleIndex')
#        Sample = self.data[SampleIndex,:,:]
#        SampleClass = self.classes[SampleIndex]    
        Sample = torch.from_numpy(self.data[SampleIndex,:,:])
        Sample = Sample.float()
#        Sample = torch.unsqueeze(Sample, dim=0)
        SampleClass = torch.tensor(self.classes[SampleIndex])
        SampleClass = SampleClass.float()
        return Sample, SampleClass    
# ======================================================================================
# Dataloader for to load TU Berlin MDT experiments data
class TICNN_DataloaderMDT():
    def __init__(self, mc=True, rpm=150, train=True):
        if mc == True: # mc is short for MotorCurrent 
            filename_front = 'ae2mc_'
        else:
            filename_front = 'ae2cv_'
        if train == True:
            filename_end = '_train'
        else:
            filename_end = '_test' 
        self.filename = filename_front+str(rpm)+'rpm'+filename_end+'.h5' # input .h5 filename
        print(self.filename)
         # filename check, if not found, raise error
        if os.path.exists('Data_MDT/' + self.filename) == False:
            raise AssertionError('The input file was not found: '+self.filename)
            return
 
        self.f = h5py.File('Data_MDT/'+self.filename, "r") # open the corresponding .h5 file
        exp = list(self.f) # list of frist Group layer(exp)
        measurement = list(self.f[exp[0]]) # list of second Group layer(measurement)
        self.dataANDtarget = [] # to output list, include 'data' & 'target' of each measurement
        
        for i in range(len(measurement)):
            data_array = self.f[exp[0]][measurement[i]]['data'][:]
            target_array = self.f[exp[0]][measurement[i]]['target']
            target = sum(target_array)/len(target_array)  # take the mean of the target 
            self.dataANDtarget.append([data_array,target])
        self.length = len(self.dataANDtarget)
        self.f.close()

    def __len__(self):
        return self.length
        
    def __getitem__(self, MeasurementIndex):   
        if MeasurementIndex > self.length:
            raise AssertionError('Perhaps, you should reduce the values of input var: MeasurementIndex')
        self.Measurement = self.dataANDtarget[MeasurementIndex]
        return MeasurementIndex, self.Measurement[0],self.Measurement[1] # MeasurementIndex, data, target
        
# ======================================================================================
#Function description -> OverlapDeg:
#    automatically calculate the overlap degree, in oder to make use of more data
def OverlapDeg(data, start_point, s_length, s_num):
    if len(data) >= s_length * s_num + start_point:
        deg = 0
        return deg
    else:
        deg = 1 - (len(data) - start_point - s_length) / (s_length * (s_num - 1))
        if deg >= 0.99999:
            raise AssertionError ('Overlap degree has exceeded 99.999%, please check the data again')
        deg = np.ceil(deg * 100)/100 # take three decimal, round up
        return deg
    
# ======================================================================================
#Function description -> Overlap:
#    usesd to perform overlap function / data slicing operation
#    Input variables:
#    Data: original data to be operated(array)
#    start_p: start point for slicing operation (int)
#    s_length: number of points that each sample contains (int)
#    s_number: number of samples to get (int)
#    fDeg: degree of overlap(bool, 0~1)
def Overlap(Data, start_p, s_length, s_number, fDeg):
    if not(isinstance(start_p,int)) or not(isinstance(s_number,int)) or not(isinstance(s_length,int)):
        raise AssertionError('Please einter an integer for input vvariables: start_p, s_length and s_number')
        return
    Data = np.array(Data)
    # define output array
    output = np.zeros([s_number, s_length], dtype = float)
    for i in range(s_number):
        # define start and end points of a sample 
        start = start_p + (i * int((1 - fDeg) * s_length))
        end = start + s_length
        sample = Data[start:end].reshape(s_length)
        # assign data to the output
        output[i] = sample   
    return output

# ======================================================================================
#Function description -> DataSegment:
#    used to segment(divisive) data
#    Input variables:
#    Data: to be segmented data（!!! vector form）
#    percent: proportion of output data (0~1)
def DataSegment(Data, percent):
    if percent<0 and percent>1:
        raise AssertionError('Input percent should be between 0 and 1.')
        return
    length = len(Data)
    output_a = Data[0:int(length * percent)]
    output_b = Data[int(length * percent):]
    output =[output_a, output_b] 
    return output  
# ====================================================================================== 
# Max Min Normalization
def MaxMinNorm(x, Max, Min): 
    x = (x - Min) / (Max - Min)
    return x

# ======================================================================================
# Z-score Normalization
def Z_ScoreNorm(x, mu, sigma):
	x = (x - mu) / sigma
	return x

# ======================================================================================
# Add additive white Gaussian noise, given SNR(dB) & discrete signal data
def AddAWGN(SNR, signal_raw):
#    if len(signal_raw) != 2048:
#        raise AssertionError('There is size error of Input(signal_raw) of function TICNN.lib.AddAWGN')
#        return
    signal_power = sum(abs(signal_raw[:])**2)/len(signal_raw)
    noise_power = signal_power / pow(10,SNR/10)
    noise =np.sqrt(noise_power) * (np.random.normal(0,1,len(signal_raw)))
    signal_AddAWGN = signal_raw[:] + noise[:]
    return signal_AddAWGN

	