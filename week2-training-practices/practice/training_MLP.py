import torch
from torch import nn
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torchvision.transforms import v2
import os
import numpy as np

# import matplotlib
# matplotlib.use("TkAgg")
# import matplotlib.pyplot as plt

def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dataset = pickle.load(fo, encoding='bytes')
    return dataset

class CustomImageDataset(Dataset):
    def __init__(self, batch_list):
        self.batch_list = batch_list
        self.batch_num = len(batch_list)
        self.batch_sizes = [len(batch_list[i][b'data']) for i in range(self.batch_num)]
        self.len = sum(self.batch_sizes)
        self.transform = v2.Compose([
            v2.ToDtype(torch.float32, scale=True),
            v2.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])

    def __len__(self):
        return self.len
    
    def __getitem__(self, idx):
        for i in range(self.batch_num):
            if idx < self.batch_sizes[i]:
                break
            else:
                idx -= self.batch_sizes[i]
        
        image = torch.from_numpy(self.batch_list[i][b'data'][idx])
        # image already tensor rgb align
        image = image.reshape(3, 32, 32)
        image = self.transform(image)
        label = self.batch_list[i][b'labels'][idx]
        return image, label

train_batch_list = [unpickle(os.path.abspath("cifar-10-batches-py/data_batch_" + str(i+1)))
    for i in range(5)]
test_batch_list = unpickle(os.path.abspath("cifar-10-batches-py/test_batch"))
# print(batch_list[i].keys())

train_data = CustomImageDataset(train_batch_list)
test_data = CustomImageDataset([test_batch_list])

train_dataloader = DataLoader(
    train_data,
    batch_size=5,
    shuffle=True,
    num_workers=2
)
test_dataloader = DataLoader(
    test_data,
    batch_size=5,
    shuffle=False,
    num_workers=2
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



def train_loop(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    model.train()
    for batch, (X, y) in enumerate(dataloader):
        pred = model(X)
        loss = loss_fn(pred, y)

        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        if batch % 100 == 0:
            loss, current = loss.item(), batch * dataloader.batch_size + len(X)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")

def test_loop(dataloader, model, loss_fn):
    model.eval()
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    test_loss, correct = 0, 0

    with torch.no_grad():
        for X, y in dataloader:
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    
    test_loss /= num_batches
    correct /= size
    print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")

import torch.optim as optim

def main():
    

    model = MLP()
    learning_rate = 1e-3
    batch_size = 5
    epochs = 5

    loss_fn = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

    epochs = 6
    for t in range(epochs):
        print(f"Epoch {t+1}\n-------------------------------")
        train_loop(train_dataloader, model, loss_fn, optimizer)
        test_loop(test_dataloader, model, loss_fn)
    print("Done!")

    torch.save(model.state_dict(), 'model_weights_MLP.pth')
    print("model saved!")

if __name__ == "__main__":
    main()