import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import numpy as np
import torch.nn.functional as F


# Automatically utilize RTX if CUDA is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Hyperparameters
batch_size = 64
learning_rate = 0.001
epochs = 5 # Keep it low for a quick test

# 2. Data Preparation
# Transforms convert the image into a PyTorch Tensor and normalize pixel values (0 to 1)
transform = transforms.Compose([transforms.ToTensor()])

# Download and load training and testing data
print("Downloading MNIST dataset...")
train_dataset = torchvision.datasets.MNIST(root='./data', train=True, transform=transform, download=True)
test_dataset = torchvision.datasets.MNIST(root='./data', train=False, transform=transform, download=True)

train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)
test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=1, shuffle=True)

# 3. Model Architecture (The Neural Network)
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        # Input layer: 28x28 pixels = 784 inputs
        # Hidden layer: 128 neurons
        self.fc1 = nn.Linear(28 * 28, 128) 
        self.fc2 = nn.Linear(128, 10)      

    def forward(self, x):
        x = x.view(-1, 28 * 28) 
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

model = SimpleNN().to(device)

criterion = nn.CrossEntropyLoss() 
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# 5. Training Loop
print("Starting training...")
for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)

        outputs = model(images)
        loss = criterion(outputs, labels)
        
        optimizer.zero_grad() 
        loss.backward()       
        optimizer.step()     
        
        running_loss += loss.item()
        
    print(f"Epoch [{epoch+1}/{epochs}], Loss: {running_loss/len(train_loader):.4f}")

print("Training finished!")

def visualize_prediction(model, data_loader):
    model.eval() 
    
    images, labels = next(iter(data_loader))
    image, label = images[0], labels[0]
    
    with torch.no_grad():
        image_device = image.unsqueeze(0).to(device)
        output = model(image_device)
        probabilities = F.softmax(output, dim=1).cpu().numpy().flatten()
    
    predicted_class = np.argmax(probabilities)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    ax1.imshow(image.squeeze().numpy(), cmap='gray')
    ax1.axis('off')
    ax1.set_title(f"Actual Label: {label.item()}\nNetwork Prediction: {predicted_class}")

    classes = np.arange(10)
    bars = ax2.bar(classes, probabilities, color='skyblue')
    bars[predicted_class].set_color('green' if predicted_class == label.item() else 'red')
    
    ax2.set_xticks(classes)
    ax2.set_ylim([0, 1.1])
    ax2.set_xlabel("Digit Class")
    ax2.set_ylabel("Probability")
    ax2.set_title("Network Confidence")
    
    plt.tight_layout()
    plt.show()

visualize_prediction(model, test_loader)

# Save the trained weights to a file
torch.save(model.state_dict(), "my_mnist_brain.pth")
print("Model saved to my_mnist_brain.pth")