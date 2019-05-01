# ======================================================================================
# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# 
# Created on Thu Nov 15 10:55:04 2018   
# @@author: Masterarbeit_Junning_Zhang
# ======================================================================================
'''
ToDo:
'''  
import torch
import torch.utils.data as utils_data
import torch.nn as nn
import torch.nn.functional as nn_func
import torch.autograd as autograd
import matplotlib.pyplot as plt
import TICNN_lib
import numpy as np
from torchsummary import summary # to output network structure 

# ========================= input variables ============================================
print('Dont forget to standardize training and evaluation datasets through TICNN_mat2h5.py')
dataset_train = str.upper(input('Please input the dataset for training(a,b,c or d):')) # input dataset for training
dataset_eval = str.upper(input('Please input the dataset for evaluation(a,b,c or d):')) # input dataset for evaluation
while True: # whether do evaluation after each epoch 
    bool_tempo = str.upper(input('Whether do evaluation after each epoch(Y or N):'))
    if bool_tempo == 'Y':
        bool_epoch_eval = True
        break
    elif bool_tempo == 'N':
        bool_epoch_eval = False
        break
    else:
        print('I dont unterstand, please input again')
    
h5_file = 'Data_TICNN/TICNN_2019-03-18.h5'
EPOCH = 20
BATCH_SIZE = 50
LR = 0.005
print('Dont forget to standardize training and evaluation datasets through TICNN_mat2h5.py')

# ============================= model define ===========================================
class ConvNeuralNet(nn.Module):
    def __init__(self, bn, dropout): # whether add Batch Normalization / Dropout function ///bool_bn, bool_dropout
        self.bn = bn
        self.dropout = dropout
        super(ConvNeuralNet, self).__init__()
        self.conv1 = nn.Conv1d(2, 16, kernel_size=64, stride=8, padding=28)
        self.conv2 = nn.Conv1d(16, 32, 3, 1, 1)
        self.conv3 = nn.Conv1d(32, 64, 3, 1, 1)
        self.conv4 = nn.Conv1d(64, 64, 3, 1, 1)
        self.conv5 = nn.Conv1d(64, 64, 3, 1, 1)
        self.conv6 = nn.Conv1d(64, 64, 3, 1) # no padding in conv6
        self.relu = nn.ReLU() # activation function
        self.pool = nn.MaxPool1d(kernel_size=2, stride=2)  
        self.lin1 = nn.Linear(3 * 64, 100)
        self.lin2 = nn.Linear(100, 10)    
        self.lin3 = nn.Linear(3 * 64, 10)
        # batch normalization layers
        self.bn2 = nn.BatchNorm1d(2) # num_features=2
        self.bn16 = nn.BatchNorm1d(16) # num_featvures=16
        self.bn32 = nn.BatchNorm1d(32) # num_features=32 
        self.bn64 = nn.BatchNorm1d(64) # num_features=64
        self.bn192 = nn.BatchNorm1d(192) # num_features=100
        # dropout layers
#        self.dropout_p = torch.distributions.uniform.Uniform(0.1,0.9)
        self.dropout_p = torch.distributions.uniform.Uniform(0.1,0.9)
        self.dropout = nn.Dropout(p=self.dropout_p.sample()) 
        
    def forward(self, x):         
        x = self.pool(self.dropout(self.relu(self.conv1(x))))
        x = self.pool(self.relu(self.conv2(x)))
        x = self.pool(self.relu(self.conv3(x)))
        x = self.pool(self.relu(self.conv4(x)))
        x = self.pool(self.relu(self.conv5(x))) 
        x = self.pool(self.relu(self.conv6(x))) 
        x = x.view(x.size(0),-1)
        x = self.lin1(x)
        x = self.lin2(x)
        x = nn_func.log_softmax(x,-1) # log(exp(x_i)/exp(x).sum())
        return x 
        
#        x = self.pool(self.relu(self.bn16(self.conv1(x))))
#        x = self.pool(self.relu(self.bn32(self.conv2(x))))
#        x = self.pool(self.relu(self.bn64(self.conv3(x))))
#        x = self.pool(self.relu(self.bn64(self.conv4(x))))
#        x = self.pool(self.relu(self.bn64(self.conv5(x))))
#        x = self.pool(self.relu(self.bn64(self.conv6(x))))
#        x = x.view(x.size(0),-1)
#        x = self.bn192(x)
#        x = self.lin1(x)
#        x = self.lin2(x)
#        x = nn_func.log_softmax(x,-1) # log(exp(x_i)/exp(x).sum())
#        return x 
        
#        x = self.bn16(self.pool(self.relu(self.conv1(x))))
#        x = self.bn32(self.pool(self.relu(self.conv2(x))))
#        x = self.bn64(self.pool(self.relu(self.conv3(x))))
#        x = self.bn64(self.pool(self.relu(self.conv4(x))))
#        x = self.bn64(self.pool(self.relu(self.conv5(x))))
#        x = self.bn64(self.pool(self.relu(self.conv6(x))))
#        x = x.view(x.size(0),-1)
#        x = self.lin1(x)
#        x = self.lin2(x)
#        x = nn_func.log_softmax(x,-1) # log(exp(x_i)/exp(x).sum())
#        return x 
        
#        x = self.pool(self.relu(self.bn16(self.conv1(x)))) # set BN after conv before relu
#        x = self.pool(self.relu(self.bn32(self.conv2(x))))
#        x = self.pool(self.relu(self.bn64(self.conv3(x))))
#        x = self.pool(self.relu(self.bn64(self.conv4(x))))
#        x = self.pool(self.relu(self.bn64(self.conv5(x))))
#        x = self.pool(self.relu(self.bn64(self.conv6(x))))
##        x = self.relu(x)
#        x = x.view(x.size(0),-1)
#        x = self.lin1(x)
#        x = self.lin2(x)
##        x = self.lin3(x)
#        x = nn_func.log_softmax(x,-1) # log(exp(x_i)/exp(x).sum())
#        return x 
       
#        x = self.pool(self.relu(self.bn16(self.conv1(x)))) # set BN after conv before relu
#        x = self.pool(self.relu(self.bn32(self.conv2(x))))
#        x = self.pool(self.relu(self.bn64(self.conv3(x))))
#        x = self.pool(self.relu(self.bn64(self.conv4(x))))
#        x = self.pool(self.relu(self.bn64(self.conv5(x))))
#        x = self.pool(self.relu(self.bn64(self.conv6(x))))
#        x = self.relu(x)
#        x = x.view(x.size(0),-1)
#        x = self.lin1(x)
#        x = self.lin2(x)
#        x = nn_func.log_softmax(x,-1) # log(exp(x_i)/exp(x).sum())
#        return x 
    
#        x = self.pool(self.dropout(self.relu(self.conv1(x))))
#        x = self.pool(self.relu(self.conv2(x)))
#        x = self.pool(self.relu(self.conv3(x)))
#        x = self.pool(self.relu(self.conv4(x)))
#        x = self.pool(self.relu(self.conv5(x))) 
#        x = self.pool(self.relu(self.conv6(x))) 
#        x = self.relu(x)
#        x = x.view(x.size(0),-1)
#        x = self.lin1(x)
#        x = self.lin2(x)
#        x = nn_func.log_softmax(x,-1) # log(exp(x_i)/exp(x).sum())
#        return x 
    
# =================== training and evaluaton ===========================================
ticnn = ConvNeuralNet(bn=False, dropout=False)
summary(ticnn, input_size=(2,2048))

## Training and evaluation model with CWRU Data & # load datasets for training and evaluation
train_data = TICNN_lib.TICNN_DataloaderCWRU(h5_file, [dataset_train], True)
train_data = utils_data.DataLoader(dataset=train_data, batch_size=BATCH_SIZE, shuffle=True)
optimizer = torch.optim.Adam(ticnn.parameters(), lr=LR)   # optimize all cnn parameters
loss_func = nn.CrossEntropyLoss()   # the target label is not one-hotted
loss_train_epoch = [] # array for loss in training
test_data = TICNN_lib.TICNN_DataloaderCWRU(h5_file, [dataset_eval], False)
test_data = utils_data.DataLoader(dataset=test_data)    
test_num = test_data.dataset.__len__()  
loss_eval_epoch = [] # array for loss in evaluation

for epoch in range(EPOCH):
    for step,(x,y) in enumerate(train_data): 
        loss_train_tempo = []
        ticnn.train()
        x = autograd.Variable(x)
        y = autograd.Variable(y).long()
        output = ticnn(x)
        optimizer.zero_grad()           # clear gradients for this training step
        loss = loss_func(output, y)     # cross entro py loss
        loss.backward()                 # backpropagation, compute gradients
        optimizer.step()                # apply gradients
        loss_train_tempo.append(loss.data)
    loss_train_epoch.append(sum(loss_train_tempo)/len(loss_train_tempo))
    
    if bool_epoch_eval == True: # after each epoch, evaluate the modell once 
        with torch.no_grad():
            loss_eval_tempo = []
            result = np.zeros((test_num,2)) # Actual class and predicted class
            correct_num = 0
            for step,(x,y) in enumerate(test_data): 
                ticnn.eval()
                y = y.long()
                output = ticnn(x)
                loss = loss_func(output, y)
                loss_eval_tempo.append(loss.data)
                #calculate the accuracy of the prediction for each class 
                output_max, y_predicted = torch.max(output, 1)
                y_predicted = y_predicted.type(torch.float)
                result[step] = [y_predicted,y]
                if y_predicted == y.float():
                    correct_num = correct_num + 1  
            accuracy = correct_num / test_num        
        loss_eval_epoch.append(sum(loss_eval_tempo)/len(loss_eval_tempo))
        print('Epoch:',epoch, '|Average-loss-train:',loss_train_epoch[epoch], '|Average-loss-eval.:',loss_eval_epoch[epoch], '|Eval.accuracy:%.2f%%' %(100*accuracy))
    elif bool_epoch_eval == False: 
        print('Epoch:',epoch, '|Average-loss-train:',loss_train_epoch[epoch])
        
if bool_epoch_eval == False: # evaluate the modell only once 
    with torch.no_grad():
        result = np.zeros((test_num,2)) # Actual class and predicted class
        correct_num = 0
        for step,(x,y) in enumerate(test_data): 
            ticnn.eval()
            output = ticnn(x)
            #calculate the accuracy of the prediction for each class 
            output_max, y_predicted = torch.max(output, 1)
#            y_predicted = y_predicted.type(torch.float)
            result[step] = [y_predicted,y]
            if y_predicted == y.long():
                correct_num = correct_num + 1  
        accuracy = correct_num / test_num        
    print('Eval.accuracy after all epoch:%.2f%%' %(100*accuracy))
 
# ================================= Plot ===============================================
# Plot Loss vs Epoch
if bool_epoch_eval == False:
    plt.plot(loss_train_epoch, marker='o')
    plt.xticks(np.arange(EPOCH))
    plt.xlim((0,EPOCH))
    plt.xlabel('Epoch') 
    plt.ylabel('Average loss') 
    plt.title('Epoch loss in Training') 
    plt.show()
if bool_epoch_eval == True:
    plt.plot(range(EPOCH),loss_train_epoch, range(EPOCH),loss_eval_epoch,marker='o')
    plt.xticks(np.arange(EPOCH))
    plt.xlim((0,EPOCH))
    plt.xlabel('Epoch') 
    plt.ylabel('Average loss') 
    plt.title('Epoch loss in Training and Evaluation') 
    plt.legend(labels=['loss in training','loss in evaluation'],loc='upper right')
    plt.show()
# plot accuracy of the prediction for each class 
result_class = np.zeros(10)
for i in range(10):
    result_class[i] = sum(j[0]==j[1] for j in result[i*(int(len(result)/10)):(i+1)*int(len(result)/10)])
    result_class[i] = result_class[i] / (len(result)/10) 
plt.bar(range(10), result_class, width = 0.5)
for a,b in zip(range(10),result_class):
    plt.text(a,b, '%.2f%%'%(100*b), ha='center',va='bottom', fontsize=8)
plt.title('Model prediction accuracy of each class')
plt.xlabel('Class No.') 
plt.xticks(np.arange(10))
plt.ylabel('prediction accuracy')
plt.show()
# ======================================================================================
