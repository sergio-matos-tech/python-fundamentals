import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np

class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(28 * 28, 128) 
        self.fc2 = nn.Linear(128, 10)      

    def forward(self, x):
        x = x.view(-1, 28 * 28) 
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# 2. Load the saved "Brain"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SimpleNN().to(device)
model.load_state_dict(torch.load("my_mnist_brain.pth", weights_only=True))
model.eval() # Set to testing mode

def process_custom_image(image_path):
    img = Image.open(image_path)
    img = img.convert('L')
    img = ImageOps.invert(img)
    img = img.resize((28, 28))
    transform = transforms.ToTensor()
    tensor_img = transform(img)
    
    return tensor_img


image_path = "5.jpeg" 
my_tensor = process_custom_image(image_path)

with torch.no_grad():
    # Send the tensor to the GPU and add a "batch" dimension
    my_tensor_device = my_tensor.unsqueeze(0).to(device)
    output = model(my_tensor_device)
    probabilities = F.softmax(output, dim=1).cpu().numpy().flatten()

predicted_class = np.argmax(probabilities)

# 5. Display the Results
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# Show how the network "sees" your drawing after preprocessing
ax1.imshow(my_tensor.squeeze().numpy(), cmap='gray')
ax1.axis('off')
ax1.set_title(f"How the Network Sees It\nPrediction: {predicted_class}")

# Show the confidence
classes = np.arange(10)
bars = ax2.bar(classes, probabilities, color='skyblue')
bars[predicted_class].set_color('green')
ax2.set_xticks(classes)
ax2.set_ylim([0, 1.1])
ax2.set_title("Network Confidence")

plt.tight_layout()
plt.show()