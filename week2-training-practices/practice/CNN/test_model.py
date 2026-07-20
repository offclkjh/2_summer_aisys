import torch
import torchvision
from torchvision.transforms import v2
from classifier import Net, testloader, imshow, classes, PATH

import matplotlib.pyplot as plt
import numpy as np

# 5. test the network on the test data
dataiter = iter(testloader)
images, labels = next(dataiter)

# print images
imshow(torchvision.utils.make_grid(images))
print('GroundTruth: ', ' '.join(f'{classes[labels[j]]:5s}' for j in range(4)))

net = Net()
net.load_state_dict(torch.load(PATH, weights_only=True))
net.eval()

outputs = net(images)

_, predicted = torch.max(outputs, 1)

print('Predicted: ', ' '.join(f'{classes[predicted[j]]:5s}'
                              for j in range(4)))

correct = 0
total = 0
# since we're not training, we don't need to calculate the gradients for our outputs
with torch.no_grad():
    for data in testloader:
        images, labels = data
        # calculate outputs by running images through the network
        outputs = net(images)
        # the class with the highest energy is what we choose as prediction
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print(f'Accuracy of the network on the 10000 test images: {100 * correct // total} %')

# prepare to count predictions for each class
criterion = torch.nn.CrossEntropyLoss()

correct = 0
total = 0
test_loss = 0.0

with torch.no_grad():
    for images, labels in testloader:
        outputs = net(images)

        loss = criterion(outputs, labels)
        test_loss += loss.item() * labels.size(0)

        predicted = outputs.argmax(dim=1)

        total += labels.size(0)
        correct += (predicted == labels).sum().item()

average_loss = test_loss / total
accuracy = 100 * correct / total

print(f"Accuracy: {accuracy:.1f}%")
print(f"Average loss: {average_loss:.6f}")