import torch
import torchvision.models as models
import os
from training_MLP import MLP, test_dataloader
from torch import nn

# # saving
# model = models.vgg16(weights='IMAGENET1K_V1')
# torch.save(model.state_dict(), 'model_weights.pth')

# loading
# check the directory
print(os.getcwd())
print(os.path.abspath("model_weights.pth"))

# model = models.vgg16() # we do not specify ``weights``, i.e. create untrained model
# model.load_state_dict(torch.load('model_weights.pth', weights_only=True))
# model.eval()

model = MLP()

model.load_state_dict(
    torch.load('model_weights_MLP.pth', weights_only=True)
)

model.eval()


loss_fn = nn.CrossEntropyLoss()

test_size = len(test_dataloader.dataset)
num_batches = len(test_dataloader)

total_loss = 0.0
correct = 0

with torch.inference_mode():
    for images, labels in test_dataloader:
        outputs = model(images)

        total_loss += loss_fn(outputs, labels).item()
        predictions = outputs.argmax(dim=1)
        correct += (predictions == labels).sum().item()

average_loss = total_loss / num_batches
accuracy = 100 * correct / test_size

print(f"Test samples: {test_size}")
print(f"Accuracy: {accuracy:.1f}%")
print(f"Average loss: {average_loss:.6f}")