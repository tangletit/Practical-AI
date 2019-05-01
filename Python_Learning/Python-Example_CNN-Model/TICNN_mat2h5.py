
# ======================================================================================
# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

# Created on Tue Aug 21 15:36:07 2018
# @author: Masterarbeit_Junning_Zhang
# log: 
# -> 15.10.2018, lack of group D
# -> 19.10.2018, lack of Drehzahl
# -> 27.10.2018, + overlap
# -> 29.10.2018, + DatasetD
# -> 30.10.2018, + Warning in overlap function
# -> 06.11.2018, no overlap part between training & test data| + DataSegment fucntion
# -> 11.12.2018, + data normalization in datasetA,B,C,D (x_new = (x - x_min)/(x_max - x_min))
# -> 18.12.2018, + from MaxMin to Z_Score standardization
#                  The recognition rate of both is not as high as the original data
# The purpose of this programm is to import mat files from Case Western Reserve 
# University Bearing Data Center Website,restructure the data and store the datasets 
# to a hdf5 files.
# http://csegroups.case.edu/bearingdatacenter/pages/download-data-file

# ================ basic variables from .mat to .h5 ====================================
#Load mat file and restructure the data through overlap.
#1. The training samples are overlapped and there is no overlap among the test samples;
#2. Dataset D is the combination of datasets A B C;
#3. For details, please refer to the excel file 'DatasetsDescription'
import scipy.io as sio
import numpy as np
import h5py
import TICNN_lib
import time 
import torch
import os
import shutil
# .h5 file name is associated with the current date
Time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
file_name = 'TICNN_' + Time + '.h5'
file = h5py.File(file_name, "w")
file = h5py.File(file_name, "r+")
# Input variables about overlap (data slicing operation)"
start_point = 0   
s_length    = 2048
s_num_train = 700
s_num_test  = 300
segment     = 0.7 # The proportion of data used for training to total data

# ================ create groups (DatasetA,B,C) ========================================
# dictionary class & corresponding fault diameter"
dict_fault = {0:0, 1:0.007, 2:0.014, 3:0.021, 
                   4:0.007, 5:0.014, 6:0.021, 
                   7:0.007, 8:0.014, 9:0.021} 
# dictionary file suffix(class) & corresponding array suffix in mat file"      
dict_datasetA = {0:'X098',1:'X119',2:'X186',3:'X223',4:'X106',
                 5:'X170',6:'X210',7:'X131',8:'X198',9:'X235'}
dict_datasetB = {0:'X099',1:'X120',2:'X187',3:'X224',4:'X107',
                 5:'X171',6:'X211',7:'X132',8:'X199',9:'X236'}
dict_datasetC = {0:'X100',1:'X121',2:'X188',3:'X225',4:'X108',
                 5:'X172',6:'X212',7:'X133',8:'X200',9:'X237'} 
for i in ['A','B','C']:
    name_group = 'Dataset' + i
    group = file.create_group(name_group)
    if i == 'A':
        dict_dataset = dict_datasetA 
    elif i == 'B':
        dict_dataset = dict_datasetB
    elif i == 'C':
        dict_dataset = dict_datasetC
    # create subgroups (A1~A9, B1~B9, C1~C9) and import data
    for j in range(0,10):
        subgroup = group.create_group(i + str(j)) # name_subgroup = i + str(j)
        #create datasets (BA_time, DE_time, FE_time, RPM)
        for k in ['DE_time','FE_time','BA_time']:
            mat_path = 'data_CWRU/'+ name_group + '/' + i + str(j) + '.mat'
            mat_file = sio.loadmat(mat_path)
            # RPM assignment
            if j != 0:
                RPM_index = dict_dataset[j] + 'RPM'
                RPM = mat_file[RPM_index]
            elif i == 'A':
                RPM = 1772
            elif i == 'B':
                RPM = 1750
            elif i == 'C':
                RPM = 1730
            
            if j!= 0 or k != 'BA_time':
                mat_prefix = dict_dataset[j] + '_' + k 
                train = np.zeros([s_num_train, s_length], dtype = float)
                test  = np.zeros([s_num_test, s_length], dtype = float)
                # with overlap funcion, restructure point data in mat and divide into train & test parts
                data  = TICNN_lib.DataSegment(np.array(mat_file[mat_prefix]), segment)
                overlap_train = TICNN_lib.OverlapDeg(data[0], start_point, s_length, s_num_train)
                overlap_test = TICNN_lib.OverlapDeg(data[1], start_point, s_length, s_num_test)
                data_train = TICNN_lib.Overlap(data[0], start_point, s_length, s_num_train, overlap_train)
                data_test = TICNN_lib.Overlap(data[1], start_point, s_length, s_num_test, overlap_test)
                # create 2 datasets(train & test)
                name_d_train = k + '_' + 'train'
                name_d_test = k + '_' + 'test'
                dataset_train = subgroup.create_dataset(name_d_train, data = data_train)
                dataset_test = subgroup.create_dataset(name_d_test, data = data_test)
                # write attribute in datasets
                if k == 'DE_time':
                    dataset_train.attrs['Variable indication'] = 'Drive end accelerometer data'
                    dataset_train.attrs['class'] = j
                    dataset_train.attrs['FaultDiameter'] = dict_fault[j]
                    dataset_train.attrs['RPM'] = RPM
                    dataset_test.attrs['Variable indication'] = 'Drive end accelerometer data'
                    dataset_test.attrs['class'] = j
                    dataset_test.attrs['FaultDiameter'] = dict_fault[j]
                    dataset_test.attrs['RPM'] = RPM
                elif k == 'FE_time':
                # write attribute in datasets
                    dataset_train.attrs['Variable indication'] = 'Fan end accelerometer data'
                    dataset_train.attrs['class'] = j
                    dataset_train.attrs['FaultDiameter'] = dict_fault[j]
                    dataset_train.attrs['RPM'] = RPM
                    dataset_test.attrs['Variable indication'] = 'Fan end accelerometer data'
                    dataset_test.attrs['class'] = j
                    dataset_test.attrs['FaultDiameter'] = dict_fault[j] 
                    dataset_test.attrs['RPM'] = RPM
                elif k == 'BA_time':
                # write attribute in datasets
                    dataset_train.attrs['Variable indication'] = 'Base accelerometer data'
                    dataset_train.attrs['class'] = j
                    dataset_train.attrs['FaultDiameter'] = dict_fault[j]
                    dataset_train.attrs['RPM'] = RPM
                    dataset_test.attrs['Variable indication'] = 'Base accelerometer data'
                    dataset_test.attrs['class'] = j
                    dataset_test.attrs['FaultDiameter'] = dict_fault[j]  
                    dataset_test.attrs['RPM'] = RPM
file.close()

# ==================== create groups (DatasetD) ========================================
#DatasetD = DatasetA + DatasetB + DatasetC
#Each dataset in DatasetD(D0...D10) contains 660*3=1980 training samples and 25*3=75 test samples
file = h5py.File(file_name, "r+")
group = file.create_group('DatasetD')
for j in range(0,10):
    name_subgroup = 'D' + str(j)
    subgroup = group.create_group(name_subgroup)
    #create datasets (BA_time, DE_time, FE_time)
    for k in ['DE_time','FE_time','BnA_time']:
        if j != 0 or k != 'BA_time':
            data_trainD = np.zeros([s_num_train*3, s_length], dtype = float)
            data_testD = np.zeros([s_num_test*3, s_length], dtype = float)
            data_trainD[0:s_num_train] = file['DatasetA']['A'+str(j)][k+'_train']
            data_trainD[s_num_train:s_num_train*2]  = file['DatasetB']['B'+str(j)][k+'_train']
            data_trainD[s_num_train*2:s_num_train*3] = file['DatasetC']['C'+str(j)][k+'_train']
            data_testD[0:s_num_test] = file['DatasetA']['A'+str(j)][k+'_test']
            data_testD[s_num_test:s_num_test*2]  = file['DatasetB']['B'+str(j)][k+'_test']
            data_testD[s_num_test*2:s_num_test*3] = file['DatasetC']['C'+str(j)][k+'_test']
            # create 2 datasets(train & test)
            name_d_train = k + '_' + 'train'
            name_d_test = k + '_' + 'test'
            dataset_train = subgroup.create_dataset(name_d_train, data = data_trainD)
            dataset_test = subgroup.create_dataset(name_d_test, data = data_testD)
            # write attribute in datasets
            if k == 'DE_time':
                dataset_train.attrs['class'] = j
                dataset_train.attrs['Variable indication'] = 'Drive end accelerometer data'
                dataset_test.attrs['class'] = j
                dataset_test.attrs['Variable indication'] = 'Drive end accelerometer data'
            elif k == 'FE_time':
                dataset_train.attrs['class'] = j 
                dataset_train.attrs['Variable indication'] = 'Fan end accelerometer data'
                dataset_test.attrs['class'] = j
                dataset_test.attrs['Variable indication'] = 'Fan end accelerometer data'
            elif k == 'BA_time':
                dataset_train.attrs['class'] = j 
                dataset_train.attrs['Variable indication'] = 'Base end accelerometer data'
                dataset_test.attrs['class'] = j
                dataset_test.attrs['Variable indication'] = 'Base end accelerometer data'
file.close()
print('create HDF5 --- completed')

# ================= Z-Score Normalization for input Datasets ===========================
# Standard deviation standardization: x_hat = (x - mean) / std
# Normalization of Training Dataset and Validation Dataset should based on same mean & variance
while True: # input whether do Z-Score Normalization, if do input the relevant datasets
    bool_normalization = str.upper(input('Do Z-Score Normalization or not (Y or N):'))
    if bool_normalization == 'Y':
        bool_norm_do = True
        break
    elif bool_normalization == 'N':
        bool_norm_do = False
        print('without Z-Score Normalization')
        break
    else:
        print('I dont understand your input')
        
if bool_norm_do:
    file = h5py.File(file_name, "r+") 
    dataset_train = str.upper(input('Please input the dataset for training(a,b,c or d):')) # input dataset for training
    dataset_eval = str.upper(input('Please input the dataset for evaluation(a,b,c or d):')) # input dataset for evaluation
    datasets_array = [dataset_train, dataset_eval]
    data_DE = torch.DoubleTensor().zero_()
    data_FE = torch.DoubleTensor().zero_()
    MeanVariance = torch.DoubleTensor(2,2).zero_() # MeanVariance=([DE_mean, DE_variance],[FE_mean, FE_variance])
    # Splice data of all datasets and calculate mean and variance
    for i in datasets_array: 
        for j in range(0,10):
            dir_index = file['Dataset'+i][i+str(j)]
            tempo_data_DE = torch.from_numpy(dir_index['DE_time_train'][:,:]) # mean&variance based only on training data
            tempo_data_FE = torch.from_numpy(dir_index['FE_time_train'][:,:])
            data_DE = torch.cat((data_DE, tempo_data_DE)) 
            data_FE = torch.cat((data_FE, tempo_data_FE)) 
    MeanVariance[0,0] = torch.mean(data_DE) # calculate mean & variance of all datasets in datasets_array
    MeanVariance[0,1] = torch.rsqrt(torch.var(data_DE))
    MeanVariance[1,0] = torch.mean(data_FE)
    MeanVariance[1,1] = torch.rsqrt(torch.var(data_FE))
    print('Mean and variacne of DE and FE based on Datasets','\n', datasets_array, '\n', MeanVariance)
    # do Z-Score normalization
    for i in datasets_array:
        for j in range(0,10):  
            dir_index = file['Dataset'+i][i+str(j)]
            for index, item in enumerate(torch.DoubleTensor(dir_index['DE_time_train'][:,:])):
                dir_index['DE_time_train'][index] = TICNN_lib.Z_ScoreNorm(item, MeanVariance[0,0], MeanVariance[0,1])
            for index, item in enumerate(torch.DoubleTensor(dir_index['DE_time_test'][:,:])):
                dir_index['DE_time_test'][index] = TICNN_lib.Z_ScoreNorm(item, MeanVariance[0,0], MeanVariance[0,1])
            for index, item in enumerate(torch.DoubleTensor(dir_index['FE_time_train'][:,:])):
                dir_index['FE_time_train'][index] = TICNN_lib.Z_ScoreNorm(item, MeanVariance[1,0], MeanVariance[1,1]) 
            for index, item in enumerate(torch.DoubleTensor(dir_index['FE_time_test'][:,:])):
                dir_index['FE_time_test'][index] = TICNN_lib.Z_ScoreNorm(item, MeanVariance[1,0], MeanVariance[1,1]) 
        if datasets_array[0] == datasets_array[1]: # if datasets of train and evaluation are same, then jump out
            break
    file.close()
    print('Z-Score Normalization --- completed')
    
# ============== Add noise based on input SNR ==========================================
#Add additive white Gaussian noise in test dataset of DE & FE signal
while True: # Determine whether add noise and the SNR value
    bool_addnoise = str.upper(input('Add noise to all datasets or not (Y or N):'))
    if bool_addnoise == 'Y':
        bool_noise = True
        while True:
            SNR = int(input('SNR(dB) of the noise is:(from -4 to 10):'))
            if (-4) <= SNR <= 10:
                break
            else:
                print('SNR out of range(-4 to 10), please input again')
        break
    elif bool_addnoise == 'N':
        bool_noise = False
        print('without noise')
        break
    else:
        print('I dont understand your input')
# Add additive white Gaussian noise
if bool_noise == True:
    file = h5py.File(file_name, "r+")
    for i in ['A','B','C','D']:
        for j in range(0,10):
            dir_index = file['Dataset'+i][i+str(j)]
            for index, item in enumerate (dir_index['DE_time_test'][:,:]):
                dir_index['DE_time_test'][:,:][index] = TICNN_lib.AddAWGN(SNR, item)
            for index, item in enumerate (dir_index['FE_time_test'][:,:]):
                dir_index['DE_time_test'][:,:][index] = TICNN_lib.AddAWGN(SNR, item)
    file.close()
    print('\n','Add noise --- completed')
# ======================================================================================
if os.path.exists("Data_TICNN") == True:
    shutil.move(file_name,'Data_TICNN/')
    
## backup do Max Min normilization
#for i in ['A','B','C','D']:
#    name_gr = 'Dataset' + i 
#    for j in range(0,9):
#        name_subgr = i + str(j)
#        dir_index = file[name_gr][name_subgr]
#        dir_index['DE_time_train'][:,:] = TICNN_lib.MaxMinNorm(dir_index['DE_time_train'][:,:], MaxMin[0,0], MaxMin[0,1])          
#        dir_index['DE_time_test'][:,:] = TICNN_lib.MaxMinNorm(dir_index['DE_time_test'][:,:], MaxMin[0,0], MaxMin[0,1])  
#        dir_index['FE_time_train'][:,:] = TICNN_lib.MaxMinNorm(dir_index['FE_time_train'][:,:], MaxMin[1,0], MaxMin[1,1])  
#        dir_index['FE_time_test'][:,:] = TICNN_lib.MaxMinNorm(dir_index['FE_time_test'][:,:], MaxMin[1,0], MaxMin[1,1])  
#file.close()    