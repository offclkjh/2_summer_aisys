import torch
import torchvision.models as models
import os
import 6_optimization

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

model = NeuralNetwork()

model.loat_state_dict(
    torch.load('model_weights.pth', weights_only=True)
)

model.eval()