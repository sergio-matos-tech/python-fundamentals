import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt

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

# 2. Load the Saved "Brain"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SimpleNN().to(device)
model.load_state_dict(torch.load("my_mnist_brain.pth", weights_only=True))
model.eval() # Set to evaluation mode

# 3. Load the 10,000 Test Images
transform = transforms.Compose([transforms.ToTensor()])
# Notice train=False here. We are only loading the test vault.
test_dataset = torchvision.datasets.MNIST(root='./data', train=False, transform=transform, download=False)

test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=9, shuffle=True)

# 4. Grab one batch of 9 random images
dataiter = iter(test_loader)
images, labels = next(dataiter)

# 5. Make the Predictions
with torch.no_grad():
    images_device = images.to(device)
    outputs = model(images_device)
    _, predicted = torch.max(outputs, 1) 

fig, axes = plt.subplots(3, 3, figsize=(8, 8))
fig, axes = plt.subplots(3, 3, figsize=(8, 8))

fig.suptitle('Testing on the MNIST Vault', fontsize=16, fontweight='bold')
for i, ax in enumerate(axes.flat):
    ax.imshow(images[i].squeeze().numpy(), cmap='gray')
    
    actual = labels[i].item()
    guess = predicted[i].item()
    
    color = 'green' if actual == guess else 'red'
    ax.set_title(f"Actual: {actual} | Guess: {guess}", color=color, fontweight='bold')
    ax.axis('off')

plt.tight_layout()
plt.show()