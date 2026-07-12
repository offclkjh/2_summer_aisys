import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision.transforms import v2
import os
import numpy as np

# import matplotlib
# matplotlib.use("TkAgg")
# import matplotlib.pyplot as plt

import pandas as pd
form torchvision.io import decode_image

def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dataset = pickle.load(fo, encoding='bytes')
    return dataset

class CustomImageDataset(Dataset):
    def __init__(self, batches):
        self.batches = batches
        self.batch_num = len(batches)
        self.batch_sizes = [len(batches[i] for i in batch_num)]
        self.len = sum(batch_sizes)

    def __len__(self):
        return self.len
    
    def __getitem__(self, idx):
        for i in range(self.batch_num):
            if idx < self.batch_sizes[i]:
                break
            else:
                idx -= self.batch_sizes[i]
        
        image = torch.from_numpy(self.batches[i][b'data'][idx])
        # image already tensor rgb align
        image = v2.ToDtype(torch.float32, scale=True)(image.reshape(3, 32, 32))
        label = self.batches[i][b'labels'][idx]
        return image, label


train_batches = [unpickle(os.path.abspath("cifar-10-batches-py/data_batch_" + str(i+1)))
    for i in range(5)]
test_batch = unpickle(os.path.abspath("cifar-10-batches-py/test_batch"))
# print(batches[i].keys())

train_data = CustomImageDataset(train_batches)
test_data = CustomImageDataset(test_batch)

train_dataloader = DataLoader(
    train_data,
    batch_size=50,
    shuffle=True
)
test_dataloader = DataLoader(
    test_data,
    batch_size=50,
    shuffle=True
)

# MLP
class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(3*32*32, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10)
        )
    
    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

model = MLP()
learning_rate = 1e-3
batch_size = 50
epochs = 5

loss_fn = nn.CrossEntropyLoss()

def train_loop(dataloader, model,)